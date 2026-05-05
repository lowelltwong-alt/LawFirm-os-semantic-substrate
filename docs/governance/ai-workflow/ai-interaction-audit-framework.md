# AI Interaction Audit Framework

This framework defines the target audit model for governed AI interactions. It is a contract and governance plan, not a production storage implementation.

## Separation of responsibilities

| Surface | Responsibility |
|---|---|
| Law Firm contract repo | Defines audit concepts, schemas, retention classes, policy expectations, and route requirements. |
| Runtime repos | Capture audit events and enforce audit policy at execution time. |
| Secure audit store | Stores sealed transcripts or content when approved by governance. |
| SIEM / monitoring | Receives selected audit metadata and alerts. |

## Audit envelope

The audit envelope is metadata-first and should be safe to store in governed audit infrastructure.

Target fields:

- `audit_event_id`
- `session_id`
- `run_id`
- `actor_id`
- `agent_or_tool_id`
- `system_context`
- `route`
- `mode`
- `contract_repo_sha`
- `model_provider`
- `model_or_deployment`
- `prompt_or_instruction_version`
- `started_at`
- `ended_at`
- `content_input_hash`
- `content_output_hash`
- `sealed_transcript_pointer`
- `redaction_status`
- `tool_call_refs`
- `retrieval_source_refs`
- `access_decision_refs`
- `policy_gate_results`
- `approval_token_ref`
- `human_reviewer_ref`
- `risk_tier`
- `retention_class`
- `legal_hold_status`
- `audit_event_hash`
- `previous_audit_event_hash`

## Sealed transcript boundary

The sealed transcript is not a contract-repo object. It may contain sensitive or privileged content and must be stored only in an approved secure store.

The contract repo may define the pointer and governance requirements, but it must not store sealed transcript contents.

## Redaction and minimization

Runtime implementations should support:

- content minimization before persistence
- redacted transcript variants
- hash-only capture for low-risk or test interactions
- policy-controlled access to sealed content
- route-based retention defaults

## First implementation target

The first implementation should be synthetic or dry-run only:

```text
synthetic interaction
-> route/mode classification
-> policy decision
-> content hashes
-> append-only audit envelope
-> no sealed production transcript
```
