# Endpoints And Commands

This repo is the control-plane authority surface. It publishes schemas, registries, and policies. It does not expose production runtime endpoints.

## Local Validation Commands

```bash
python -m unittest discover -s scripts/validation/tests -p 'test_*.py'
python scripts/run_full_pytest.py
python scripts/check_repo_drift.py
python scripts/validate_examples.py
```

Pytest must use `config/validation-runtime-policy.yaml` through `python scripts/run_full_pytest.py`; direct pytest is blocked to preserve the 900 second minimum ceiling for full and focused test runs.

Optional full audit:

```bash
bash scripts/run_full_audit.sh
```

If the full audit stops at the known truthful SHACL fail-closed gate, report that explicitly and confirm no earlier validation stage failed.

## Phase 2 Published Surfaces

Control-plane registries:

- `registry/innovation-object-registry.json`
- `registry/autonomy-lane-registry.json`
- `registry/assumption-watch-registry.json`
- `registry/harness-policy-registry.json`
- `registry/red-flag-trigger-registry.json`
- `registry/research-signal-registry.json`
- `registry/prompt-registry.json`
- `registry/tool-authority-registry.json`
- `registry/endpoint-authority-registry.json`
- `registry/agent-hostile-control-registry.json`
- `registry/agent-control-contract-export.json`

Phase 2 schema directories:

- `schemas/autonomy/`
- `schemas/harness/`
- `schemas/research/`
- `schemas/innovation/`

## PR-09 Architecture Sync Gate

```bash
python scripts/validate_architecture_object_coverage.py --workspace ..
```

Fails closed when a governed spine object drifts across schema registry, architecture-flow registry, AI docs, contract exports, or actionable command maps.

## Cross-Repo CLI Surfaces (synthetic / local only)

Legal Knowledge Runtime (`lawfirm-os-legal-knowledge`):

- `ingest-preflight` — emits SourceRef / coverage / anomaly checks on synthetic manifests
- `assemble-bundle` — emits PassageRef-backed `controlling_span_refs`, `passage_ref`, and retrieval trace refs

Skills Registry (`lawfirm-os-skills`):

- `skill-qa` — Skill QA report (trust surface + freshness + authority scan)
- `emit-trust-record` — SkillTrustRecord / `skill_trust_record` emission
- `trust-surface-diff` — trust surface change detection (human approval when required)
- `approve-skill --trust-record` — approval gate requiring SkillTrustRecord

Orchestrator:

- `preflight-execution` — ExecutionPassport / authority chain (EvidencePacket v2 consumer)

Exception Lake:

- `tests/test_central_admission.py` / `admit_dry_run` — EvidencePacket v2 admission; ExceptionLakeAdmissionRecord (PR-06 central admission)

## Consumer Responsibilities

Orchestrator and Exception Lake consumers may read these files to validate and route proposal-only operating objects. They must not mutate this repo at runtime and must not treat evidence objects as canonical promotion authority.

## Agent-Hostile Control Surfaces

- `classify-exception` - synthetic/local Orchestrator command surface governed by agent identity, prompt, tool, endpoint, and revocation contracts.
- `registry/endpoint-authority-registry.json` - canonical endpoint authority entry for the local classify-exception surface.
- `governance/AGENT_HOSTILE_CONTROL_BOUNDARY.md` - runtime-control boundary for identity, prompt, tool, endpoint, and revocation policy meaning.
