# Entrypoint and Endpoint Map

## Human entrypoints

| Need | File |
|---|---|
| Start here for AI/human orientation | `AI_START_HERE.md` |
| Understand repo purpose and local checks | `README.md` |
| Understand agent rules | `AGENTS.md` |
| Understand Exceptions Lake boundary | `governance/EXCEPTIONS_LAKE_BOUNDARY.md` |
| Understand current readiness/non-claims | `reports/RELEASE_READINESS_AUDIT.md` |
| Understand current roadmap | `governance/CURRENT_STATE_AND_ROADMAP.md` |
| CINO brief | `docs/CINO_EXECUTIVE_BRIEF.md` |
| Automation manager starter pack | `docs/AUTOMATION_MANAGER_STARTER_PACK.md` |

## Machine/authority entrypoints

| Need | File |
|---|---|
| Source of truth and precedence | `registry/source-of-truth.json` |
| Design authority | `registry/design-authority.json` |
| Active schema registry | `registry/schema-registry.json` |
| Object prefixes | `registry/object_prefix_registry.json` |
| Canonical schema manifest | `governance/canonical_spine_manifest.json` |
| Drift check | `scripts/check_repo_drift.py` |
| Registry refs check | `scripts/check_registry_refs.py` |
| Full audit | `scripts/run_full_audit.sh` |

## Validation command map

| Check | Command | Expected current behavior |
|---|---|---|
| Unit tests | `python -m unittest discover -s scripts/validation/tests -p 'test_*.py'` | Pass. |
| Pytest suite | `python scripts/run_full_pytest.py` | Pass under `config/validation-runtime-policy.yaml`; direct pytest is blocked to preserve the 900 second minimum ceiling. |
| Drift check | `python scripts/check_repo_drift.py` | Pass; may write generated report. |
| Registry refs | `python scripts/check_registry_refs.py` | Pass. |
| Examples registry | `python scripts/validate_examples_registry.py` | Pass. |
| Integrity | `python scripts/validate_integrity.py` | Pass. |
| Source ingestion manifests | `python scripts/validation/validate_source_ingestion_manifests.py` | Pass. |
| Source-of-truth coherence | `python scripts/validation/validate_source_of_truth_coherence.py` | Pass. |
| Learning-loop transitions | `python scripts/validation/validate_learning_loop_transitions.py` | Pass. |
| Canonical grounding chain | `python scripts/validation/validate_canonical_grounding_chain.py` | Pass. |
| SHACL runner | `python scripts/validation/run_shacl.py` | Fail closed truthfully; conformance not currently claimed. |
| Full audit | `bash scripts/run_full_audit.sh` | Pass earlier stages, then stop at known truthful SHACL fail-closed gate. |

## Concept map

```text
source-ingestion-manifest
  -> governed source readiness
  -> claim / answer evidence
  -> fail-closed grounding
  -> sensitivity / allowed-use gate
  -> grounded evaluation readiness

exception-event
  -> pressure-vector
  -> adaptation-proposal
  -> promotion-decision

exception-event
  -> pressure-vector
  -> opportunity-object
  -> sprint-object or pilot-object
  -> validation-gate-record
  -> scale-package-object
  -> promotion-decision
```

## Boundary map

| Belongs here | Does not belong here |
|---|---|
| schemas | production event storage |
| registries | real internal documents |
| validators | vector indexes |
| synthetic examples | answer caches |
| doctrine | production dashboards |
| source-ingestion metadata contracts | runtime telemetry lake |
| evaluation readiness | production retrieval metrics |
| Exceptions Lake contract boundary | real Exceptions Lake runtime |
