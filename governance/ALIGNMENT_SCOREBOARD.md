# ALIGNMENT SCOREBOARD

Last updated: 2026-04-21
Purpose: record the current live repo state for active example canon, drift checks, and local validation commands.

## Current Gate Read

- Active example canon: aligned for the currently governed claim, artifact, and exception-learning chain.
- Repo drift gate: aligned; `.github/workflows/repo-drift-check.yml` now runs `python scripts/check_repo_drift.py` and uploads the generated report.
- Registry truthfulness: aligned for the active claim transition. `claim-schema-v3` is active, `claim-schema-v2` is deprecated, and no governed `templates/claim-template-v3.md` exists yet.
- Remaining governance gap to track explicitly: the repo still has only `claim-template-v2` and `artifact-template-v1` in `registry/template-registry.json`. A claim-v3 template should be documented as missing until it is intentionally created.

## Active Example Canon

| Surface | Live state |
| --- | --- |
| Active claim example | `examples/claims/CLM-000101.v3.json` |
| Deprecated v2 claim example | preserved only at `examples/claims/legacy/CLM-000101.v2.json` |
| Active artifact example | `examples/artifacts/ART-000001.json` with live `SRC-doc-000001` attribution |
| Active exception chain | `examples/exceptions/events/EXC-000101.json` -> `examples/exceptions/pressure-vectors/PV-000101.json` -> `examples/exceptions/adaptation-proposals/AP-000001.json` -> `examples/exceptions/promotion-decisions/PD-000001.json` |
| Archived standalone exception examples | `archive/examples/exceptions/retrieval_miss_example.json`, `archive/examples/exceptions/workflow_escalation_example.json`, `archive/examples/exceptions/authority_conflict_override_example.json` |

## Live Reference Truth

- Active claim and artifact refs resolve to live example identities:
  - `SRC-doc-000001`
  - `CHK-000001`
- Source-style identities may resolve through `address_struct.object_id` when the canonical example uses a source-facing object ID rather than a top-level `id` field.
- No new pressure vectors or replacement source objects were invented to clear broken historical examples.

## Current Validation Commands

These are the commands reviewers should run from a clean working tree:

```bash
python -m unittest discover -s scripts/validation/tests -p 'test_*.py'
python scripts/check_repo_drift.py
bash scripts/run_full_audit.sh
```

Expected current result:

- the focused unit-test and drift commands should pass on healthy `main`
- `bash scripts/run_full_audit.sh` should pass all earlier stages and then stop at the known truthful SHACL fail-closed gate
- that SHACL stop is expected because `shapes/core.ttl` is not yet a trustworthy same-namespace focus-node data graph for `shapes/core.shacl.ttl`
- no core SHACL conformance is currently claimed for that pair
- that SHACL stop is an explicit truthfulness boundary, not a green conformance signal
- no earlier validation stage should fail when the repo is healthy

## Explicit Truth Notes

- `CHANGELOG.md` exists in the repository root.
- `templates/claim-template-v3.md` does not exist and should not be claimed as present.
- The drift report is generated from live checks, not from a placeholder markdown artifact.
