# AI Control Plane Boundary

This repository supports AI assistants and coding agents, but the AI control plane is **governed by Law Firm canonical authority** rather than by any single vendor runtime.

## Role of the AI control plane

The AI control plane defines:
- neutral instruction and safety posture for AI contributors
- risk tiers and approval requirements for agent-authored changes
- change-packet requirements for governed edits
- deterministic release-hygiene and boundary checks
- adapter rules for vendor-specific agent surfaces

It does **not** redefine:
- canonical ontology meaning
- canonical document structure
- registry precedence
- promotion-decision requirements
- policy or access semantics already governed by canonical files

## Authority order

When AI-facing files disagree, follow this order:

1. `registry/source-of-truth.json`
2. `registry/design-authority.json`
3. `governance/AI_CONTROL_PLANE_BOUNDARY.md`
4. `AGENTS.md`
5. `AI_START_HERE.md`
6. `.ai/` neutral control-plane artifacts
7. vendor adapter files such as `.claude/`, GitHub Copilot instructions, or Microsoft-house profiles

Vendor adapters are **consumers** of Law Firm contracts. They are not semantic authorities.

## Mutation boundary

AI systems may:
- inspect
- summarize
- propose
- validate
- draft derived artifacts
- prepare governed change packets

AI systems may not directly mutate canonical meaning, registry truth, policy posture, or source-of-truth precedence outside the existing governed promotion path.

## Runtime boundary

This repository is not a production runtime, telemetry lake, vector store, prompt log archive, or live agent execution environment.

Allowed here:
- schemas
- policies
- validation scripts
- examples
- adapter instructions
- governance docs

Not allowed here:
- live client or matter content
- production agent memories
- uncontrolled model traces
- leaked vendor code or leak-derived repositories
- runtime indexes or answer caches represented as canonical truth

## Claude Code / agent-harness lesson encoded here

Prompt instructions are advisory.
Deterministic controls are authoritative.

Accordingly:
- prompts and adapter files may guide behavior
- hooks, scripts, validators, CI checks, approval rules, and release-hygiene gates must enforce behavior

## Microsoft-house posture

Law Firm remains AI-agnostic at the canonical layer.
Microsoft services may be the preferred implementation path for identity, DLP, audit, workflow, and hosted agent execution, but they do not become semantic authorities in this repository.
