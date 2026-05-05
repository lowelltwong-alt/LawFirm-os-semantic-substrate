# Universal Prompt Header

Use this header for Codex, Claude Code, ChatGPT, Cursor, Copilot Workspace, or other AI-assisted repository work.

```text
Repository: lowelltwong-alt/LawFirm-os-semantic-substrate

Before task work:
- Read AGENTS.md.
- Read AI_START_HERE.md.
- Read AI_WORK_START_HERE.md.
- Read registry/source-of-truth.json and registry/design-authority.json.
- Select exactly one route from docs/governance/ai-workflow/ai-task-route-table.yaml.
- State the route, mode, allowed paths, forbidden paths, validation plan, and stop conditions before editing.

Hard boundaries:
- Do not use real internal Law Firm records.
- Do not create production runtime, connector, telemetry, dashboard, audit-lake, or transcript-store surfaces in this repo.
- Do not store raw user AI prompts or outputs in this repo.
- Do not redefine canonical meaning outside existing authority surfaces.
- Do not copy leaked code, private prompts, or leak-derived repositories.

After work:
- Run route-appropriate validation.
- Report exact validation results.
- State AI routing impact.
```
