from __future__ import annotations

import argparse
import sys
from pathlib import Path

from contract_surface import ContractSurfaceError, compute_contract_surface, load_surface_registry, select_surface


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the LawFirm OS contract surface registry.")
    parser.add_argument("--substrate", default=".")
    args = parser.parse_args()
    substrate = Path(args.substrate).resolve()
    errors: list[str] = []
    try:
        registry = load_surface_registry(substrate)
        seen: set[str] = set()
        for surface in registry.get("surfaces", []):
            sid = surface.get("surface_id")
            if sid in seen:
                errors.append(f"duplicate surface_id: {sid}")
            seen.add(sid)
            if not surface.get("include_patterns"):
                errors.append(f"surface {sid} has no include_patterns")
            if surface.get("hash_algorithm") != "lawfirm_os_contract_surface_sha256.v1":
                errors.append(f"surface {sid} has unsupported hash_algorithm")
            try:
                result = compute_contract_surface(substrate, sid)
                if result["included_file_count"] <= 0:
                    errors.append(f"surface {sid} selected zero files")
            except ContractSurfaceError as exc:
                errors.append(str(exc))
        try:
            select_surface(registry, registry.get("default_surface_id"))
        except ContractSurfaceError as exc:
            errors.append(str(exc))
    except ContractSurfaceError as exc:
        errors.append(str(exc))
    if errors:
        print("Contract surface registry validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Contract surface registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
