# Skill-Agent Control Plane Boundary

## Purpose

The Skill-Agent Control Plane makes skills, agents, tools, evaluators, guardrails, workflows, and future repos discoverable and governable across the LawFirm OS kernel.

## Canonical ownership

The Semantic Substrate owns:

- skill-agent metadata schema;
- lifecycle states and transition policy;
- quality scoring policy;
- workflow composition schema;
- skill gap detection schema;
- repo membership registry;
- skill-agent graph index contract;
- AI front-door routing doctrine.

Runtime repos may implement skills, agents, tools, adapters, and evaluators, but they do not own canonical lifecycle semantics or quality scoring policy.

## Required local artifacts

Every LawFirm OS repo must have:

- `README.md`
- `AGENTS.md`
- `AI_WORK_START_HERE.md`
- `skill-agent-manifest.json`

Every skill or agent must have machine-readable metadata. The human-readable `SKILL.md` or agent instruction is not sufficient.

## Scaling rule

When skill/agent count becomes large, the graph index may be sharded. Sharding changes storage layout, not the metadata schema or validation obligation.

## New repo rule

A new sibling repo whose name matches `LawFirm-os-*` is non-compliant until it is registered in `registry/lawfirm-os-repo-registry.json` or explicitly excluded with a reason.

## Schema-surface exclusion rule

Skill-Agent Control Plane schemas (`skill-agent-metadata`, `skill-agent-lifecycle-record`, `skill-agent-improvement-proposal`, `skill-agent-quality-score`, `skill-gap-detection`, `workflow-composition`, `repo-membership-record`) are **canonical for the control plane but intentionally excluded from the primary `registry/schema-surface-registry.json` pending promotion**. This is not a hidden surface or a documentation gap: the exclusion is explicit and machine-readable.

Why the exclusion exists:

- The control-plane schemas are versioned and validated by `scripts/validate_skill_agent_control_plane.py`, not by the primary schema registry's surface gate.
- Adding them to the primary schema surface before they have stabilized contract usage in two or more runtime repos would prematurely lock the schema shape against legitimate iteration.
- The primary schema surface is reserved for schemas with cross-repo runtime contract obligations (e.g., exception routes, governance manifests, contract lock).

Where the exclusion is recorded:

- `registry/schema-surface-exclusions.json` enumerates each excluded control-plane schema with `governance_doc: "governance/SKILL_AGENT_CONTROL_PLANE_BOUNDARY.md"`, `governance_reason`, and `exclusion_class: "skill_agent_control_plane_surface"`.

When the exclusion is lifted:

- A schema graduates out of the exclusion list when (a) at least two LawFirm OS repos rely on it for runtime contracts, AND (b) the canonical surface registry maintainer accepts the responsibility of versioning it under the primary schema surface gate.
- Promotion is recorded by removing the entry from `registry/schema-surface-exclusions.json` and adding it to `registry/schema-surface-registry.json` in the same commit, with a managed-patch decision record explaining the promotion.
