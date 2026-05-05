# DNA Invariant Checklist (Reusable)

## Source Basis

This checklist is derived from:
- `governance/FRACTAL_DNA_DESIGN_QA.md`
- `docs/architecture/8_LAYER_DNA_ADDRESS_MODEL.md`
- `governance/CANONICAL_ADDRESS_CONSTITUTION.md`

Use it for any first-order governed object type and example.

## Invariant 1: Identity

Required outcome: the object can answer **what are you?** deterministically.

Checklist:
- [ ] Stable object identifier field is explicit (for example `id`).
- [ ] Deterministic type discriminator is explicit (for example `object_type`).
- [ ] Human label/title is explicit where applicable.
- [ ] Identity is not collapsed into address.

## Invariant 2: Address / Placement

Required outcome: the object can answer **where are you?** using the canonical shell.

Checklist:
- [ ] Canonical placement fields are explicit (`address` and/or `address_struct`) or linked to an address-bearing record.
- [ ] Placement remains compatible with the canonical 8-part address pattern:
  `/environment/authority_zone/layer/domain/module/object_type/object_id/version`.
- [ ] Placement does not redefine identity.
- [ ] No parallel address system is introduced.

## Invariant 3: Lineage / Provenance

Required outcome: the object can answer **what are you derived from, and by whom/what?**

Checklist:
- [ ] Provenance source/evidence links are explicit or linked references are explicit.
- [ ] Derivation chain fields are explicit (for example `derived_from_refs`, activity refs, witness refs, or source refs).
- [ ] Upstream/downstream transformation references remain auditable.

## Invariant 4: Lifecycle / State

Required outcome: the object can answer **what state are you in now?**

Checklist:
- [ ] Lifecycle/status field is explicit (`lifecycle_status` or type-specific status).
- [ ] State changes are represented in governed fields (not inferred from folder names).
- [ ] Review/promotion/quarantine posture is representable where relevant.

## Invariant 5: Trust Posture

Required outcome: the object can answer **how trustworthy are you, and under what authority boundary?**

Checklist:
- [ ] Trust/authority zone is explicit (`authority_zone` or equivalent trust boundary).
- [ ] Confidence/review/trust qualifiers are explicit or linked references are explicit.
- [ ] Trust posture remains separate from probabilistic enrichment.

## Implementation Rule

For every first-order type, declare an invariant mapping with explicit fields and/or linked references for all five invariants.

Validation must fail when:
- a first-order type does not declare an invariant mapping, or
- a mapping omits one of the five invariants, or
- declared mapping fields do not exist in the type/interface field surface.
