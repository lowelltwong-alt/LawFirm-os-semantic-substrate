# Exceptions Layer Integration Note

## Integration scope

This note defines how the exceptions layer integrates with existing governance, schema, and validation surfaces.

## Upstream dependencies

- `governance/ALIGNMENT_FIRST_ROADMAP.md`
- `governance/ONTOLOGY_BOUNDARY_CONTRACT.md`
- `registry/source-of-truth.json`

## Downstream integrations

1. **Validation**
   - `scripts/validation/validate_exception_events.py` validates schema conformance.
   - `scripts/validation/validate_exception_governance.py` enforces route/trust and no-direct-mutation controls.
2. **Registry controls**
   - `registry/exceptions-schema-registry.json` binds exception object families to schemas.
   - `registry/exception-route-registry.json` governs allowed routes and prohibited direct actions.
3. **Examples as governed corpus**
   - `examples/exceptions/*.json` are canonical governed examples for learning loop tests.

## Contract with canonical ontology

- Exception events are learning evidence, not ontology truth updates.
- Canonical ontology mutation is only legal after reviewed promotion from aggregated pressure.
- Raw events may reference canonical targets but must never apply direct mutation actions.

## Operational guidance

- Treat unknown `event_class` values as schema errors.
- Treat unknown `route_id` values as governance errors.
- Treat any direct canonical mutation flag as a hard failure.
