# Legal Context Bundle Doctrine

A Legal Context Bundle is the context unit an agent receives to do legal work safely.

It should answer:

- what task is this context for;
- which documents and spans support it;
- which policy allowed access;
- which retrieval primitives were used;
- what is controlling, related, missing, stale, or uncertain;
- what the agent is allowed to do with the bundle.

## Bundle is not advice

A bundle is not legal advice, not a final answer, and not semantic canon. It is a structured evidence object for review and drafting.

## Minimum contents

- `bundle_id`
- `bundle_type`
- `run_id`
- `retrieval_trace_id`
- `access_decision_ref`
- `document_refs`
- `controlling_span_refs`
- `related_span_refs`
- `missing_or_uncertain`
- `allowed_use`
- `human_review_required`

## Fail-closed cases

The runtime must abstain or request review when:

- controlling authority is missing;
- access policy is unresolved;
- privilege label is unknown;
- schedules/amendments/definitions are referenced but absent;
- retrieval primitives disagree materially;
- the requested use exceeds `allowed_use`.
