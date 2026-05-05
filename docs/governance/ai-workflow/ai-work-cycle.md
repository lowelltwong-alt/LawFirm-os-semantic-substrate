# AI Work Cycle

All AI-assisted work must complete this cycle before editing, proposing runtime changes, or opening a PR.

1. **Orient**  -  read `AGENTS.md`, `AI_START_HERE.md`, `AI_WORK_START_HERE.md`, source-of-truth and design-authority registries, and task-relevant governance files.
2. **Sync safely**  -  confirm current branch, target scope, and whether local or remote work already exists.
3. **Classify task**  -  select exactly one primary route from `ai-task-route-table.yaml`.
4. **Choose mode**  -  Explore, Plan, Edit, or Execute.
5. **Choose settings**  -  use the route's reasoning, internet, and permission posture.
6. **Choose template**  -  use the route-specific template under `templates/`.
7. **Execute inside scope**  -  change only allowed paths and preserve canonical boundaries.
8. **Validate**  -  run route-required validation and report exact results.
9. **Open PR**  -  include governance sections and routing impact.
10. **Report outcome**  -  summarize files changed, validation, risks, and follow-ups.
11. **Check router update**  -  decide whether route table, templates, stop conditions, settings, or PR requirements must change.

## Work modes

| Mode | Meaning | Side effects |
|---|---|---|
| Explore | read, inspect, compare, summarize | none |
| Plan | propose changes, implementation plan, risks | no mutation except plan docs if requested |
| Edit | edit repo files within approved route/scope | repo-only changes |
| Execute | runtime action or external side effect | not allowed in this repo except docs-only planning |

Law Firm may define runtime contracts, but runtime execution belongs outside this repo unless an authority surface explicitly says otherwise.
