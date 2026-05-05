# Repo Orientation Guide

## What is this?

This is the Law Firm semantic-governance substrate and Innovation OS contract repository.

It defines the governed contracts that future runtime systems should consume. It does not run the production systems itself.

## What problem does it solve?

It prevents AI, automation, and exception-learning work from becoming ungoverned sprawl. It gives Law Firm a controlled way to define:

- what objects mean
- which source evidence supports claims
- when an answer must refuse
- when evidence cannot be used because of sensitivity or lifecycle state
- how exceptions become governed learning signals
- how changes may be promoted into canon

## What is the shortest mental model?

```text
Meaning lives in canon.
Evidence supports claims.
Unsupported answers fail closed.
Runtime observations become exception candidates.
Canonical change requires promotion decisions.
```

## What should a new user read first?

1. `AI_START_HERE.md`
2. `README.md`
3. `docs/HANDOFF_INDEX.md`
4. `governance/EXCEPTIONS_LAKE_BOUNDARY.md`
5. `AGENTS.md`
6. `reports/RELEASE_READINESS_AUDIT.md`

## What can I ask an AI assistant?

- Explain this repo in plain English.
- Draw a map of the major folders and authority surfaces.
- What should I read first if I am the automation manager?
- What can this repo honestly claim today?
- What can it not claim yet?
- Show the exception-to-promotion path.
- Show the automation-candidate intake path.
- Which validators should pass?
- Why does SHACL fail closed?
- What does "no runtime Exceptions Lake here" mean?

## What should I not ask it to do?

Do not ask an agent to:

- ingest real internal documents into this repo
- create fake internal examples
- build a runtime lake in this repo
- bypass validators
- make broad rewrites without inventorying authority surfaces
- turn review comments directly into canon without the governed path

## What is the current readiness state?

The repo is ready as a governed contract/readiness layer. It is not yet a production knowledge system.

Current readiness includes:

- validation gates
- source-ingestion manifest readiness
- fail-closed grounding
- allowed-use and sensitivity posture
- synthetic evaluation readiness
- Exceptions Lake boundary discipline
- agent operating contract

Not yet included:

- internal corpus ingestion
- production retrieval quality metrics
- production answer quality metrics
- production runtime Exceptions Lake
- green SHACL conformance for the current core SHACL pair
