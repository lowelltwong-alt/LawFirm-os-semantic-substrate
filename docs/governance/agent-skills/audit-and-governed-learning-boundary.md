# Audit and Governed-Learning Boundary

This document connects the Agent/Skill Capability Graph to audit, Exceptions Lake, and governed learning without collapsing those surfaces into one layer.

## AI interaction audit ledger

Capability cards define:
- `audit_requirement_class`
- `transcript_posture`

The audit ledger remains metadata-first. Raw transcripts remain outside this repository in approved secure stores only.

## Transcript governance

This registry surface may declare transcript posture requirements, but it must not store raw transcript content.

Default posture:
- `no_raw_transcript_in_repo`

## Exceptions Lake

Broken workflows, stale ownership, overlap conflicts, invalid orchestration, and monitor findings are candidate signals only.

They may contribute to governed learning. They may not directly mutate canonical registry cards.

## Math Intelligence

Math Intelligence may create impact assessments or roadmap candidates against capability surfaces. It may not directly mutate cards.

## Future Frontier Intelligence

Future Frontier Intelligence should be treated as an adjacent governed-learning surface. This PR only creates relationship hooks and shared governance language.

## Governed learning

This registry is a governed-learning input surface for governed recursive improvement.

Use the existing path:

`candidate signal -> assessment -> recommendation -> adaptation-proposal recommendation if reviewed -> promotion-decision only through existing authority path`
