# Claude Adapter Instructions

This file is an adapter for Claude-style coding agents.

Read in this order before acting:
1. `AI_START_HERE.md`
2. `AGENTS.md`
3. `registry/source-of-truth.json`
4. `registry/design-authority.json`
5. `governance/AI_CONTROL_PLANE_BOUNDARY.md`
6. `.ai/instruction-kernel.yaml`
7. `.ai/action-risk-tiers.yaml`
8. `.ai/approval-matrix.yaml`

This file does not override registries, doctrine, or canonical schema authority.

## Adapter rules

- treat vendor settings as adapter-only
- use deny-first posture for risky operations
- do not claim production readiness from synthetic or draft artifacts
- do not treat runtime traces, embeddings, or summaries as canon
- do not use leaked or unofficial vendor code as input to repo changes

## Sensitive operations

For T3 and above changes, produce or update a governed change packet before editing.

<!-- BEGIN DIGITAL_ASSET_DIRECTORY_CLAUDE_IMPORT -->
@AGENTS.md

Claude Code should follow the DAD enrollment contract in `AGENTS.md` and
`.digital-asset/dad-integration.json`. Agent review is triage only; human
approval gates remain separate.
<!-- END DIGITAL_ASSET_DIRECTORY_CLAUDE_IMPORT -->
