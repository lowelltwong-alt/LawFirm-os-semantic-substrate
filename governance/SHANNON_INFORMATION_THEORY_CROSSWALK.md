---
artifact: true
artifact_type: technical_crosswalk
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

# Shannon Information Theory Crosswalk — LawFirm OS

**Plane:** Semantic Substrate / companion reference  
**Applies to:** context-quality metrics, Legal Knowledge Runtime, Orchestrator context admission, Exception Lake analytics, Skills Registry trust scoring  
**Parent doctrine:** `AI_STRATEGY_DOCTRINE.md`

**Companion note:** `docs/architecture/SHANNON_INFORMATION_THEORY_AND_SEMANTIC_AUTHORITY.md` covers the **substrate-internal architecture** angle — why the control plane sits upstream of runtimes, and how the data-processing inequality formalizes the mutation boundary so downstream evidence cannot rewrite canon. This file covers the **governance / metrics-discipline** angle — which entropy-style metrics may be used, with caveats and forbidden uses. The two are complementary, not duplicative; neither is canonical until promoted through the Semantic Substrate governance process.

---

## 1. Purpose

This file explains how Shannon Information Theory may inform LawFirm OS without turning information theory into decorative or misleading governance language.

Shannon concepts are useful for engineering uncertainty, noise, redundancy, compression, and information gain.

They do not prove legal truth.

---

## 2. Core caveat

```text
Entropy metrics are not legal truth metrics.
Low entropy does not mean correctness.
High confidence can still be wrong.
Information gain means uncertainty reduction inside a defined measurement model, not proof of legal validity.
```

Any entropy metric used in LawFirm OS must declare:

- variable being measured;
- candidate set;
- probability distribution or estimator;
- data source;
- sample size if applicable;
- calibration method;
- intended operational decision;
- known limitations.

---

## 3. Shannon concept crosswalk

| Shannon concept | Engineering meaning | LawFirm OS translation | Valid use | Risk |
|---|---|---|---|---|
| Entropy `H(X)` | Expected uncertainty over a variable | Uncertainty over route, issue, source reliability, privilege status, or context class | Use when candidate set and probabilities are explicit | False precision if probabilities are guessed |
| Conditional entropy `H(X|C)` | Remaining uncertainty after context | Uncertainty after Legal Context Bundle assembly | Compare before/after context assembly | Can imply certainty where none exists |
| Information gain | Reduction in uncertainty | Difference between prior uncertainty and post-context/post-review uncertainty | Measure usefulness of context assembly | Not a truth measure |
| Mutual information | Shared information between variables | Relationship between source features and reviewer labels | Feature selection or routing diagnostics | Correlation mistaken for causation |
| KL divergence | Difference between probability distributions | Drift between model confidence distributions, route distributions, or reviewer outcomes | Drift detection | Sensitive and asymmetric |
| Jensen-Shannon divergence | Stable symmetric distribution difference | Safer distribution comparison for context/model drift | Compare route or defect distributions across versions | Still not a legal-validity metric |
| Cross-entropy | Predictive distribution quality | Model/classifier penalty when expected label differs from actual label | Classifier evaluation | Requires labels |
| Brier score | Calibration of probabilistic predictions | Whether confidence matches reviewer outcomes | Confidence calibration | Requires enough labeled cases |
| Expected calibration error | Confidence calibration by buckets | Whether high-confidence predictions are actually correct at expected rates | Calibration dashboard | Can hide cohort problems |
| Rate-distortion | Compression with bounded loss | Context summarization under token/risk budget | Summary loss checks | Hard to formalize in legal meaning |
| Information bottleneck | Keep relevant information, discard noise | Context selection before model call | Context-admission design | May discard legally important edge facts |
| Minimum description length | Prefer compact explanation that preserves signal | Summary discipline and duplicate reduction | Avoid bloated context | Over-compression risk |

---

## 4. Recommended first metrics

Start with practical metrics before advanced math:

| Metric | Definition | Owner | MVP use |
|---|---|---|---|
| Context completeness score | Required context fields present / required fields | Legal Knowledge Runtime | Admit/escalate context bundle |
| Provenance score | Claims with source references / material claims | Legal Knowledge Runtime | Block unsupported context |
| Source conflict count | Number of unresolved conflicting claims | Legal Knowledge Runtime / Exception Lake | Escalate review |
| Staleness count | Number of expired or stale source refs | Legal Knowledge Runtime | Refresh or mark stale |
| Reviewer correction rate | Corrected bundles / reviewed bundles | Exception Lake | Improve context assembly |
| High-confidence error rate | High-confidence outputs later rejected | Exception Lake / Orchestrator | Calibration defect |
| Context compression loss flag | Required facts missing after compression | Legal Knowledge Runtime | Prevent over-compression |

Only after those are stable should the system add formal entropy, mutual information, or divergence metrics.

---

## 5. Repo placement

| Repo | What belongs there |
|---|---|
| Semantic Substrate | Metric definitions, allowed metric IDs, schemas, governance caveats |
| Legal Knowledge Runtime | Metric calculation for Legal Context Bundles |
| Orchestrator | Gates that consume metric results; should not define metrics ad hoc |
| Exception Lake Runtime | Runtime observations, reviewer labels, calibration evidence, drift signals |
| Skills Registry | Skill context-discipline scoring and trust impact |

---

## 6. Forbidden uses

Do not use Shannon language to claim:

- a model answer is legally correct;
- a case strategy is optimal;
- a legal conclusion is proven;
- a low-entropy route is safe without review;
- institutional knowledge is canonical without approval;
- context compression preserved all legally material meaning without validation.

---

## 7. Required architecture language

Use this language:

```text
LawFirm OS may use entropy-inspired and information-theoretic metrics to measure uncertainty reduction, calibration, drift, and context compression quality. These metrics are bounded engineering measurements. They do not prove legal correctness, legal authority, or truth.
```

---

## 8. Short form

> Shannon helps LawFirm OS measure uncertainty and information flow. It does not turn AI output into truth.
