# AGENTS.md

<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->
Managed bootstrap for the LawFirm OS Skill-Agent Control Plane. This block adds cross-repo routing context; it must not replace the repo-specific instructions preserved below.

Before making changes in this repository, read:

1. AI_WORK_START_HERE.md
2. skill-agent-manifest.json
3. ../LawFirm-os-semantic-substrate/registry/ai-front-door-registry.json, or registry/ai-front-door-registry.json when already in Semantic Substrate
4. ../LawFirm-os-semantic-substrate/registry/skill-agent-control-plane-registry.json, or registry/skill-agent-control-plane-registry.json when already in Semantic Substrate
5. ../LawFirm-os-semantic-substrate/governance/SKILL_AGENT_CONTROL_PLANE_BOUNDARY.md, or local governance/SKILL_AGENT_CONTROL_PLANE_BOUNDARY.md in Semantic Substrate

Repo: LawFirm-os-semantic-substrate
Plane: semantic substrate / control plane
Repo purpose: Canonical schemas, registries, governance, AI front door, lifecycle policy, schema registry, repo registry, skill-agent graph, and workspace validators.
This repo must not own: Runtime observations, model execution, raw legal payload storage.

Preservation rule: keep the REPO_SPECIFIC_INSTRUCTIONS section intact unless a human explicitly approves removal. New bootstrap text should be merged around repo-specific doctrine, not overwrite it.
<!-- END LAWFIRM_OS_BOOTSTRAP -->

<!-- BEGIN REPO_SPECIFIC_INSTRUCTIONS -->
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

Before reporting success, run `python scripts/run_full_pytest.py` in this repository and the AI front-door integrity gate: `python scripts/validate_ai_front_door.py` (from this repo root; optional `--substrate-root` if invoked from elsewhere). Full and focused pytest must use `config/validation-runtime-policy.yaml`; direct `python -m pytest` is blocked so validation does not inherit a short 300 second ceiling.

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
exception-event â†’ pressure-vector â†’ adaptation-proposal â†’ promotion-decision
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

<!-- END REPO_SPECIFIC_INSTRUCTIONS -->

## Skill-Agent Control Plane References

- skill-agent-manifest.json
- Semantic Substrate registry/skill-agent-control-plane-registry.json
- Semantic Substrate registry/skill-agent-graph-index.json
- Semantic Substrate registry/lawfirm-os-repo-registry.json
- Semantic Substrate governance/SKILL_AGENT_CONTROL_PLANE_BOUNDARY.md
- Semantic Substrate governance/SKILL_AGENT_LIFECYCLE_AND_RECURSIVE_IMPROVEMENT.md

## Validation Commands

    python scripts/validate_ai_front_door.py
    python scripts/validate_skill_agent_control_plane.py --workspace ..
    python scripts/validate_managed_patch_preservation.py --workspace ..
    python scripts/run_full_pytest.py

## AI Strategy Doctrine and Context Quality Governance

- [governance/AI_STRATEGY_DOCTRINE.md](governance/AI_STRATEGY_DOCTRINE.md) is the proposed controlling doctrine for vendor-agnostic AI strategy, proprietary context, decision models, Legal Context Bundles, Evidence Packets, model/provider adapters, skill trust records, and governed promotion paths.
- [governance/STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md](governance/STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md) is a strategy reference, not an implementation mandate.
- [governance/SHANNON_INFORMATION_THEORY_CROSSWALK.md](governance/SHANNON_INFORMATION_THEORY_CROSSWALK.md) is a technical crosswalk and must not be used as legal-truth math.
- [governance/CONTEXT_QUALITY_DOCTRINE.md](governance/CONTEXT_QUALITY_DOCTRINE.md) defines Legal Context Bundles and context-quality controls.
- [governance/INSTITUTIONAL_KNOWLEDGE_ENCODING_STANDARD.md](governance/INSTITUTIONAL_KNOWLEDGE_ENCODING_STANDARD.md) defines how institutional knowledge must be scoped, sourced, reviewed, and governed.
- None of these files are canon until approved through this repo's governance process.
