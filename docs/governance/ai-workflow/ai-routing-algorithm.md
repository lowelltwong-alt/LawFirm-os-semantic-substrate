# AI Routing Algorithm

The router classifies AI-assisted work before edits begin.

```text
Start
  -> read AGENTS.md, AI_START_HERE.md, AI_WORK_START_HERE.md
  -> confirm branch and scope are safe
  -> classify task type
  -> select mode: Explore / Plan / Edit / Execute
  -> select route from ai-task-route-table.yaml
  -> apply tool settings and stop conditions
  -> use route template
  -> edit only allowed paths
  -> validate
  -> open PR with routing impact statement
  -> decide whether router update is required
```

## Decision order

1. **Is the task runtime execution?** If yes, stop unless the route is `runtime_agent_planning` or another docs-only planning route. Runtime code belongs outside this repo unless explicitly authorized.
2. **Does the task change canonical authority?** If yes, use a promotion or governance route and require evidence, validation, and explicit authority.
3. **Does the task change schemas/contracts?** If yes, use `schema_change` or `contract_export_change`.
4. **Does the task touch Exceptions Lake runtime consumption?** If yes, use `exceptions_runtime_contract`.
5. **Does the task touch retrieval/access/answer evidence?** If yes, use `retrieval_access_contract`.
6. **Does the task add research or source synthesis?** If yes, use `research_addition` or `governance_bridge`.
7. **Does the task add or change audit capture?** If yes, use `ai_audit_design`.
8. **If no route fits, stop and report route gap.**

## Required output before editing

Every AI contributor must state:

- selected route
- selected mode
- allowed paths
- forbidden paths
- validation plan
- routing impact expectation

If this cannot be stated, the task is not ready for editing.
