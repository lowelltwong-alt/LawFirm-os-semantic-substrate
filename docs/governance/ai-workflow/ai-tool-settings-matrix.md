# AI Tool Settings Matrix

Recommended settings are route defaults, not permission grants. Repository authority surfaces still govern.

| Route | Reasoning | Internet | Permissions | Default mode |
|---|---|---|---|---|
| research_addition | medium | off unless source verification needed | conservative | Edit |
| governance_bridge | high | off unless official docs needed | conservative | Plan/Edit |
| schema_change | high | off | conservative | Plan/Edit |
| contract_export_change | high | off | conservative | Plan/Edit |
| exceptions_runtime_contract | high | off | conservative | Plan/Edit |
| retrieval_access_contract | high | off | conservative | Plan/Edit |
| adapter_profile | medium | off unless official vendor docs needed | conservative | Edit |
| validation_infra | high | off | conservative | Plan/Edit |
| runtime_agent_planning | high | off unless official docs needed | conservative | Plan |
| ai_audit_design | high | off unless official governance docs needed | conservative | Plan/Edit |
| chat_handoff | medium | off | conservative | Plan/Edit |

## Tool rules

- Prefer read-only inspection before edits.
- Use the minimum context required.
- Do not use internet unless the selected route permits it.
- Do not use leaked code, private prompts, or leak-derived repositories.
- Never widen tool scope inside the task.
- Stop if a tool would create a runtime, connector, audit lake, transcript store, or production persistence surface in this repo.
