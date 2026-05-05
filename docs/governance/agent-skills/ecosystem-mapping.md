# Ecosystem Mapping

This document maps external agent and skill ecosystems into substrate-neutral registry classes.

## Mapping posture

Vendor or tool-specific surfaces are consumers of substrate-neutral canonical cards. They are not semantic authorities.

## Relationship mapping

- `Claude Skills`
  - map as `skill` cards with `platform_surface:claude_skill`
- `Claude subagents`
  - map as `subagent` or `orchestrator` cards
- `OpenAI Agents`
  - map as `agent`, `orchestrator`, or `workflow` cards
- `Codex workflows`
  - map as `workflow`, `orchestrator`, `monitor`, or `agent` cards
- `GitHub Copilot instructions`
  - map as adapter or instruction surfaces, never semantic authority
- future `runtime monitors`
  - map as `monitor` cards with governance-only posture until a separate runtime repo implements them

## Hard boundary

This PR does not add:
- `.claude/agents` files
- `.claude/skills` files
- runtime monitor implementation
- production orchestration logic

## Why this matters

Large capability inventories are easier to govern when ecosystem-specific surfaces are mapped into a neutral canonical vocabulary instead of treated as separate ungoverned islands.
