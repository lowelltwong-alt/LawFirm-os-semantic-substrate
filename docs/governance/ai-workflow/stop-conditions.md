# Stop Conditions

AI-assisted work must stop and report instead of guessing when any of these conditions occur.

## Repository state

- Target branch, base branch, or worktree state is ambiguous.
- Existing branch contains unrelated work.
- The task would require reset, rebase, force-push, deletion, or overwrite without explicit instruction.

## Authority and governance

- No route in `ai-task-route-table.yaml` fits the task.
- Source-of-truth or design-authority surfaces conflict.
- The task would promote research, examples, reports, or runtime observations into canon without an authorized promotion path.
- The task would treat an adapter profile, mapping, report, archive, legacy file, or example as semantic authority.

## Data and security

- The task requires real internal Law Firm records, client/matter data, employee data, privileged material, or raw AI transcripts.
- The task would store production prompts, outputs, transcripts, answer caches, embeddings, indexes, telemetry, or audit-lake records in this repo.
- The task changes confidentiality, privilege, trust-zone, retention, or legal-hold assumptions without governance review.

## Runtime and side effects

- The task would create a production runtime, connector worker, dashboard, HTTP service, approval service, audit lake, transcript vault, or side-effecting automation in this repo.
- The task would allow runtime observations to mutate canonical ontology, taxonomy, schemas, or governance directly.

## Validation

- Required validators fail for reasons other than a documented truthful fail-closed gate.
- A validator failure would need to be converted into a silent skip.
- The contributor cannot report exact validation commands and outcomes.
