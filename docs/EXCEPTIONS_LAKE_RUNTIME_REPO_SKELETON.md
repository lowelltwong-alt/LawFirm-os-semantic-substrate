# Exceptions Lake Runtime Repo Skeleton

## Purpose

This is a recommended structure for a future separate runtime repository.

It is not a proposal to build runtime behavior inside this contract repo.
Its purpose is to show how a future operational implementation can consume Law Firm
contracts without redefining them.

## Suggested Separate Runtime Repo Layout

```text
exceptions-lake-runtime/
  connectors/
  contract_loader/
  event_ingestion/
  event_store/
  validation_gateway/
  policy_gateway/
  approval_queue/
  exception_queue/
  telemetry/
  dashboards/
  exports/
  tests/
  deployment/
```

## Folder Responsibilities

| Folder | Purpose | Repo contract it consumes | What it must not redefine |
|---|---|---|---|
| `connectors/` | Source-system adapters for runtime observations, access denials, and retrieval misses. | `schemas/exception-event.schema.json`<br>`registry/exception-route-registry.json`<br>`governance/RETRIEVAL_ARCHITECTURE.md` | Canonical event meaning, route semantics, or policy posture |
| `contract_loader/` | Pin and load versioned contracts from this repo by tag, commit, or release snapshot. | `registry/source-of-truth.json`<br>`registry/design-authority.json`<br>`registry/schema-registry.json`<br>`registry/exceptions-lake-contract-export.json` | Source-of-truth precedence or design-authority precedence |
| `event_ingestion/` | Normalize raw runtime observations into governed exception candidates. | `schemas/exception-event.schema.json`<br>`registry/exceptions-schema-registry.json` | Exception schema fields, lifecycle rules, or mutation controls |
| `event_store/` | Persist real runtime events outside this repo with retention and audit controls. | `governance/EXCEPTIONS_LAKE_BOUNDARY.md`<br>`docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md` | Any claim that runtime storage belongs in the contract repo |
| `validation_gateway/` | Enforce contract validation before events progress to pressure, opportunity, or approval paths. | `scripts/validation/validate_exception_events.py`<br>`scripts/validation/validate_exception_governance.py`<br>`scripts/validation/validate_learning_loop_transitions.py` | Validator rules, schema semantics, or promotion criteria |
| `policy_gateway/` | Apply live access and allowed-use enforcement in runtime execution. | `schemas/access-decision.schema.json`<br>`governance/RETRIEVAL_ARCHITECTURE.md` | Access semantics, deny-by-default posture, or policy meaning |
| `approval_queue/` | Hold reviewed adaptation proposals, pilot approvals, and promotion packages for human decisions. | `schemas/adaptation-proposal.schema.json`<br>`schemas/promotion-decision.schema.json`<br>`schemas/validation-gate-record.schema.json` | Review roles, approval states, or promotion authority |
| `exception_queue/` | Operate triage and follow-on work queues for reviewed exception candidates. | `schemas/pressure-vector.schema.json`<br>`schemas/opportunity-object.schema.json`<br>`schemas/sprint-object.schema.json` | Pressure semantics, opportunity scoring rules, or sprint/pilot mutation boundaries |
| `telemetry/` | Emit runtime metrics, traces, and audit observations about processing behavior. | `governance/AI_CONTROL_PLANE_BOUNDARY.md`<br>`governance/EXCEPTIONS_LAKE_BOUNDARY.md` | Semantic truth, canonical evidence, or promotion authority |
| `dashboards/` | Present derived operational monitoring and queue views. | `schemas/view-executive-brief.schema.json`<br>`docs/EXCEPTIONS_LAKE_CONTRACT_CONSUMPTION_MAP.md` | Executive-brief meaning, canonical status, or promotion decisions |
| `exports/` | Publish metadata-only handoff packs and release exports for runtime consumers. | `registry/exceptions-lake-contract-export.json`<br>`scripts/build_release_snapshots.py` | Schema meaning, lifecycle authority, or runtime deployment truth |
| `tests/` | Validate contract loading, queue behavior, and runtime adapters against pinned Law Firm contracts. | `python -m unittest discover -s scripts/validation/tests -p 'test_*.py'`<br>Law Firm validators listed in the export manifest | Any local test shortcut that weakens Law Firm validator behavior |
| `deployment/` | Manage infrastructure-as-code, secrets wiring, environment config, and operational rollout. | `docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md`<br>`governance/CURRENT_STATE_AND_ROADMAP.md` | Contract meaning, schema authority, or governance policy |

## Runtime Repo Rules

- The runtime repo should pin a version of this repo before loading contracts.
- The runtime repo should treat Law Firm validators as boundary checks, not advisory
  suggestions.
- The runtime repo may store real events, queues, telemetry, and dashboards.
- The runtime repo may not redefine Law Firm schema meaning or promotion authority.
- Runtime observations may become exception candidates, but they may not write
  directly into canonical ontology, schema, registry, or governance surfaces.
