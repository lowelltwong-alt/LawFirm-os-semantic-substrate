# AI Workflow Router

This folder defines the control-plane routing rules for AI-assisted work in the LawFirm OS semantic-governance substrate repository.

The router does not create runtime agents. It classifies work, selects a safe mode, assigns a route template, defines validation expectations, and forces every PR to consider whether the routing rules themselves need to change.

## Entry point

Start with `AI_WORK_START_HERE.md` at the repository root.

## Core files

- `ai-work-cycle.md`  -  universal AI work cycle.
- `ai-routing-algorithm.md`  -  route decision tree.
- `ai-routing-update-policy.md`  -  when the router must be reviewed or updated.
- `ai-task-route-table.yaml`  -  machine-readable route table.
- `ai-tool-settings-matrix.md`  -  recommended tool settings by route and mode.
- `universal-prompt-header.md`  -  reusable prompt header for Codex, Claude Code, ChatGPT, and similar AI tools.
- `stop-conditions.md`  -  mandatory stop conditions.
- `validation-and-pr-requirements.md`  -  validation and PR reporting requirements.
- `clean-room-and-source-boundaries.md`  -  source, copyright, and clean-room boundaries.
- `ai-interaction-audit-roadmap.md`  -  roadmap for governed AI input/output audit capture.
- `ai-interaction-audit-framework.md`  -  target audit envelope and transcript-control framework.
- `ai-audit-retention-and-privacy.md`  -  retention, privilege, privacy, and legal hold boundaries.

## Design intent

One AI entry point, one routing algorithm, route-specific templates, a settings matrix, update triggers, and PR enforcement later.

The immediate phase is docs-only. Enforcement belongs in a later PR after this control-plane surface is reviewed.
