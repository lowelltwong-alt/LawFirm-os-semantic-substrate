# Learning Loop Example Slice: Exception to Promotion Outcome

This slice demonstrates end-to-end traceability from an exception event through
feedback capture, interpreted inference, structured proposals, and promotion
outcomes (accepted + rejected).

## Trace Chain

1. **Exception signal**
   - `examples/exceptions/authority_conflict_override_example.json`
2. **Feedback capture**
   - `data/retrieval/RFB-000002.exception_authority_conflict.yaml`
3. **Interpreted inference**
   - `data/action-log/ALG-000002.exception_loop_inference.yaml`
4. **Structured proposals**
   - Accepted path candidate: `data/retrieval/PRP-000002.exception_authority_conflict_accepted.yaml`
   - Rejected path candidate: `data/retrieval/PRP-000003.exception_authority_conflict_rejected.yaml`
5. **Promotion decision log**
   - `data/action-log/ALG-000003.exception_loop_promotion_decisions.yaml`

## Why This Slice Matters

- demonstrates no direct canonical mutation from raw exception events
- demonstrates mandatory review metadata before actioned feedback can drive
  promotion
- demonstrates evidence + alignment checkpoint requirement on promoted proposals
- demonstrates explicit rejection as a first-class governed outcome
