# Agent Operating Contract

This repository may be edited by coding agents, but agents operate under the same governance and mutation-boundary rules as human contributors.

## Required AI entry behavior

Before making changes in this repository, read:

1. `AI_WORK_START_HERE.md`
2. `registry/ai-front-door-registry.json`
3. `governance/AI_FRONT_DOOR_BOUNDARY.md`

This repository is one component of the LawFirm OS multi-repo kernel. Do not treat it as standalone.

## Boundary rule

This repository owns canonical schemas, registries, governance doctrine, published route and event authority (as defined here), and the machine-readable AI front door (`registry/ai-front-door-registry.json`). Runtime and skill repos consume these artifacts read-only unless a governed migration says otherwise. Do not duplicate canonical authority in sibling repos without an explicit compatibility plan.

## Required validation

Before reporting success, run `python -m pytest -q` in this repository and the AI front-door integrity gate: `python scripts/validate_ai_front_door.py` (from this repo root; optional `--substrate-root` if invoked from elsewhere).

## Read order

Before editing, read:

1. `AI_START_HERE.md`
2. `registry/source-of-truth.json`
3. `registry/design-authority.json`
4. `governance/AI_CONTROL_PLANE_BOUNDARY.md`
5. `governance/EXCEPTIONS_LAKE_BOUNDARY.md` if present
6. relevant schemas, validators, examples, and governance docs for the task

## Operating rules

Agents must:

- inventory before editing
- keep PRs narrow
- use existing authority surfaces before creating new ones
- preserve the distinction between canonical, operational, AI control plane, reference, derived, legacy, and archive surfaces
- run the validation commands requested in the task
- report exact validation results
- stop and report unresolved governance conflicts instead of guessing
- preserve the Phase 2 rule: risk color controls authority, hardness controls harness depth, and leverage controls priority
- use `registry/` as the canonical discovery surface for Phase 2 schemas and policies
- keep existing root-level Innovation OS schemas in place unless a separate compatibility-preserving migration is approved

Agents must not:

- invent internal documents, facts, clients, matters, employees, policies, or source content
- ingest real internal records
- create runtime storage, telemetry lakes, dashboards, or production pipelines in this repo
- bypass validators
- convert failures into silent skips
- treat adapter files as semantic authority
- treat examples, reports, data, graphs, archive, or legacy files as canonical truth unless an authority surface says so
- create grouped duplicate schemas for existing root-level Innovation OS schemas
- create or restore green authority without human approval
- let hardness or leverage override red/yellow/green authority
- add live research crawling, external API calls, external writes, or production automation as part of Phase 2 scaffolding

## Agent findings as exception candidates

Agent review findings, failed validators, stale docs, unsupported claims, retrieval misses, access denials, and hallucinated or overbroad fixes are exception candidates.

They may become governed learning signals through:

```text
exception-event → pressure-vector → adaptation-proposal → promotion-decision
```

They may not directly mutate canonical ontology, schemas, registries, or governance policy.

## Validation posture

At minimum, agents should run the task-specific validation commands.

Common checks include:

```bash
python -m unittest discover -s scripts/validation/tests -p 'test_*.py'
python scripts/check_repo_drift.py
bash scripts/run_full_audit.sh
```

If the full audit stops at the known truthful SHACL fail-closed gate, report that explicitly and confirm no earlier validation stage failed.
