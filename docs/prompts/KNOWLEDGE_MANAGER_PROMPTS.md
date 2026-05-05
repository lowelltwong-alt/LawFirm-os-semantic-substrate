# Knowledge Manager Prompt Kit

Use these prompts with ChatGPT, Copilot, Claude, or another review AI when a
Knowledge Manager is taking over stewardship of this repository.

## 1. Day-One Orientation Prompt

You are supporting an incoming Knowledge Manager who needs to understand this repository as a governed knowledge system, not as a generic ontology project.

Explain:
- what problem the repository is solving
- which parts are canonical versus derived
- how stewardship, review, promotion, and exceptions work
- which documents the KM lead should read first
- what the KM lead could practically own in the first 30 days

Your output should include:
1. plain-language summary
2. what gives this repository immediate KM value
3. what is still immature
4. first reading order
5. first ownership moves

## 2. Stewardship Gap Audit Prompt

You are reviewing this repository as a Knowledge Manager looking for stewardship gaps.

Audit the repository for:
- missing or weakly governed answer patterns
- duplicated or stale documentation
- places where examples, templates, and governance docs could drift
- places where policy answers would still depend on human memory instead of governed artifacts
- places where lifecycle status or ownership should be made more explicit

Return:
1. the top 10 stewardship gaps
2. why each gap matters operationally
3. which gaps KM can fix directly
4. which gaps need reviewer or approver involvement
5. the smallest practical remediation sequence

## 3. Workflow Takeover Prompt

You are helping a Knowledge Manager take over one bounded workflow using this repository.

Use the current repository state to design a KM operating model for a single workflow such as intake, conflicts, or AI-use policy triage.

Explain:
- what artifacts the workflow should rely on
- which roles should author, review, approve, and steward content
- what the answer format should look like for end users
- what should trigger escalation or exception review
- what success metric would prove the workflow is worth continuing

Return:
1. workflow scope
2. stewardship model
3. answer pattern
4. review and exception path
5. 30-day rollout approach

## 4. Weekly KM Review Prompt

You are the weekly review assistant for the Knowledge Manager who owns this repository.

Review the current repository state and identify:
- new or changed artifacts that affect sponsor-facing meaning
- validation or coherence risks
- stale drafts or deprecated materials that should be cleaned up
- unresolved gaps in supported questions or answer payloads
- any place where exceptions imply missing governed content

Return:
1. what changed
2. what requires KM action
3. what requires reviewer or approver action
4. what can wait
5. the next three highest-leverage tasks

## 5. Executive Prep Prompt

You are helping a Knowledge Manager prepare to show this repository to an executive sponsor.

Explain the repository as:
- a governed decision substrate
- a KM operating layer
- a future-safe foundation for retrieval and AI support

Do not present it as an abstract ontology exercise.

Return:
1. the executive storyline
2. what the sponsor should care about
3. what is real today
4. what is intentionally still bounded
5. the smartest next ask

## 6. Takeover Plan Prompt

You are helping a Knowledge Manager take ownership of this repository over the next 90 days.

Build a takeover plan that covers:
- first week orientation
- first 30-day cleanup and stewardship setup
- first 60-90 day operationalization steps
- what should be measured
- what should not be expanded yet

Return:
1. first-week checklist
2. 30-day plan
3. 60-90 day plan
4. success metrics
5. anti-patterns to avoid
