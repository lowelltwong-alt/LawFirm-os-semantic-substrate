# Learning Loop State Machine

## Purpose

This document formalizes the governed learning-loop transition model using
existing repository object families in `data/retrieval/` and
`data/action-log/`.

## Canonical States and Artifact Types

| State | Meaning | Primary object type |
| --- | --- | --- |
| `feedback_signal` | Raw governed signal captured from retrieval or exception pressure. | `retrieval_feedback` |
| `interpreted_inference` | Human/AI interpretation of what the signal means and what should be tested. | `action_log_entry` (`action_type: revise_alignment_assessment` / analysis actions) |
| `structured_proposal` | Explicit candidate change with bounded scope and approval criteria. | `proposal_promotion` |
| `promoted_baseline_change` | Reviewed change accepted into baseline operating posture (or explicitly rejected). | `proposal_promotion` + `action_log_entry` decision record |

## Required Transition Checkpoints

Transition checkpoints are tied to existing enums in `schema/enums/`.

- **Trust checkpoint**: `authority_zone` must map to `trust_zone` enum values.
- **Review checkpoint**: `review_metadata.review_status` must map to `review_status`.
- **Reviewer accountability**: `review_metadata.reviewer_role` must map to
  `reviewer_role`.
- **Alignment checkpoint**: `alignment_assessment.alignment_degree` must map to
  `alignment_degree`.
- **Evidence checkpoint**: `alignment_assessment.evidence_sufficiency` must map
  to `evidence_sufficiency`.

## Allowed Transitions

```text
feedback_signal (captured)
  -> feedback_signal (triaged)
  -> interpreted_inference
  -> structured_proposal (proposed)
  -> structured_proposal (under_review)
  -> promoted_baseline_change (approved_for_pilot | promoted)
```

### Transition Rules

1. `retrieval_feedback_status: captured -> triaged -> actioned|archived`
2. `proposal_promotion_status: proposed -> under_review -> approved_for_pilot|promoted|rejected`
3. Promotion path to `approved_for_pilot` or `promoted` requires:
   - non-empty review metadata on source feedback
   - non-empty evidence sufficiency and alignment assessment on proposal

## Rejection Paths

A transition must be rejected when any of the following are true:

1. **Feedback promoted without review metadata**
   - feedback is `actioned` or is referenced by a proposal at
     `approved_for_pilot|promoted`
   - `review_metadata` is missing or incomplete
2. **Proposal promoted without evidence + alignment**
   - proposal is `approved_for_pilot|promoted`
   - `alignment_assessment.evidence_sufficiency` missing
   - `alignment_assessment.alignment_degree` missing
3. **Enum mismatch at checkpoint**
   - any checkpoint value is outside allowed enum values

## Operational Notes

- Rejections should be explicit, not silent; use `proposal_promotion_status: rejected`
  and record rationale in `decision_notes` and an `action_log_entry`.
- `interpreted_inference` remains non-canonical by design and is represented via
  audited action-log steps until promoted.
