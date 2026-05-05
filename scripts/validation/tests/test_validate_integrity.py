from __future__ import annotations

from copy import deepcopy
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_integrity


class ValidateIntegrityTests(unittest.TestCase):
    def test_duplicate_active_claim_ids_and_dangling_refs_fail(self) -> None:
        address_struct = {
            "environment": "example",
            "authority_zone": "public",
            "layer": "governance",
            "domain": "legal",
            "module": "intake_conflicts",
            "version": "v1",
        }

        examples = [
            (
                "examples/claims/CLM-000101.json",
                {
                    "claim_id": "CLM-000101",
                    "schema_id": "claim-schema-v2",
                    "template_id": "claim-template-v2",
                    "authority_zone": "public",
                    "source_refs": ["SRC-000100"],
                    "evidence_refs": ["CHK-000100"],
                    "artifact_refs": ["ART-000001"],
                    "address_struct": {
                        **address_struct,
                        "object_type": "claim",
                        "object_id": "CLM-000101",
                    },
                },
            ),
            (
                "examples/claims/CLM-000101.v3.json",
                {
                    "claim_id": "CLM-000101",
                    "schema_type": "claim",
                    "schema_version": "v3",
                    "authority_zone": "public",
                    "artifact_refs": ["ART-000001"],
                    "address_struct": {
                        **address_struct,
                        "object_type": "claim",
                        "object_id": "CLM-000101",
                    },
                },
            ),
            (
                "examples/artifacts/ART-000001.json",
                {
                    "id": "ART-000001",
                    "schema_id": "artifact-schema-v1",
                    "template_id": "artifact-template-v1",
                    "artifact_type": "framework",
                    "authority_zone": "public",
                    "attribution_chain": {"primary_sources": ["SRC-000100"]},
                    "address_struct": {
                        **address_struct,
                        "object_type": "artifact",
                        "object_id": "ART-000001",
                    },
                },
            ),
        ]

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=examples),
            patch.object(validate_integrity, "active_examples", return_value=examples),
            patch.object(
                validate_integrity,
                "load_schema_registry",
                return_value={
                    "claim-schema-v2": {"applies_to": ["claim"]},
                    "artifact-schema-v1": {"applies_to": ["artifact"]},
                },
            ),
            patch.object(
                validate_integrity,
                "load_template_registry",
                return_value={
                    "claim-template-v2": {
                        "applies_to": ["claim"],
                        "required_metadata_fields": ["authority_zone"],
                    },
                    "artifact-template-v1": {
                        "applies_to": ["artifact"],
                        "required_metadata_fields": ["authority_zone", "artifact_type"],
                    },
                },
            ),
            patch.object(
                validate_integrity,
                "load_object_prefixes",
                return_value={"CLM": "claim", "ART": "artifact", "CHK": "chunk"},
            ),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertIn("duplicate claim identifier 'CLM-000101'", joined)
        self.assertIn(
            "source_ref 'SRC-000100' does not resolve to an active example object",
            joined,
        )
        self.assertIn(
            "evidence_ref 'CHK-000100' does not resolve to an active example object",
            joined,
        )
        self.assertIn(
            "attribution_chain.primary_source 'SRC-000100' does not resolve to an active example object",
            joined,
        )

    def test_source_ref_can_resolve_through_address_struct_object_id(self) -> None:
        address_struct = {
            "environment": "example",
            "authority_zone": "internal_general",
            "layer": "data",
            "domain": "legal",
            "module": "documents",
            "version": "v1",
        }

        examples = [
            (
                "examples/claims/CLM-000101.v3.json",
                {
                    "claim_id": "CLM-000101",
                    "schema_type": "claim",
                    "schema_version": "v3",
                    "authority_zone": "public",
                    "source_refs": ["SRC-doc-000001"],
                    "evidence_refs": ["CHK-000001"],
                    "artifact_refs": ["ART-000001"],
                    "access_basis": {
                        "purpose_of_use": "synthetic_test_review",
                        "source_policy_refs": ["policy:synthetic-doc-read"],
                    },
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "public",
                        "layer": "governance",
                        "domain": "legal",
                        "module": "intake_conflicts",
                        "object_type": "claim",
                        "object_id": "CLM-000101",
                        "version": "v3",
                    },
                },
            ),
            (
                "examples/artifacts/ART-000001.json",
                {
                    "id": "ART-000001",
                    "schema_id": "artifact-schema-v1",
                    "template_id": "artifact-template-v1",
                    "artifact_type": "framework",
                    "authority_zone": "public",
                    "attribution_chain": {"primary_sources": ["SRC-doc-000001"]},
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "public",
                        "layer": "governance",
                        "domain": "legal",
                        "module": "intake_conflicts",
                        "object_type": "artifact",
                        "object_id": "ART-000001",
                        "version": "v1",
                    },
                },
            ),
            (
                "examples/documents/DOC-000001.json",
                {
                    "document_id": "DOC-000001",
                    "schema_type": "document",
                    "schema_version": "v1",
                    "access_policy_ref": "policy:synthetic-doc-read",
                    "canonical_status": "active",
                    "address_struct": {
                        **address_struct,
                        "object_type": "source",
                        "object_id": "SRC-doc-000001",
                    },
                },
            ),
            (
                "examples/documents/CHK-000001.json",
                {
                    "chunk_id": "CHK-000001",
                    "schema_type": "chunk",
                    "schema_version": "v1",
                    "address_struct": {
                        **address_struct,
                        "object_type": "chunk",
                        "object_id": "CHK-000001",
                    },
                },
            ),
        ]

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=examples[:2]),
            patch.object(validate_integrity, "active_examples", return_value=examples),
            patch.object(
                validate_integrity,
                "load_schema_registry",
                return_value={
                    "artifact-schema-v1": {"applies_to": ["artifact"]},
                },
            ),
            patch.object(
                validate_integrity,
                "load_template_registry",
                return_value={
                    "artifact-template-v1": {
                        "applies_to": ["artifact"],
                        "required_metadata_fields": ["authority_zone", "artifact_type"],
                    },
                },
            ),
            patch.object(
                validate_integrity,
                "load_object_prefixes",
                return_value={"CLM": "claim", "ART": "artifact", "CHK": "chunk"},
            ),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertNotIn("SRC-doc-000001", joined)
        self.assertNotIn("CHK-000001", joined)

    def test_substantive_claim_without_grounding_fails_closed(self) -> None:
        examples = [
            (
                "examples/claims/CLM-999999.v3.json",
                {
                    "claim_id": "CLM-999999",
                    "schema_type": "claim",
                    "schema_version": "v3",
                    "authority_zone": "public",
                    "subject": "internal_client",
                    "predicate": "has_policy",
                    "object": "special_billing_rule",
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "public",
                        "layer": "governance",
                        "domain": "legal",
                        "module": "intake_conflicts",
                        "object_type": "claim",
                        "object_id": "CLM-999999",
                        "version": "v3",
                    },
                },
            )
        ]

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=examples),
            patch.object(validate_integrity, "active_examples", return_value=examples),
            patch.object(validate_integrity, "answer_examples", return_value=[]),
            patch.object(validate_integrity, "load_answer_support_inventory", return_value={"retrieval_responses": {}, "answer_evidence": {}, "access_decisions": {}}),
            patch.object(validate_integrity, "build_governed_source_inventory", return_value={"source_refs": {}, "document_versions": {}}),
            patch.object(validate_integrity, "load_schema_registry", return_value={}),
            patch.object(validate_integrity, "load_template_registry", return_value={}),
            patch.object(validate_integrity, "load_object_prefixes", return_value={"CLM": "claim"}),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertIn("requires at least one source_ref", joined)
        self.assertIn("requires at least one evidence_ref", joined)

    def test_grounded_answer_event_cannot_self_satisfy_retrieval_support(self) -> None:
        answer_event = (
            "examples/answer-events/AE-999999.json",
            {
                "answer_event_id": "AE-999999",
                "schema_type": "answer-event",
                "schema_version": "v1",
                "grounding_status": "grounded",
                "retrieval_response_id": "RR-999999",
                "answer_evidence_ids": ["AEV-123456"],
                "address_struct": {
                    "environment": "example",
                    "authority_zone": "internal_general",
                    "layer": "retrieval",
                    "domain": "legal",
                    "module": "answer_events",
                    "object_type": "artifact",
                    "object_id": "ART-ae-999999",
                    "version": "v1",
                },
            },
        )

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=[]),
            patch.object(validate_integrity, "active_examples", return_value=[answer_event]),
            patch.object(validate_integrity, "answer_examples", return_value=[answer_event]),
            patch.object(
                validate_integrity,
                "load_answer_support_inventory",
                return_value={"retrieval_responses": {}, "answer_evidence": {"AEV-123456": {"document_version_id": "DV-123456"}}, "access_decisions": {}},
            ),
            patch.object(validate_integrity, "build_governed_source_inventory", return_value={"source_refs": {}, "document_versions": {}}),
            patch.object(validate_integrity, "load_schema_registry", return_value={}),
            patch.object(validate_integrity, "load_template_registry", return_value={}),
            patch.object(validate_integrity, "load_object_prefixes", return_value={}),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertIn(
            "retrieval_response_id 'RR-999999' does not resolve to grounded support",
            joined,
        )

    def test_restricted_claim_without_access_basis_fails(self) -> None:
        claim = (
            "examples/claims/CLM-777777.v3.json",
            {
                "claim_id": "CLM-777777",
                "schema_type": "claim",
                "schema_version": "v3",
                "authority_zone": "public",
                "subject": "matter_document",
                "predicate": "supports",
                "object": "billing_position",
                "source_refs": ["SRC-777777"],
                "evidence_refs": ["CHK-777777"],
                "address_struct": {
                    "environment": "example",
                    "authority_zone": "public",
                    "layer": "governance",
                    "domain": "legal",
                    "module": "claims",
                    "object_type": "claim",
                    "object_id": "CLM-777777",
                    "version": "v3",
                },
            },
        )
        active_examples = [
            claim,
            (
                "examples/documents/DOC-777777.json",
                {
                    "document_id": "DOC-777777",
                    "schema_type": "document",
                    "schema_version": "v1",
                    "access_policy_ref": "policy:synthetic-restricted",
                    "canonical_status": "active",
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "restricted",
                        "layer": "data",
                        "domain": "legal",
                        "module": "documents",
                        "object_type": "source",
                        "object_id": "SRC-777777",
                        "version": "v1",
                    },
                },
            ),
            (
                "examples/documents/CHK-777777.json",
                {
                    "chunk_id": "CHK-777777",
                    "schema_type": "chunk",
                    "schema_version": "v1",
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "restricted",
                        "layer": "data",
                        "domain": "legal",
                        "module": "documents",
                        "object_type": "chunk",
                        "object_id": "CHK-777777",
                        "version": "v1",
                    },
                },
            ),
        ]

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=[claim]),
            patch.object(validate_integrity, "active_examples", return_value=active_examples),
            patch.object(validate_integrity, "answer_examples", return_value=[]),
            patch.object(validate_integrity, "load_answer_support_inventory", return_value={"retrieval_responses": {}, "answer_evidence": {}, "access_decisions": {}}),
            patch.object(
                validate_integrity,
                "build_governed_source_inventory",
                return_value={
                    "source_refs": {
                        "SRC-777777": {
                            "is_restricted": True,
                            "source_policy_refs": {"policy:synthetic-restricted"},
                            "stale_reason": None,
                        }
                    },
                    "document_versions": {},
                },
            ),
            patch.object(validate_integrity, "load_schema_registry", return_value={}),
            patch.object(validate_integrity, "load_template_registry", return_value={}),
            patch.object(validate_integrity, "load_object_prefixes", return_value={"CLM": "claim", "CHK": "chunk"}),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertIn("restricted governed support requires access_basis", joined)

    def test_restricted_claim_with_access_basis_passes(self) -> None:
        claim = (
            "examples/claims/CLM-888888.v3.json",
            {
                "claim_id": "CLM-888888",
                "schema_type": "claim",
                "schema_version": "v3",
                "authority_zone": "public",
                "subject": "matter_document",
                "predicate": "supports",
                "object": "billing_position",
                "source_refs": ["SRC-888888"],
                "evidence_refs": ["CHK-888888"],
                "access_basis": {
                    "purpose_of_use": "synthetic_test_review",
                    "source_policy_refs": ["policy:synthetic-restricted"],
                },
                "address_struct": {
                    "environment": "example",
                    "authority_zone": "public",
                    "layer": "governance",
                    "domain": "legal",
                    "module": "claims",
                    "object_type": "claim",
                    "object_id": "CLM-888888",
                    "version": "v3",
                },
            },
        )
        active_examples = [
            claim,
            (
                "examples/documents/DOC-888888.json",
                {
                    "document_id": "DOC-888888",
                    "schema_type": "document",
                    "schema_version": "v1",
                    "access_policy_ref": "policy:synthetic-restricted",
                    "canonical_status": "active",
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "restricted",
                        "layer": "data",
                        "domain": "legal",
                        "module": "documents",
                        "object_type": "source",
                        "object_id": "SRC-888888",
                        "version": "v1",
                    },
                },
            ),
            (
                "examples/documents/CHK-888888.json",
                {
                    "chunk_id": "CHK-888888",
                    "schema_type": "chunk",
                    "schema_version": "v1",
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "restricted",
                        "layer": "data",
                        "domain": "legal",
                        "module": "documents",
                        "object_type": "chunk",
                        "object_id": "CHK-888888",
                        "version": "v1",
                    },
                },
            ),
        ]

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=[claim]),
            patch.object(validate_integrity, "active_examples", return_value=active_examples),
            patch.object(validate_integrity, "answer_examples", return_value=[]),
            patch.object(validate_integrity, "load_answer_support_inventory", return_value={"retrieval_responses": {}, "answer_evidence": {}, "access_decisions": {}}),
            patch.object(
                validate_integrity,
                "build_governed_source_inventory",
                return_value={
                    "source_refs": {
                        "SRC-888888": {
                            "is_restricted": True,
                            "source_policy_refs": {"policy:synthetic-restricted"},
                            "stale_reason": None,
                        }
                    },
                    "document_versions": {},
                },
            ),
            patch.object(validate_integrity, "load_schema_registry", return_value={}),
            patch.object(validate_integrity, "load_template_registry", return_value={}),
            patch.object(validate_integrity, "load_object_prefixes", return_value={"CLM": "claim", "CHK": "chunk"}),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertNotIn("restricted governed support requires access_basis", joined)

    def test_restricted_answer_without_access_basis_fails(self) -> None:
        answer_event = (
            "examples/answer-events/AE-777777.json",
            {
                "answer_event_id": "AE-777777",
                "schema_type": "answer-event",
                "schema_version": "v1",
                "grounding_status": "grounded",
                "retrieval_response_id": "RR-777777",
                "answer_evidence_ids": ["AEV-777777"],
                "address_struct": {
                    "environment": "example",
                    "authority_zone": "internal_general",
                    "layer": "retrieval",
                    "domain": "legal",
                    "module": "answer_events",
                    "object_type": "artifact",
                    "object_id": "ART-ae-777777",
                    "version": "v1",
                },
            },
        )

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=[]),
            patch.object(validate_integrity, "active_examples", return_value=[answer_event]),
            patch.object(validate_integrity, "answer_examples", return_value=[answer_event]),
            patch.object(
                validate_integrity,
                "load_answer_support_inventory",
                return_value={
                    "retrieval_responses": {"RR-777777": {"access_decision_id": "AD-777777"}},
                    "answer_evidence": {"AEV-777777": {"document_version_id": "DV-777777"}},
                    "access_decisions": {
                        "AD-777777": {
                            "decision": "allow",
                            "purpose_of_use": "synthetic_test_review",
                            "source_policy_refs": {"policy:synthetic-restricted"},
                            "confidentiality_class": "restricted",
                        }
                    },
                },
            ),
            patch.object(
                validate_integrity,
                "build_governed_source_inventory",
                return_value={
                    "source_refs": {},
                    "document_versions": {
                        "DV-777777": {
                            "is_restricted": True,
                            "source_policy_refs": {"policy:synthetic-restricted"},
                            "stale_reason": None,
                        }
                    },
                },
            ),
            patch.object(validate_integrity, "load_schema_registry", return_value={}),
            patch.object(validate_integrity, "load_template_registry", return_value={}),
            patch.object(validate_integrity, "load_object_prefixes", return_value={}),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertIn("restricted governed support requires access_basis", joined)

    def test_grounded_answer_with_stale_source_fails(self) -> None:
        answer_event = (
            "examples/answer-events/AE-888888.json",
            {
                "answer_event_id": "AE-888888",
                "schema_type": "answer-event",
                "schema_version": "v1",
                "grounding_status": "grounded",
                "retrieval_response_id": "RR-888888",
                "answer_evidence_ids": ["AEV-888888"],
                "access_basis": {
                    "access_decision_id": "AD-888888",
                    "purpose_of_use": "synthetic_test_review",
                    "source_policy_refs": ["policy:synthetic-restricted"],
                },
                "address_struct": {
                    "environment": "example",
                    "authority_zone": "internal_general",
                    "layer": "retrieval",
                    "domain": "legal",
                    "module": "answer_events",
                    "object_type": "artifact",
                    "object_id": "ART-ae-888888",
                    "version": "v1",
                },
            },
        )

        with (
            patch.object(validate_integrity, "canonical_examples", return_value=[]),
            patch.object(validate_integrity, "active_examples", return_value=[answer_event]),
            patch.object(validate_integrity, "answer_examples", return_value=[answer_event]),
            patch.object(
                validate_integrity,
                "load_answer_support_inventory",
                return_value={
                    "retrieval_responses": {"RR-888888": {"access_decision_id": "AD-888888"}},
                    "answer_evidence": {"AEV-888888": {"document_version_id": "DV-888888"}},
                    "access_decisions": {
                        "AD-888888": {
                            "decision": "allow",
                            "purpose_of_use": "synthetic_test_review",
                            "source_policy_refs": {"policy:synthetic-restricted"},
                            "confidentiality_class": "restricted",
                        }
                    },
                },
            ),
            patch.object(
                validate_integrity,
                "build_governed_source_inventory",
                return_value={
                    "source_refs": {},
                    "document_versions": {
                        "DV-888888": {
                            "is_restricted": True,
                            "source_policy_refs": {"policy:synthetic-restricted"},
                            "stale_reason": "document_version.status is superseded",
                        }
                    },
                },
            ),
            patch.object(validate_integrity, "load_schema_registry", return_value={}),
            patch.object(validate_integrity, "load_template_registry", return_value={}),
            patch.object(validate_integrity, "load_object_prefixes", return_value={}),
        ):
            failures = validate_integrity.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertIn("may not cite stale governed support", joined)


if __name__ == "__main__":
    unittest.main()
