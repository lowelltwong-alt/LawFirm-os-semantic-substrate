---
artifact: true
artifact_type: governance_markdown
author: Lowell Wong
created: 2026-05-29
review_cycle: 6 months
stale_after: 2026-11-29
project: LawFirm OS
status: proposed
canon_status: not_canon_until_approved
usage_note: >
  This artifact is a governance/reference draft. It should not be treated as canonical
  unless promoted through the Semantic Substrate governance process.
---

# Context Quality Doctrine — LawFirm OS

**Plane:** Semantic Substrate / Legal Knowledge Runtime boundary  
**Applies to:** Legal Context Bundles, matter-record quality, context admission, Orchestrator pre-model gates, Exception Lake context defects  
**Parent doctrine:** `AI_STRATEGY_DOCTRINE.md`

---

## 1. Doctrine statement

LawFirm OS treats context quality as a first-class control objective.

The system should reduce uncertainty before inference by assembling governed, permissioned, provenance-rich context.

The pre-model unit is the **Legal Context Bundle**.

The post-model unit is the **Evidence Packet**.

---

## 2. Why context quality matters

Models are increasingly available to all firms.

Durable advantage comes from what the firm can safely and repeatably provide to those models:

- clean matter records;
- structured legal task facts;
- client and matter context;
- source-grounded claims;
- approved institutional knowledge;
- past corrections;
- decision rules;
- evidence minimums;
- permission and privilege labels.

Bad context creates wrong routing, weak evidence, false confidence, hallucinated authority, repeated reviewer rework, cross-matter leakage, stale-law or stale-fact errors, and institutional folklore mistaken for governance.

---

## 3. Legal Context Bundle

A Legal Context Bundle is a contract-bound pre-model artifact.

It should contain:

```yaml
LegalContextBundle:
  bundle_id: string
  bundle_version: string

  contract:
    manifest_id: string
    manifest_sha256: string
    schema_refs: [string]

  matter_scope:
    tenant_id: string
    matter_id: string | null
    client_id: string | null
    practice_area: string | null
    jurisdiction: string | null
    phase: string | null
    confidentiality_label: string
    privilege_label: string

  context_inputs:
    matter_records: [MatterRecordRef]
    source_claims: [ContextClaim]
    institutional_knowledge_refs: [InstitutionalKnowledgeRef]
    prior_decision_refs: [DecisionRecordRef]
    playbook_refs: [PlaybookRef]
    skill_refs: [SkillTrustRef]

  quality:
    completeness_score: number
    provenance_score: number
    conflict_score: number
    freshness_score: number
    permission_score: number
    context_density_score: number
    reviewer_ready: boolean

  uncertainty:
    route_uncertainty: number | null
    issue_uncertainty: number | null
    source_uncertainty: number | null
    privilege_uncertainty: number | null
    measurement_model_ref: string | null

  assembly:
    assembled_by: legal_knowledge_runtime
    assembled_at: timestamp
    source_hashes: [string]
    bundle_sha256: string
```

---

## 4. Minimum admissibility rules

A context bundle should not be admitted to model execution if:

- contract reference is missing;
- bundle hash is missing;
- matter scope is ambiguous;
- permission label is missing;
- privilege label is missing;
- material claims lack source references;
- required matter facts are missing;
- unresolved source conflict is high;
- freshness checks fail;
- institutional knowledge is unreviewed where reviewed knowledge is required.

---

## 5. Legal Knowledge Runtime responsibilities

The Legal Knowledge Runtime should normalize matter records, extract claim-level facts, attach source references, resolve approved institutional knowledge, compute context-quality scores, detect missing or stale context, detect conflicting claims, label permission and privilege status, emit Legal Context Bundles, and preserve source/bundle hashes.

It should not define canonical route IDs, define canonical event classes, promote institutional knowledge to canon, store unbounded raw matter files in context bundles, or treat retrieved content as verified truth without provenance.

---

## 6. Orchestrator responsibilities

The Orchestrator should request or receive Legal Context Bundles, validate bundle schema, check bundle contract pin, check context-quality thresholds, block or escalate insufficient bundles, record context admission decisions in the run ledger, and include bundle references in Evidence Packets.

It should not define context-quality schemas ad hoc, silently repair missing context with model guesses, execute model calls when privilege or permission uncertainty is unresolved, or treat context-quality scores as legal-truth scores.

---

## 7. Exception Lake responsibilities

The Exception Lake should record context-quality defects, missing provenance, stale context, conflicting sources, privilege uncertainty, permission failure, reviewer corrections, high-confidence model errors, and repeated context assembly failures.

Exception Lake records remain runtime evidence, not canon.

---

## 8. Skills Registry responsibilities

The Skills Registry should evaluate whether a skill accepts only approved context types, preserves source references, preserves permission labels, emits audit-ready output, refuses forbidden context types, avoids stripping provenance, reduces reviewer rework, and does not expand authority.

---

## 9. Short form

> Better AI output begins before the model call. LawFirm OS wins by assembling clean, governed, provenance-rich context before inference and by preserving evidence after inference.
