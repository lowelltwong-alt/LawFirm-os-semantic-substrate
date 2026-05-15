# Skill-Agent Lifecycle and Recursive Improvement Doctrine

## Lifecycle states

`draft -> candidate -> active -> preferred -> deprecated -> superseded -> retired` with `quarantined` available from any state when safety or boundary checks fail.

## Automated improvement is allowed only inside policy

The system may automatically:

- score a skill or agent;
- detect workflow gaps;
- recommend a better skill for a workflow;
- create a draft improvement proposal;
- create a draft skill or draft agent to fill a detected gap;
- quarantine a skill or agent after hard safety failure;
- mark a skill as needing review.

The system must not automatically:

- promote protected skills into active use;
- expand side-effect permissions;
- delete canonical records;
- override human approval requirements;
- convert runtime evidence into canonical semantic truth.

## Exception Lake role

The Exception Lake records skill usage events, failures, quality signals, lifecycle proposals, gap detections, and improvement proposals. It may generate pressure vectors and candidate proposals, but it does not promote skills into canon.

## Skills Registry role

The Skills Registry stores draft and candidate skill definitions and metadata. It does not own lifecycle doctrine or promotion authority.

## Workflow gap rule

If a workflow repeatedly fails because a capability is missing, the system should create a `skill-gap-detection` record and a draft `skill-agent-improvement-proposal`. External research may be invoked only through an approved research-skill radar workflow and only with approved data boundaries.
