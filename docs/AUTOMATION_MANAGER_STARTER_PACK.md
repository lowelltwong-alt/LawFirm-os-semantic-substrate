# Automation Manager Starter Pack

## Purpose

This starter pack helps the automation manager orient quickly and convert automation requests into governed Innovation OS work.

The goal is not to build bots on demand. The goal is to turn operational friction into validated, measurable improvements.

## Operating loop

```text
Signal -> Exception -> Pressure -> Opportunity -> Sprint/Pilot -> Validation Gate -> Scale Package -> Promotion Decision
```

## What counts as a signal

Examples:

- billing guideline misses
- carrier portal failures
- repeated AR delays
- time-entry narrative corrections
- Litify workflow exceptions
- iManage/source-document metadata gaps
- recurring Excel workarounds
- client/carrier rule changes
- failed automation attempts
- access-denied or support-unavailable answer events
- reviewer comments from AI/code agents

## What not to do

Do not treat a single anecdote as a production automation requirement.
Do not automate high-risk billing, client-facing, or legal judgment workflows without validation gates.
Do not store real exception events in the contract repo.
Do not let runtime observations directly rewrite canon.

## Automation intake form

Use this for every candidate.

```text
Automation candidate name:
Requester:
Business owner:
Source system(s):
Pain point / exception type:
Who experiences it:
Frequency:
Estimated dollar impact:
Estimated time impact:
Current workaround:
Evidence/source available:
Data sensitivity:
Allowed-use/access concern:
Client/matter impact:
Billing integrity impact:
Legal risk impact:
Automation type:
  - RPA
  - workflow routing
  - validation/check
  - report/brief
  - exception queue
  - document/source metadata cleanup
Risk level:
Human checkpoint required:
Required approvals:
Success metric:
Failure mode:
Rollback plan:
Exception queue owner:
Target sprint/pilot:
```

## Scoring model

Score each candidate from 1-5.

| Dimension | Meaning |
|---|---|
| Impact | Dollars, cycle time, client experience, or risk reduction. |
| Frequency | How often the exception occurs. |
| Evidence readiness | Whether source data and examples exist. |
| Automation fit | Whether the task is rule-based, repeatable, and reversible. |
| Risk | Billing, legal, confidentiality, client-facing, or operational risk. |
| Time to value | Likelihood of visible result in one sprint. |

Prioritize high-impact, high-frequency, low-to-moderate-risk items with clear evidence and rollback paths.

## Validation gates

Before scaling an automation, require:

- Ops owner approval
- Security/DLP review
- Legal Risk/Billing Integrity review if billing, client-facing, or legal judgment surfaces are affected
- access and allowed-use basis
- audit/logging path
- rollback path
- exception queue for failures
- KPI instrumentation

## First 30 days

### Week 1  -  orientation

- read `docs/HANDOFF_INDEX.md`
- read `governance/EXCEPTIONS_LAKE_BOUNDARY.md`
- map current automation requests and pain points
- identify source systems and owners
- establish an exception-review cadence

### Weeks 2-3  -  candidate triage

- collect 10-20 automation candidates
- score each candidate
- identify 3-5 near-term pilots
- define validation gates and owners

### Week 4  -  pilot selection

- choose 1-2 pilots
- define success metrics
- define rollback and exception queue
- prepare first executive brief

## First 90 days

- run 1-2 validated pilots
- produce weekly exception review
- produce monthly executive brief
- document one scale package if a pilot passes validation
- feed unresolved issues into pressure vectors and adaptation proposals

## Suggested questions to ask the repo/AI assistant

- What does the Innovation OS loop mean in this repo?
- What is the difference between an exception event and a promotion decision?
- What belongs in this repo versus a runtime Exceptions Lake?
- How do I score an automation candidate?
- What validation gates are required before scaling an automation?
- What does fail-closed mean for AI answers?
- How should I handle restricted or stale source support?
