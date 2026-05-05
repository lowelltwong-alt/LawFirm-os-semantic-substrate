# Validation and PR Requirements

Every AI-assisted PR must report the selected route, mode, validation commands, validation outcomes, and routing impact.

## Required PR sections

```markdown
## AI route
- Route:
- Mode:
- Allowed paths:
- Forbidden paths:

## Validation
- [ ] Task-specific validators run
- [ ] Repo drift check run when applicable
- [ ] Full audit run or known fail-closed gate reported when applicable

## AI routing impact
Does this PR change AI work routing, templates, validation expectations, stop conditions, route ownership, or AI tool settings?
- [ ] No
- [ ] Yes  -  updated AI_WORK_START_HERE.md / ai-task-route-table.yaml / relevant template
- [ ] Yes  -  follow-up PR required

## AI audit impact
Does this PR change AI input/output audit capture, retention, transcript storage, policy-gate logging, or audit-event requirements?
- [ ] No
- [ ] Yes  -  updated audit roadmap/framework/privacy docs
- [ ] Yes  -  follow-up PR required
```

## Validation posture

Do not convert validator failures into silent skips. Known truthful fail-closed gates must be reported exactly. Unsupported claims must fail closed instead of being papered over.

## Merge posture

Docs-only router changes may be reviewed as governance documentation. Any later enforcement change belongs in a separate PR and should include validators or PR-template checks only after the route docs are stable.
