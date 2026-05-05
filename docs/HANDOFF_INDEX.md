# Law Firm Handoff Index

## Purpose

This index orients executives, automation leaders, engineers, and coding agents to the LawFirm OS Semantic Substrate repository.

The repository is a governed semantic-governance substrate and contract repository for the Innovation OS. It defines meaning, evidence structure, validation gates, provenance, source-ingestion boundaries, fail-closed answer behavior, sensitivity and allowed-use gates, grounded evaluation readiness, and the Exceptions Lake contract boundary.

It is not a production runtime, internal document corpus, vector index, answer cache, production Exceptions Lake, or dashboard system.

## Start here by role

| Role | Start with | Then read | Outcome |
|---|---|---|---|
| CINO / executive sponsor | `docs/CINO_EXECUTIVE_BRIEF.md` | `reports/RELEASE_READINESS_AUDIT.md`, `governance/CURRENT_STATE_AND_ROADMAP.md` | Understand current guarantees, non-claims, and next operating steps. |
| Automation manager | `docs/AUTOMATION_MANAGER_STARTER_PACK.md` | `docs/ENTRYPOINT_AND_ENDPOINT_MAP.md`, `governance/EXCEPTIONS_LAKE_BOUNDARY.md` | Turn automation requests into governed exception/opportunity/sprint candidates. |
| Future runtime implementer | `docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md` | `docs/EXCEPTIONS_LAKE_CONTRACT_CONSUMPTION_MAP.md`, `docs/EXCEPTIONS_LAKE_RUNTIME_REPO_SKELETON.md`, `governance/EXCEPTIONS_LAKE_BOUNDARY.md` | Plan a separate runtime that consumes Law Firm contracts without redefining canon. |
| Coding agent / AI assistant | `AI_START_HERE.md` | `AGENTS.md`, `governance/EXCEPTIONS_LAKE_BOUNDARY.md`, `registry/source-of-truth.json` | Make narrow, validated changes without hallucinating or creating runtime drift. |
| Engineer / repo maintainer | `README.md` | `docs/ENTRYPOINT_AND_ENDPOINT_MAP.md`, `scripts/run_full_audit.sh`, `registry/schema-registry.json` | Run validations, understand contracts, and preserve current boundaries. |
| Reviewer / auditor | `reports/RELEASE_READINESS_AUDIT.md` | `governance/ALIGNMENT_SCOREBOARD.md`, `docs/REPO_ORIENTATION_GUIDE.md` | Verify what the repo can and cannot currently claim. |

## Repository truth hierarchy

When documents conflict, resolve in this order:

1. `registry/source-of-truth.json`
2. `registry/design-authority.json`
3. validated operational files, including `registry/schema-registry.json`, validation scripts, and canonical examples
4. governance docs and roadmap docs
5. reports and generated outputs
6. archive and legacy materials, which are historical unless explicitly cited by an authority surface

## Current state in one paragraph

Current `main` has a healthy focused validation posture. Unit tests and focused validators pass. `bash scripts/run_full_audit.sh` is expected to pass earlier stages and then stop only at the known truthful SHACL fail-closed gate. Core SHACL conformance for `shapes/core.ttl` against `shapes/core.shacl.ttl` is not currently claimed. The repo has readiness infrastructure, not production corpus performance.

## Current non-claims

The repository does not currently claim:

- internal corpus ingestion
- firm-knowledge completeness
- production retrieval accuracy, precision, recall, or coverage
- production answer quality
- production runtime Exceptions Lake deployment
- production-safe autonomous runtime behavior
- green SHACL conformance for the current core SHACL pair

## Suggested first questions

Ask a coding agent or reviewer:

- What is this repository?
- What does this repo currently guarantee?
- What does it intentionally not claim?
- Show me the contract surfaces and authority hierarchy.
- Map the path from exception-event to promotion-decision.
- Show which validations should pass and which SHACL boundary is expected to fail closed.
- Explain how an automation candidate becomes an opportunity, sprint, validation gate, and scale package.
- Explain what belongs in this repo versus a future runtime Exceptions Lake implementation.
- Show me the synthetic insurance-defense budget learning loop POC, exact template row map, `view-budget-workbook-v1` draft contract, and expected review-path mappings.
