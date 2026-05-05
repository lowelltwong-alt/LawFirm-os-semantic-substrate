# AI Routing Update Policy

The AI router is a living control-plane artifact. Any PR that changes how AI work should be classified, validated, governed, audited, or stopped must update this router or explicitly create a follow-up item.

## Mandatory path triggers

Review routing impact when a PR changes:

- `AGENTS.md`
- `AI_START_HERE.md`
- `AI_WORK_START_HERE.md`
- `governance/**`
- `registry/**`
- `schemas/**`
- `shapes/**`
- `scripts/**`
- `.github/**`
- `docs/governance/**`
- `docs/EXCEPTIONS_LAKE_RUNTIME_BUILD_PACK.md`
- `docs/EXCEPTIONS_LAKE_CONTRACT_CONSUMPTION_MAP.md`
- `profiles/**`
- `mappings/**`
- `examples/**`

## Mandatory semantic triggers

Review routing impact when a PR introduces or changes:

- trust zone
- lifecycle status
- source type
- source ingestion policy
- validation rule
- schema
- runtime contract
- action type
- adapter profile
- route or template
- AI tool setting
- internet-use rule
- clean-room or source boundary
- audit-capture requirement
- retention rule
- transcript storage behavior
- PR governance requirement
- branch protection or CODEOWNERS policy
- Exceptions Lake, retrieval, access, evidence, governance, schema, audit, or runtime workflow

## Required PR statement

Every AI-assisted PR should answer:

```markdown
## AI routing impact

Does this PR change AI work routing, templates, validation expectations, stop conditions, route ownership, or AI tool settings?

- [ ] No
- [ ] Yes  -  updated AI_WORK_START_HERE.md / ai-task-route-table.yaml / relevant template
- [ ] Yes  -  follow-up PR required
```

If the contributor cannot answer this, the PR is not ready for review.
