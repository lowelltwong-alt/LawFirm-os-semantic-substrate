---
artifact: true
artifact_type: standard_markdown
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

# Institutional Knowledge Encoding Standard — LawFirm OS

**Plane:** Semantic Substrate / Legal Knowledge Runtime / Skills Registry boundary  
**Applies to:** institutional knowledge capture, playbooks, client preferences, expert heuristics, reusable legal work patterns  
**Parent doctrine:** `AI_STRATEGY_DOCTRINE.md`

---

## 1. Standard statement

Institutional knowledge is not free-form prompt text.

Institutional knowledge must be encoded with provenance, scope, authority level, review status, reuse rules, expiration policy, and promotion history.

A person describing how they work is not the same as governed institutional knowledge.

---

## 2. Institutional Knowledge Reference

Use this shape as the baseline object:

```yaml
InstitutionalKnowledgeRef:
  knowledge_id: string
  knowledge_type:
    - playbook
    - client_preference
    - expert_heuristic
    - clause_position
    - negotiation_pattern
    - litigation_strategy_pattern
    - risk_tolerance_rule
    - drafting_standard
    - review_checklist
  scope:
    practice_area: string | null
    client_id: string | null
    jurisdiction: string | null
    matter_type: string | null
    task_class: string | null
  authority_level:
    - draft
    - reviewed
    - approved
    - deprecated
  provenance:
    source_refs: [string]
    source_hashes: [string]
    captured_from: string | null
    captured_at: timestamp
    approved_by: string | null
    approved_at: timestamp | null
  reuse_rules:
    allowed_tasks: [string]
    forbidden_tasks: [string]
    requires_human_review: boolean
    expiration_policy: string
    stale_after: date | null
  governance:
    promotion_decision_ref: string | null
    supersedes: string | null
    superseded_by: string | null
```

---

## 3. Authority levels

| Level | Meaning | Allowed use |
|---|---|---|
| draft | Captured but not reviewed | Research or internal analysis only |
| reviewed | Checked by appropriate reviewer | May inform Legal Context Bundles with review flag |
| approved | Promoted through governance | May be used as approved institutional knowledge |
| deprecated | No longer current | Must not be used except for historical analysis |

---

## 4. Required provenance

Every institutional knowledge item must preserve:

- source reference;
- source hash where possible;
- capture date;
- capture method;
- reviewer identity or role;
- approval decision if any;
- scope;
- expiration or stale-after policy.

Do not encode institutional knowledge from memory alone unless it is clearly marked as draft and unsupported.

---

## 5. What must not be encoded as approved knowledge

Do not encode these as approved institutional knowledge without governed review:

- one-off attorney preference;
- stale client instruction;
- model-generated summary;
- litigation anecdote;
- unsupported “this is how we do it” claim;
- practice folklore;
- unverified template;
- unapproved negotiation position;
- confidential information outside allowed scope.

---

## 6. Legal Knowledge Runtime responsibilities

The Legal Knowledge Runtime may retrieve and attach institutional knowledge references to Legal Context Bundles.

It must preserve authority level, scope, and provenance.

It must not silently upgrade draft or reviewed knowledge to approved knowledge.

---

## 7. Skills Registry responsibilities

Any skill that consumes institutional knowledge must declare:

- accepted knowledge types;
- accepted authority levels;
- whether it can use draft knowledge;
- whether human review is required;
- how it preserves knowledge references;
- whether it emits derived knowledge;
- how derived knowledge is marked as non-canonical.

---

## 8. Exception Lake responsibilities

Exception Lake should record institutional-knowledge defects, including:

- stale institutional knowledge used;
- wrong scope used;
- unapproved knowledge treated as approved;
- missing provenance;
- reviewer correction to institutional knowledge;
- repeated conflict between practice groups or reviewers;
- client preference mismatch.

These records are evidence only and do not mutate canon.

---

## 9. Short form

> Institutional knowledge becomes valuable only when it is scoped, sourced, reviewed, reusable, and governable. Otherwise it is just folklore in a model prompt.
