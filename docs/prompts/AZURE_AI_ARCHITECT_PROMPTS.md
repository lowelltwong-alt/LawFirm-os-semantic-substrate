# Azure AI Architect Prompt Kit

Use these prompts with ChatGPT, Copilot, Claude, or another review AI when an
Azure AI architect is evaluating or taking over the platform side of this repository.

## 1. Azure Orientation Prompt

You are supporting an Azure AI architect who needs to understand this repository as a governed retrieval and answer foundation, not as a generic RAG project.

Explain:
- what problem the repository is solving
- what the canonical spine controls
- which layers are content/governance versus platform/execution
- how ingestion, retrieval, answer generation, evaluation, and access control should be shaped by the repo
- which documents the architect should read first

Your output should include:
1. plain-language architecture summary
2. what gives this repository immediate Azure value
3. what is not yet production-ready
4. first reading order
5. first architecture decisions to make

## 2. Azure Gap Audit Prompt

You are reviewing this repository as an Azure AI architect looking for implementation gaps.

Audit the repository for:
- missing platform assumptions
- unclear ingestion or indexing requirements
- access-control risks
- places where answer orchestration would be underspecified
- evaluation or monitoring gaps that would matter in a bounded pilot

Return:
1. the top 10 Azure implementation gaps
2. why each gap matters
3. what can be solved in platform design
4. what needs governance or KM clarification
5. the smallest safe remediation path

## 3. Governed Retrieval Prompt

You are helping an Azure AI architect design a governed retrieval pattern for this repository.

Use the current repo state to propose:
- how content should be ingested and indexed
- which metadata must be preserved for filtering
- how retrieval should distinguish canonical, derived, restricted, and quarantine material
- how provenance should survive retrieval into final answers
- what should happen when the system cannot answer safely

Return:
1. retrieval pattern
2. required metadata
3. filtering and eligibility rules
4. provenance handling
5. escalation behavior

## 4. Answer Orchestration Prompt

You are helping an Azure AI architect design the answer path for a bounded pilot workflow.

Explain:
- what the orchestrator should receive
- what retrieval should return
- how the answer payload should be assembled
- how access control and restrictions should be checked before output
- how review or exception routing should surface to the end user

Return:
1. orchestration flow
2. answer assembly logic
3. access and restriction checkpoints
4. provenance requirements
5. fallback and escalation path

## 5. Pilot Deployment Prompt

You are helping an Azure AI architect propose the safest bounded pilot deployment pattern for this repository.

Design a pilot that preserves:
- governance semantics
- access boundaries
- provenance visibility
- evaluation readiness
- bounded scope

Return:
1. minimum viable Azure architecture
2. which services are actually needed first
3. which services should wait
4. operational risks
5. recommended pilot boundary

## 6. Azure Takeover Plan Prompt

You are helping an Azure AI architect take ownership of this repository's platform implementation over the next 90 days.

Build a takeover plan that covers:
- first week orientation
- first 30-day platform design tasks
- first 60-90 day pilot implementation tasks
- which governance dependencies must be resolved in parallel
- what success metrics should be measured

Return:
1. first-week checklist
2. 30-day plan
3. 60-90 day plan
4. dependencies on KM/governance ownership
5. anti-patterns to avoid
