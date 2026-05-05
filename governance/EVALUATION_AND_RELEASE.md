# Evaluation and Release

## Release rule

A phase artifact is releasable only when:
- it is registered
- it validates against its schema or shape
- it has at least one example
- it does not violate lifecycle or mutation-boundary rules

## Evaluation categories

- semantic validity
- example conformance
- retrieval quality
- citation quality
- access-control correctness
- operational SLO conformance

## Release gates

- schema validation
- SHACL validation
- registry reference checks
- example coverage checks
- quality-gate review for high-impact changes

## Grounded-Answer Evaluation Readiness

The grounded-answer evaluation harness in this repo is readiness infrastructure
only.

- Synthetic evaluation fixtures may test grounding, refusal-safe behavior, and
  permission-aware or lifecycle-aware unavailability outcomes.
- Synthetic fixtures are not evidence of production retrieval accuracy,
  precision, recall, corpus coverage, answer quality, or firm-knowledge
  correctness.
- Real evaluation scores require approved internal corpus ingestion and
  approved gold cases.
- Until those prerequisites exist, the repo may claim evaluation readiness, not
  evaluated production performance.
