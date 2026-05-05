# Folder Semantics

This file explains the role and authority level of each top-level folder in this repository.

Use it to answer: “What lives here?” and “How authoritative is it?”

Authority tiers used here:
- **canonical** — binding repo truth
- **operational** — implements and enforces the canonical layer
- **reference** — maps or aligns to external systems/standards
- **example** — illustrative only
- **supporting** — narrative, evaluation, or generated support material
- **historical** — archived or legacy only

---

## Canonical

### `registry/`
Role: authoritative repo control files, including source-of-truth, design authority, and registries.

Use this when you need to know:
- what the repo says its role is
- what takes precedence
- who owns what
- which registry governs which area

### `governance/`
Role: doctrine, system maps, lifecycle posture, manifests, operating guidance, and mutation boundaries.

Use this when you need to know:
- what is canonical vs derived
- how change should happen
- what policy controls apply

---

## Operational

### `ontology/`
Role: semantic meaning layer.

Contains ontology modules and semantic structure. This is where concept meaning lives, not in examples.

### `shapes/`
Role: SHACL and validation shapes.

Used to validate RDF/semantic structures and enforce shape-level expectations.

### `schemas/`
Role: concrete JSON schemas for governed object types.

This is the active schema surface for live validators on `main`.
Current active schema lookup should start with `registry/schema-registry.json`. The older `schemas/schema_registry.json` is a stale stub and must not be used for routing.

### `schema/`
Role: schema-set manifest and interface/invariant structure.

This is **not** the same as `schemas/`.
Think of it as the schema framework surface rather than the individual type files.

### `scripts/`
Role: validation, enforcement, and maintenance tooling.

If you need to know what the repo actually checks today, look here.

---

## Reference

### `interop/`
Role: external model mapping profiles and interoperability artifacts.

### `mappings/`
Role: source-to-canonical and cross-model mappings.

### `profiles/`
Role: adapter and system-specific profile files.

### `standards/`
Role: standards posture, drift rules, and stable external/internal reference material.

These folders help connect the repo to outside systems or standards, but they do not outrank `registry/` or `governance/`.

---

## Example

### `examples/`
Role: illustrative object instances.

Do not infer canonical truth from examples.
Use them to understand expected shape, not to define meaning.

### `data/`
Role: sample/test data.

### `graphs/`
Role: derived graph partitions and related graph artifacts.

These are non-authoritative and may lag active contracts.

---

## Supporting

### `docs/`
Role: narrative documentation and explanatory material.

Important: `docs/` is informative, not normative.
If `docs/` conflicts with `registry/` or `governance/`, the latter wins.

### `reports/`
Role: generated reports and audit artifacts.

### `eval/`
Role: evaluation artifacts and testing support.

### `templates/`
Role: supporting templates and template drafts.

### `.github/`
Role: repository automation and workflow configuration.

These files matter operationally, but they do not define canonical meaning by themselves.

---

## Historical

### `legacy/`
Role: deprecated legacy materials.

### `archive/`
Role: archived materials retained for traceability.

Do not use either folder as an active authority surface.

---

## Fast rules

- Start with `registry/` for precedence and ownership.
- Use `governance/` for doctrine and mutation rules.
- Use `schemas/` for active JSON schema lookup.
- Use `ontology/` for meaning.
- Treat `docs/`, `examples/`, `reports/`, `legacy/`, and `archive/` as non-authoritative unless a higher-authority file explicitly says otherwise.
