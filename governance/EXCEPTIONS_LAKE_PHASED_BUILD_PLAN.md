# Exceptions Lake Phased Build Plan

## Phase EL-1: Capture foundation

Outputs:
- Exception event schema
- Pressure vector schema
- Exception schema registry
- Route registry
- Governed examples for core classes

Exit criteria:
- Validation passes for all governed examples.
- Missing route/trust metadata fails fast.

## Phase EL-2: Loop routing

Outputs:
- Route coverage for retrieval miss, workflow escalation, and authority conflict/override
- Operational routing contract from `event_class` to `route_id`
- Drift checks for unknown route IDs

Exit criteria:
- Every governed example resolves to a registered route.
- Route registry states promotion gate requirements.

## Phase EL-3: Pressure normalization

Outputs:
- Pressure vector generation contract
- Recurrence thresholds by exception class
- Trust-weighting policy for pressure aggregation

Exit criteria:
- Multiple exception events can be summarized into governed pressure vectors.
- Pressure vectors preserve lineage to originating exception IDs.

## Phase EL-4: Promotion-safe integration

Outputs:
- No-direct-mutation control in validation pipeline
- Promotion packet handoff spec from exceptions layer
- Audit trace contract for accepted/rejected learning

Exit criteria:
- Raw events cannot mutate canonical ontology directly.
- All proposed canonical changes require reviewed promotion workflow.

## Phase EL-5: Continuous learning operations

Outputs:
- Retrieval and workflow tuning dashboards fed by governed exceptions
- Quarterly route and trust policy review cycle
- Exception-class expansion process

Exit criteria:
- Retrieval/workflow/governance improvements run from the same governed evidence stream.
