import json
import os
import re
from pathlib import Path


BASE = os.path.dirname(os.path.dirname(__file__))
EXAMPLES_DIR = os.path.join(BASE, "examples")
ACTIVE_SKIP_DIRS = {"legacy", "archive", "__pycache__"}

SOURCE_REF_PATTERN = re.compile(r"^SRC-[A-Za-z0-9_-]+$")
EVIDENCE_REF_PATTERN = re.compile(r"^CHK-[A-Za-z0-9_-]+$")
ACTIVE_SOURCE_READY_STATUSES = {"approved", "active"}
ACTIVE_DOCUMENT_STATUSES = {"active"}
ACTIVE_DOCUMENT_VERSION_STATUSES = {"active"}
ACTIVE_SOURCE_ARTIFACT_STATUSES = {"captured"}


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_schema_registry(base_dir: str | Path = BASE):
    data = load_json(os.path.join(base_dir, "registry", "schema-registry.json"))
    return {entry["schema_id"]: entry for entry in data["schemas"]}


def load_template_registry(base_dir: str | Path = BASE):
    data = load_json(os.path.join(base_dir, "registry", "template-registry.json"))
    return {entry["template_id"]: entry for entry in data["templates"]}


def load_object_prefixes(base_dir: str | Path = BASE):
    return load_json(os.path.join(base_dir, "registry", "object_prefix_registry.json"))


def active_examples(examples_dir: str | Path = EXAMPLES_DIR):
    for root, dirs, files in os.walk(str(examples_dir)):
        dirs[:] = [d for d in dirs if d not in ACTIVE_SKIP_DIRS]
        for name in files:
            if not name.endswith(".json"):
                continue

            path = os.path.join(root, name)
            data = load_json(path)
            yield path, data


def canonical_examples(examples_dir: str | Path = EXAMPLES_DIR):
    examples_dir = Path(examples_dir)
    allowed_roots = {
        examples_dir / "claims",
        examples_dir / "artifacts",
    }
    for path, data in active_examples(examples_dir):
        path_obj = Path(path)
        if any(path_obj.is_relative_to(root) for root in allowed_roots):
            yield path, data


def answer_examples(examples_dir: str | Path = EXAMPLES_DIR):
    examples_dir = Path(examples_dir)
    allowed_root = examples_dir / "answer-events"
    for path, data in active_examples(examples_dir):
        path_obj = Path(path)
        if path_obj.is_relative_to(allowed_root):
            yield path, data


def object_kind(data):
    if "claim_id" in data:
        return "claim"
    if "id" in data and "artifact_type" in data:
        return "artifact"
    return None


def object_identifier(data):
    if "claim_id" in data:
        return data["claim_id"]
    return data.get("id")


def active_object_ids(data):
    identifiers = set()
    for key, value in data.items():
        if not isinstance(value, str):
            continue
        if key == "id":
            identifiers.add(value)
        elif key.endswith("_id") and key not in {"schema_id", "template_id"}:
            identifiers.add(value)
    address_struct = data.get("address_struct", {})
    if isinstance(address_struct, dict):
        object_id = address_struct.get("object_id")
        if isinstance(object_id, str):
            identifiers.add(object_id)
    return identifiers


def validate_reference_patterns(values, pattern, label, path, failures):
    for value in values:
        if not isinstance(value, str) or not pattern.fullmatch(value):
            failures.append(f"{path}: invalid {label} value '{value}'")


def load_answer_support_inventory(examples_dir: str | Path = EXAMPLES_DIR):
    examples_dir = Path(examples_dir)
    inventory = {
        "retrieval_responses": {},
        "answer_evidence": {},
        "access_decisions": {},
    }
    bundle_path = examples_dir / "documents" / "answer-trace.example.json"
    if bundle_path.exists():
        bundle = load_json(bundle_path)
        retrieval_response = bundle.get("retrieval_response", {})
        retrieval_response_id = retrieval_response.get("retrieval_response_id")
        if isinstance(retrieval_response_id, str):
            inventory["retrieval_responses"][retrieval_response_id] = {
                "access_decision_id": retrieval_response.get("access_decision_id"),
            }

        access_decision = bundle.get("access_decision", {})
        access_decision_id = access_decision.get("access_decision_id")
        if isinstance(access_decision_id, str):
            inventory["access_decisions"][access_decision_id] = {
                "decision": access_decision.get("decision"),
                "purpose_of_use": (access_decision.get("environment") or {}).get("purpose_of_use"),
                "source_policy_refs": set((access_decision.get("policy_basis") or {}).get("source_policy_refs", [])),
                "confidentiality_class": (access_decision.get("target_ref") or {}).get("confidentiality_class"),
            }

        for evidence in bundle.get("answer_evidence", []):
            evidence_id = evidence.get("answer_evidence_id")
            if isinstance(evidence_id, str):
                inventory["answer_evidence"][evidence_id] = {
                    "document_version_id": evidence.get("document_version_id"),
                }

    for _, data in active_examples(examples_dir):
        schema_type = data.get("schema_type")
        if schema_type == "retrieval-response":
            retrieval_response_id = data.get("retrieval_response_id")
            if isinstance(retrieval_response_id, str):
                inventory["retrieval_responses"][retrieval_response_id] = {
                    "access_decision_id": data.get("access_decision_id"),
                }
        elif schema_type == "access-decision":
            access_decision_id = data.get("access_decision_id")
            if isinstance(access_decision_id, str):
                inventory["access_decisions"][access_decision_id] = {
                    "decision": data.get("decision"),
                    "purpose_of_use": (data.get("environment") or {}).get("purpose_of_use"),
                    "source_policy_refs": set((data.get("policy_basis") or {}).get("source_policy_refs", [])),
                    "confidentiality_class": (data.get("target_ref") or {}).get("confidentiality_class"),
                }
        elif schema_type == "answer-evidence":
            evidence_id = data.get("answer_evidence_id")
            if isinstance(evidence_id, str):
                inventory["answer_evidence"][evidence_id] = {
                    "document_version_id": data.get("document_version_id"),
                }

    return inventory


def build_governed_source_inventory(examples_dir: str | Path = EXAMPLES_DIR):
    examples_dir = Path(examples_dir)
    inventory = {
        "source_refs": {},
        "document_versions": {},
    }

    def add_source_ref(ref_id, metadata):
        if isinstance(ref_id, str):
            inventory["source_refs"][ref_id] = metadata

    def add_document_version(version_id, metadata):
        if isinstance(version_id, str):
            inventory["document_versions"][version_id] = metadata

    for _, data in active_examples(examples_dir):
        if data.get("schema_type") != "document":
            continue
        source_ref = (data.get("address_struct") or {}).get("object_id")
        access_policy_ref = data.get("access_policy_ref")
        authority_zone = (data.get("address_struct") or {}).get("authority_zone")
        restricted = authority_zone not in {None, "public"} or isinstance(access_policy_ref, str)
        stale_reason = None
        if data.get("canonical_status") is not None and data.get("canonical_status") not in ACTIVE_DOCUMENT_STATUSES:
            stale_reason = f"document.canonical_status is {data.get('canonical_status')}"
        add_source_ref(
            source_ref,
            {
                "is_restricted": restricted,
                "source_policy_refs": {access_policy_ref} if isinstance(access_policy_ref, str) else set(),
                "stale_reason": stale_reason,
            },
        )

    bundle_path = examples_dir / "documents" / "legal-document.example.json"
    manifest_path = examples_dir / "documents" / "source-ingestion-manifest.example.json"
    if bundle_path.exists():
        bundle = load_json(bundle_path)
        manifest = load_json(manifest_path) if manifest_path.exists() else {}
        document = bundle.get("document", {})
        document_version = bundle.get("document_version", {})
        source_artifact = bundle.get("source_artifact", {})
        bundle_source_ref = (bundle.get("address_struct") or {}).get("object_id")
        bundle_policy_refs = {
            ref
            for ref in {
                document.get("access_policy_ref"),
                manifest.get("access_policy_ref"),
            }
            if isinstance(ref, str)
        }
        bundle_restricted = (
            (bundle.get("address_struct") or {}).get("authority_zone") not in {None, "public"}
            or manifest.get("confidentiality_class") not in {None, "public"}
            or bool(bundle_policy_refs)
        )
        stale_reasons = []
        if document.get("canonical_status") not in ACTIVE_DOCUMENT_STATUSES:
            stale_reasons.append(f"document.canonical_status is {document.get('canonical_status')}")
        if document_version.get("status") not in ACTIVE_DOCUMENT_VERSION_STATUSES:
            stale_reasons.append(f"document_version.status is {document_version.get('status')}")
        if source_artifact.get("status") not in ACTIVE_SOURCE_ARTIFACT_STATUSES:
            stale_reasons.append(f"source_artifact.status is {source_artifact.get('status')}")
        lifecycle_status = manifest.get("lifecycle_status")
        if lifecycle_status is not None and lifecycle_status not in ACTIVE_SOURCE_READY_STATUSES:
            stale_reasons.append(f"source_ingestion_manifest.lifecycle_status is {lifecycle_status}")
        metadata = {
            "is_restricted": bundle_restricted,
            "source_policy_refs": bundle_policy_refs,
            "stale_reason": "; ".join(stale_reasons) if stale_reasons else None,
        }
        add_source_ref(bundle_source_ref, metadata)
        add_document_version(document_version.get("document_version_id"), metadata)

    return inventory


def validate_access_basis(path, basis, required_policy_refs, failures, *, required_purpose_of_use=None, required_access_decision_id=None):
    if not required_policy_refs and required_purpose_of_use is None and required_access_decision_id is None:
        return
    if not isinstance(basis, dict):
        failures.append(
            f"{path}: restricted governed support requires access_basis with purpose_of_use and source_policy_refs"
        )
        return

    purpose_of_use = basis.get("purpose_of_use")
    if not isinstance(purpose_of_use, str) or len(purpose_of_use) < 3:
        failures.append(f"{path}: access_basis.purpose_of_use must be populated for restricted governed support")
    elif required_purpose_of_use is not None and purpose_of_use != required_purpose_of_use:
        failures.append(
            f"{path}: access_basis.purpose_of_use '{purpose_of_use}' must match '{required_purpose_of_use}'"
        )

    source_policy_refs = basis.get("source_policy_refs")
    if not isinstance(source_policy_refs, list) or not source_policy_refs:
        failures.append(f"{path}: access_basis.source_policy_refs must be a non-empty list for restricted governed support")
    else:
        missing_policy_refs = sorted(set(required_policy_refs) - set(source_policy_refs))
        for policy_ref in missing_policy_refs:
            failures.append(
                f"{path}: access_basis.source_policy_refs must include governed source policy '{policy_ref}'"
            )

    if required_access_decision_id is not None:
        access_decision_id = basis.get("access_decision_id")
        if access_decision_id != required_access_decision_id:
            failures.append(
                f"{path}: access_basis.access_decision_id '{access_decision_id}' must match '{required_access_decision_id}'"
            )


def collect_failures(base_dir: str | Path = BASE):
    base_dir = Path(base_dir)
    examples_dir = base_dir / "examples"
    schema_registry = load_schema_registry(base_dir)
    template_registry = load_template_registry(base_dir)
    object_prefixes = load_object_prefixes(base_dir)
    answer_support_inventory = load_answer_support_inventory(examples_dir)
    governed_source_inventory = build_governed_source_inventory(examples_dir)

    failures = []
    inventory = {"claim": {}, "artifact": {}}
    active_ids = {}

    examples = list(canonical_examples(examples_dir))

    for path, data in active_examples(examples_dir):
        for identifier in active_object_ids(data):
            active_ids.setdefault(identifier, []).append(path)

    for path, data in examples:
        kind = object_kind(data)
        identifier = object_identifier(data)

        if kind is None or identifier is None:
            continue

        if identifier in inventory[kind]:
            failures.append(
                f"{path}: duplicate {kind} identifier '{identifier}' also found in {inventory[kind][identifier]}"
            )
        else:
            inventory[kind][identifier] = path

    for path, data in examples:
        kind = object_kind(data)
        if kind is None:
            continue

        identifier = object_identifier(data)
        schema_id = data.get("schema_id")
        template_id = data.get("template_id")
        address_struct = data.get("address_struct", {})
        authority_zone = data.get("authority_zone")

        if schema_id is not None and schema_id not in schema_registry:
            failures.append(f"{path}: schema_id '{schema_id}' is not registered")
        elif schema_id is not None:
            schema_entry = schema_registry[schema_id]
            if kind not in schema_entry.get("applies_to", []):
                failures.append(
                    f"{path}: schema_id '{schema_id}' does not apply to {kind}"
                )

        if template_id is not None and template_id not in template_registry:
            failures.append(f"{path}: template_id '{template_id}' is not registered")
        elif template_id is not None:
            template_entry = template_registry[template_id]
            if kind not in template_entry.get("applies_to", []):
                failures.append(
                    f"{path}: template_id '{template_id}' does not apply to {kind}"
                )
            for field in template_entry.get("required_metadata_fields", []):
                if field not in data:
                    failures.append(
                        f"{path}: missing required template field '{field}'"
                    )

        expected_prefix = None
        if kind == "claim":
            expected_prefix = next(
                (prefix for prefix, value in object_prefixes.items() if value == "claim"),
                None,
            )
        elif kind == "artifact":
            expected_prefix = next(
                (prefix for prefix, value in object_prefixes.items() if value == "artifact"),
                None,
            )

        if expected_prefix and not str(identifier).startswith(f"{expected_prefix}-"):
            failures.append(
                f"{path}: identifier '{identifier}' does not use expected {expected_prefix} prefix"
            )

        if address_struct.get("object_id") != identifier:
            failures.append(
                f"{path}: address_struct.object_id does not match object identifier"
            )

        if address_struct.get("object_type") != kind:
            failures.append(
                f"{path}: address_struct.object_type '{address_struct.get('object_type')}' should be '{kind}'"
            )

        if authority_zone and address_struct.get("authority_zone") != authority_zone:
            failures.append(
                f"{path}: authority_zone does not match address_struct.authority_zone"
            )

        if kind == "claim":
            if not data.get("source_refs"):
                failures.append(
                    f"{path}: substantive claim requires at least one source_ref; empty-corpus assertions must refuse instead of inventing facts"
                )
            if not data.get("evidence_refs"):
                failures.append(
                    f"{path}: substantive claim requires at least one evidence_ref; empty-corpus assertions must refuse instead of inventing facts"
                )
            validate_reference_patterns(
                data.get("source_refs", []),
                SOURCE_REF_PATTERN,
                "source_refs",
                path,
                failures,
            )
            for source_ref in data.get("source_refs", []):
                if source_ref not in active_ids:
                    failures.append(
                        f"{path}: source_ref '{source_ref}' does not resolve to an active example object"
                    )
                metadata = governed_source_inventory["source_refs"].get(source_ref)
                if metadata:
                    if metadata.get("stale_reason"):
                        failures.append(
                            f"{path}: source_ref '{source_ref}' resolves to stale governed support ({metadata['stale_reason']})"
                        )
            validate_reference_patterns(
                data.get("evidence_refs", []),
                EVIDENCE_REF_PATTERN,
                "evidence_refs",
                path,
                failures,
            )
            for evidence_ref in data.get("evidence_refs", []):
                if evidence_ref not in active_ids:
                    failures.append(
                        f"{path}: evidence_ref '{evidence_ref}' does not resolve to an active example object"
                    )

            for artifact_ref in data.get("artifact_refs", []):
                if artifact_ref not in inventory["artifact"]:
                    failures.append(
                        f"{path}: artifact_ref '{artifact_ref}' does not resolve to a canonical artifact example"
                    )

            for claim_ref in data.get("derived_from_claims", []):
                if claim_ref not in inventory["claim"]:
                    failures.append(
                        f"{path}: derived_from_claim '{claim_ref}' does not resolve to a canonical claim example"
                    )

            restricted_policy_refs = set()
            for source_ref in data.get("source_refs", []):
                metadata = governed_source_inventory["source_refs"].get(source_ref)
                if metadata and metadata.get("is_restricted"):
                    restricted_policy_refs.update(metadata.get("source_policy_refs", set()))
            validate_access_basis(
                path,
                data.get("access_basis"),
                restricted_policy_refs,
                failures,
            )

        if kind == "artifact":
            attribution_chain = data.get("attribution_chain", {})
            validate_reference_patterns(
                attribution_chain.get("primary_sources", []),
                SOURCE_REF_PATTERN,
                "attribution_chain.primary_sources",
                path,
                failures,
            )
            for source_ref in attribution_chain.get("primary_sources", []):
                if source_ref not in active_ids:
                    failures.append(
                        f"{path}: attribution_chain.primary_source '{source_ref}' does not resolve to an active example object"
                    )

            for derived_ref in attribution_chain.get("derived_from", []):
                if (
                    derived_ref not in inventory["artifact"]
                    and derived_ref not in inventory["claim"]
                ):
                    failures.append(
                        f"{path}: attribution_chain.derived_from '{derived_ref}' does not resolve to a canonical claim or artifact example"
                    )

    for path, data in answer_examples(examples_dir):
        grounding_status = data.get("grounding_status")
        if grounding_status not in {"grounded", "partially_grounded"}:
            continue

        answer_evidence_ids = data.get("answer_evidence_ids", [])
        if not answer_evidence_ids:
            failures.append(
                f"{path}: grounded answer_event requires answer_evidence_ids; empty-corpus responses must refuse instead of asserting internal facts"
            )

        retrieval_response_id = data.get("retrieval_response_id")
        retrieval_response = answer_support_inventory["retrieval_responses"].get(retrieval_response_id)
        if retrieval_response_id and retrieval_response is None:
            failures.append(
                f"{path}: retrieval_response_id '{retrieval_response_id}' does not resolve to grounded support"
            )

        restricted_policy_refs = set()
        stale_evidence_reasons = []
        for evidence_id in answer_evidence_ids:
            evidence = answer_support_inventory["answer_evidence"].get(evidence_id)
            if evidence is None:
                failures.append(
                    f"{path}: answer_evidence_id '{evidence_id}' does not resolve to grounded support"
                )
                continue
            document_version_id = evidence.get("document_version_id")
            metadata = governed_source_inventory["document_versions"].get(document_version_id)
            if metadata:
                if metadata.get("stale_reason"):
                    stale_evidence_reasons.append(
                        f"document_version '{document_version_id}' is stale ({metadata['stale_reason']})"
                    )
                if metadata.get("is_restricted"):
                    restricted_policy_refs.update(metadata.get("source_policy_refs", set()))

        for reason in stale_evidence_reasons:
            failures.append(f"{path}: grounded answer_event may not cite stale governed support because {reason}")

        access_decision_id = retrieval_response.get("access_decision_id") if retrieval_response else None
        access_decision = (
            answer_support_inventory["access_decisions"].get(access_decision_id)
            if isinstance(access_decision_id, str)
            else None
        )
        if restricted_policy_refs:
            if not access_decision:
                failures.append(
                    f"{path}: restricted governed support requires a resolvable access decision before answer rendering"
                )
            else:
                if access_decision.get("decision") != "allow":
                    failures.append(
                        f"{path}: restricted governed support requires an allow access decision before answer rendering"
                    )
                restricted_policy_refs.update(access_decision.get("source_policy_refs", set()))
                validate_access_basis(
                    path,
                    data.get("access_basis"),
                    restricted_policy_refs,
                    failures,
                    required_purpose_of_use=access_decision.get("purpose_of_use"),
                    required_access_decision_id=access_decision_id,
                )

    return failures


def main():
    failures = collect_failures()

    if failures:
        print("INTEGRITY VALIDATION FAILURES:")
        for failure in failures:
            print(failure)
        raise SystemExit(1)

    print("Integrity validation passed.")


if __name__ == "__main__":
    main()
