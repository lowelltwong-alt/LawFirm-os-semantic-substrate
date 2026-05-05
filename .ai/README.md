# AI Control Plane

This directory is the neutral AI-facing control plane for Law Firm.

Its purpose is to provide tool-neutral guidance, risk tiers, approval rules,
and adapter boundaries so vendor-specific assistants can consume the same Law Firm
rules without redefining canonical semantics.

Read in this order:

1. `instruction-kernel.yaml`
2. `canonical-boundaries.yaml`
3. `no-hallucination-policy.md`
4. `model-provider-portability.yaml`
5. `action-risk-tiers.yaml`
6. `approval-matrix.yaml`
7. files under `.ai/adapters/`

The `.ai/` surface is governed, but it does not outrank:
- `registry/source-of-truth.json`
- `registry/design-authority.json`
- `governance/AI_CONTROL_PLANE_BOUNDARY.md`
- active registries and validated operational files
