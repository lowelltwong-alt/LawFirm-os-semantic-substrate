# Endpoints And Commands

This repo is the control-plane authority surface. It publishes schemas, registries, and policies. It does not expose production runtime endpoints.

## Local Validation Commands

```bash
python -m unittest discover -s scripts/validation/tests -p 'test_*.py'
python scripts/check_repo_drift.py
python scripts/validate_examples.py
```

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

Phase 2 schema directories:

- `schemas/autonomy/`
- `schemas/harness/`
- `schemas/research/`
- `schemas/innovation/`

## Consumer Responsibilities

Orchestrator and Exception Lake consumers may read these files to validate and route proposal-only operating objects. They must not mutate this repo at runtime and must not treat evidence objects as canonical promotion authority.
