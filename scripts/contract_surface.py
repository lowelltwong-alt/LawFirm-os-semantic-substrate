from __future__ import annotations

import fnmatch
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HASH_ALGORITHM = "lawfirm_os_contract_surface_sha256.v1"
DEFAULT_REGISTRY_PATH = Path("registry/contract-surface-registry.json")


class ContractSurfaceError(RuntimeError):
    pass


@dataclass(frozen=True)
class IncludedFile:
    path: str
    sha256: str
    size_bytes: int


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractSurfaceError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ContractSurfaceError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ContractSurfaceError(f"expected JSON object in {path}")
    return data


def _matches(rel: str, pattern: str) -> bool:
    rel = rel.replace("\\", "/")
    pattern = pattern.replace("\\", "/")
    if fnmatch.fnmatch(rel, pattern):
        return True
    if pattern.endswith("/**"):
        return rel.startswith(pattern[:-3].rstrip("/") + "/")
    if pattern.endswith("/**/*"):
        return rel.startswith(pattern[:-5].rstrip("/") + "/")
    if "/**/" in pattern:
        shallow = pattern.replace("/**/", "/")
        if fnmatch.fnmatch(rel, shallow):
            return True
    return False


def _is_excluded(rel: str, exclude_patterns: list[str]) -> bool:
    return any(_matches(rel, pattern) for pattern in exclude_patterns)


def _is_included(rel: str, include_patterns: list[str]) -> bool:
    return any(_matches(rel, pattern) for pattern in include_patterns)


def load_surface_registry(substrate_root: Path, registry_path: Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    registry = read_json(substrate_root / registry_path)
    if registry.get("schema_version") != "contract_surface_registry.v1":
        raise ContractSurfaceError("contract surface registry has unsupported schema_version")
    if registry.get("hash_algorithm") != HASH_ALGORITHM:
        raise ContractSurfaceError("contract surface registry has unsupported hash_algorithm")
    if not isinstance(registry.get("surfaces"), list) or not registry["surfaces"]:
        raise ContractSurfaceError("contract surface registry must define at least one surface")
    return registry


def select_surface(registry: dict[str, Any], surface_id: str | None = None) -> dict[str, Any]:
    wanted = surface_id or registry.get("default_surface_id")
    for surface in registry.get("surfaces", []):
        if surface.get("surface_id") == wanted:
            return surface
    raise ContractSurfaceError(f"unknown contract surface id: {wanted}")


def discover_included_files(substrate_root: Path, surface: dict[str, Any]) -> list[IncludedFile]:
    include_patterns = list(surface.get("include_patterns", []))
    exclude_patterns = list(surface.get("exclude_patterns", []))
    if not include_patterns:
        raise ContractSurfaceError("contract surface include_patterns must not be empty")
    included: list[IncludedFile] = []
    for path in sorted(substrate_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(substrate_root).as_posix()
        if any(part in {".git", "__pycache__", ".pytest_cache", ".ruff_cache"} for part in Path(rel).parts):
            continue
        if not _is_included(rel, include_patterns):
            continue
        if _is_excluded(rel, exclude_patterns):
            continue
        data = path.read_bytes()
        included.append(IncludedFile(path=rel, sha256=hashlib.sha256(data).hexdigest(), size_bytes=len(data)))
    return included


def contract_surface_digest(surface_id: str, included_files: list[IncludedFile]) -> tuple[str, str]:
    if not included_files:
        raise ContractSurfaceError("contract surface selected zero files")
    manifest_bytes = json.dumps([f.__dict__ for f in included_files], sort_keys=True, separators=(",", ":")).encode("utf-8")
    manifest_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
    digest = hashlib.sha256()
    digest.update(HASH_ALGORITHM.encode("utf-8"))
    digest.update(b"\0")
    digest.update(surface_id.encode("utf-8"))
    digest.update(b"\0")
    for item in included_files:
        digest.update(item.path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(item.sha256.encode("ascii"))
        digest.update(b"\0")
        digest.update(str(item.size_bytes).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest(), manifest_sha256


def compute_contract_surface(substrate_root: Path, surface_id: str | None = None, registry_path: Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    substrate_root = substrate_root.resolve()
    registry = load_surface_registry(substrate_root, registry_path)
    surface = select_surface(registry, surface_id)
    selected_surface_id = str(surface["surface_id"])
    included = discover_included_files(substrate_root, surface)
    surface_hash, manifest_hash = contract_surface_digest(selected_surface_id, included)
    return {
        "schema_version": "contract_surface_hash_result.v1",
        "surface_id": selected_surface_id,
        "surface_sha256": surface_hash,
        "surface_registry_path": registry_path.as_posix(),
        "hash_algorithm": HASH_ALGORITHM,
        "included_file_count": len(included),
        "included_files_manifest_sha256": manifest_hash,
        "included_files": [f.__dict__ for f in included],
    }
