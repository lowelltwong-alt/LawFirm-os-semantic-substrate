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

# AI Strategy Doctrine — LawFirm OS

**Plane:** Semantic Substrate / control plane  
**Applies to:** LawFirm OS repos, AI front-door routing, Orchestrator strategy, model/provider policy, Legal Knowledge Runtime, skill trust plane, context-quality workflows, evidence workflows  
**Decision owner:** human governance / Semantic Substrate maintainers  
**Companion files:**  
- `STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md`
- `SHANNON_INFORMATION_THEORY_CROSSWALK.md`
- `CONTEXT_QUALITY_DOCTRINE.md`
- `INSTITUTIONAL_KNOWLEDGE_ENCODING_STANDARD.md`

---

## 1. Doctrine statement

LawFirm OS does not make a single-vendor AI bet.

Its strategy is to build the durable operating layer that retains value regardless of which AI company, model family, memory architecture, agent framework, local/cloud deployment pattern, model/compute/token-capacity supplier, or skill ecosystem wins.

The durable layer is:

```text
canonical meaning
+ decision models
+ legal context bundles
+ evidence packets
+ run ledgers
+ approval gates
+ policy registries
+ model/provider adapters
+ skill trust records
+ governed promotion paths
```

AI vendors, model providers, cloud services, local runtimes, memory tools, agent frameworks, MCP servers, hosted tools, tracing systems, skill marketplaces, and model/compute/token-capacity suppliers are implementation surfaces.

They may provide capability, speed, cost advantages, and tooling ergonomics, but they do not own semantic authority.

---

## 2. Strategic thesis

The durable advantage in AI is not access to the best model. It is the quality of the context that can be safely, lawfully, and repeatedly fed into models and workflows.

For LawFirm OS, durable AI advantage comes from:

- structured data;
- clean matter records;
- properly encoded institutional knowledge;
- clear decision models;
- provenance-rich evidence;
- policy-bound context assembly;
- reusable legal work patterns;
- governed feedback loops.

The system should preserve value under multiple futures:

| Future | LawFirm OS response |
|---|---|
| One dominant AI provider wins | Keep provider behind a `ModelAdapter`; retain semantic and audit authority internally. |
| Several frontier providers remain viable | Route by risk, cost, latency, data policy, eval performance, and availability. |
| Local models become good enough for many workflows | Use local runtimes for privacy, cost, resilience, and repeated low-risk work. |
| Cloud models remain best for hard reasoning | Use cloud models as bounded capability suppliers under policy and audit. |
| Hybrid local/cloud becomes normal | Keep transport and model policy adapterized. |
| Memory architecture changes | Keep record memory, working memory, context bundles, and canonical memory distinct. |
| Token costs fall | Expect Jevons-style demand expansion; preserve token budgets and admission control. |
| Compute, memory, and energy constrain supply | Preserve vendor diversity, fallback paths, token efficiency, and workload triage. |
| Agent frameworks change | Keep run envelopes, evidence packets, legal context bundles, approval records, and decision models portable. |
| Skill ecosystems expand | Treat skills as supply-chain artifacts requiring quarantine, scans, grading, approval, trust records, and revocation. |
| Proprietary institutional context becomes the main AI moat | Govern context quality, provenance, permissioning, and institutional knowledge encoding before model execution. |

---

## 3. Strategic reference pattern: proprietary context as AI advantage

A major emerging pattern in legal AI is the large capital commitment to proprietary AI platforms built around internal knowledge capture, dedicated technologists, senior-lawyer input, restricted vendor reuse, and direct ownership of context infrastructure.

LawFirm OS treats proprietary context as a strategic pattern to evaluate through governance, not as a mandate to build a monolithic proprietary platform.

The lesson is:

```text
The moat is not the model.
The moat is governed proprietary context.
```

The risk is that proprietary platforms can become expensive bespoke technology failures if they fail to encode judgment, preserve provenance, survive expert mobility, control data quality, or adapt as foundation models commoditize.

Therefore, LawFirm OS should pursue proprietary context through modular, governed, evidence-backed architecture rather than through an uncontrolled all-in platform bet.

See: `STRATEGIC_REFERENCE_PROPRIETARY_CONTEXT.md`.

---

## 4. Strategy logic

### 4.1 Minimax regret

The architecture should minimize regret across uncertain AI futures.

The system should not over-optimize for one vendor, memory architecture, model family, hosted tool stack, or framework if that creates high switching cost, weak bargaining power, or loss of institutional memory.

Decision rule:

```text
Prefer the option that preserves the most institutional value under the widest set of plausible AI futures.
```

### 4.2 Real-options value

Adapters, registries, pinned contracts, schemas, legal context bundles, and evidence packets are not bureaucracy. They are options.

They preserve the right, but not the obligation, to switch model vendors, runtimes, memory stores, context-assembly systems, skill providers, deployment locations, tracing backends, approval workflows, storage substrates, and evaluation harnesses.

### 4.3 Supplier power and AI capacity supply chain

At scale, AI vendors become part of a supply chain of compute, tokens, latency, capacity, data-policy assurances, and model-specific capabilities.

LawFirm OS should manage that supply chain like any critical dependency:

- maintain alternatives;
- define vendor boundaries;
- track cost and availability;
- preserve evidence outside vendor dashboards;
- avoid semantic lock-in;
- avoid hidden hosted-tool dependency;
- keep local fallback where feasible;
- keep context and institutional knowledge portable.

### 4.4 Principal-agent risk

The human/user/legal institution is the principal. The AI agent is an agent with bounded delegated authority.

Therefore the system must track who or what acted, on whose behalf, under which authority, with which evidence, inside which scope, using which context bundle, with which approval, with which revocation path, and with which audit trail.

### 4.5 Mechanism design

The system should create incentives and constraints that make safe behavior easier than unsafe behavior.

Required mechanisms:

- default-deny tool access;
- decision-model gates;
- context-quality gates;
- evidence-completeness gates;
- human approval for irreversible or external actions;
- no canonical mutation from runtime;
- no unstated prompt authority;
- no vendor trace as system of record;
- no ungoverned institutional-knowledge capture.

---

## 5. Durable-value layers

| Layer | What LawFirm OS owns | Why it remains valuable |
|---|---|---|
| Ontology | route IDs, event classes, work-product types, legal task classes, governance concepts | Meaning outlasts model vendors. |
| Decision models | decision owner, criteria, evidence minimums, thresholds, reversibility, escalation | Decisions become the bottleneck when AI output scales. |
| Legal Context Bundles | structured matter facts, source references, institutional knowledge references, permission labels, freshness metadata, uncertainty indicators | Context quality becomes the durable advantage before model execution. |
| Evidence packets | proposed output, provenance, validation, contract lock, approval state | Lets humans decide faster without reconstructing context. |
| Run ledger | actions, actors, versions, tool calls, model calls, policy gates | Audit survives vendor and framework changes. |
| Adapters | `ModelAdapter`, `AgentRuntimeAdapter`, `TransportAdapter`, `ExceptionSink`, `TraceSink`, `ContextProvider` | Keeps implementation replaceable. |
| Skill trust plane | skill discovery, quarantine, scanning, grading, trust records, revocation | Skills scale as a supply chain and attack surface. |
| Governance path | evidence → pressure vector → proposal → human approval → promotion | Runtime learning improves canon without bypassing accountability. |

---

## 6. Context-quality doctrine

LawFirm OS treats context quality as a first-class control objective.

The pre-model unit is the **Legal Context Bundle**. The post-model unit is the **Evidence Packet**.

Legal Context Bundles should contain structured matter facts, source references, claim-level provenance, institutional knowledge references, permission and privilege labels, freshness metadata, uncertainty indicators, context-quality scores, and contract/manifest references.

The Legal Knowledge Runtime should assemble context bundles under contracts defined by the Semantic Substrate.

The Orchestrator should admit, reject, or escalate context bundles before model execution.

The Exception Lake should record context defects, reviewer corrections, and observed information-gain evidence as runtime evidence only.

The Skills Registry should grade skills partly by whether they preserve provenance, obey permission boundaries, and reduce review burden without creating semantic drift.

See: `CONTEXT_QUALITY_DOCTRINE.md`.

---

## 7. Shannon and uncertainty doctrine

Shannon Information Theory is useful for LawFirm OS as an engineering discipline for uncertainty, noise, compression, channel capacity, redundancy, and information gain.

It must not be misused as a claim that the system can mathematically prove legal truth.

Required caveat:

```text
Entropy metrics are not legal truth metrics.
Low entropy does not mean correctness.
High confidence can still be wrong.
Information gain means uncertainty reduction inside a defined measurement model, not proof of legal validity.
```

Entropy-inspired metrics may be used only where the variable, candidate set, estimator, data source, and calibration status are explicit.

Do not use Shannon language as decorative math.

See: `SHANNON_INFORMATION_THEORY_CROSSWALK.md`.

---

## 8. Repository responsibilities

### 8.1 Semantic Substrate

Owns canonical definitions for strategy doctrine, decision models, model/provider policy, context-quality schemas, Legal Context Bundle schema, entropy or uncertainty metric registry, institutional knowledge reference schema, skill trust schema, governance boundaries, and promotion rules.

Must not store runtime matter payloads, model outputs, agent execution state, or Exception Lake evidence as canon.

### 8.2 Legal Knowledge Runtime

Assembles Legal Context Bundles under Semantic Substrate contracts.

Responsible for matter-record normalization, source-reference handling, claim-level provenance, institutional knowledge resolution, context-quality scoring, uncertainty profiling, context compression, freshness checks, and permission/privilege labels.

Must not promote institutional knowledge to canon without governed approval.

### 8.3 Orchestrator

Executes bounded workflows under control-plane authority.

Responsible for model routing, harness selection, autonomy policy, tool permissions, context admission gates, evidence-packet flow, skill invocation, approval behavior, and run ledgers.

Must not invent canonical schemas, route IDs, event classes, or decision doctrine.

### 8.4 Exception Lake Runtime

Stores append-only runtime evidence.

May derive learning candidates or pressure vectors, but those remain runtime evidence until governed promotion.

### 8.5 Skills Registry

Skills must declare task class, decision points affected, context types accepted, forbidden context types, evidence required, provenance behavior, allowed autonomy level, required human gate, data scope, revocation path, trust status, and context-discipline score or equivalent trust measurement.

No skill should be approved if it cannot preserve source references, obey data boundaries, and emit audit-ready results.

---

## 9. Doctrinal rules

1. **Model output is proposal, not decision.**
2. **Runtime evidence is evidence, not canon.**
3. **Decision models are control-plane artifacts.**
4. **The Orchestrator executes decision models; it does not invent them.**
5. **A provider may supply capability but cannot become semantic authority.**
6. **Cheaper inference increases demand; token efficiency remains strategic.**
7. **AI automation increases the value of explicit decision rights.**
8. **Legal work should be decomposed before it is automated.**
9. **The system should optimize for accepted decisions, not generated outputs.**
10. **When uncertainty is high, preserve optionality.**
11. **Context quality is a first-class control objective.**
12. **Legal Context Bundles are pre-model context artifacts; Evidence Packets are post-model evidence artifacts.**
13. **Entropy and information-gain metrics are bounded engineering measurements, not legal-truth claims.**
14. **Institutional knowledge must be encoded with provenance, authority level, scope, and review status.**
15. **No skill, model, or agent may strip provenance or expand authority silently.**

---

## 10. Operating implications

LawFirm OS should optimize for accepted decisions per reviewer hour, reduced reviewer rework, lower defect recurrence, higher first-pass validation, better provenance completeness, calibrated confidence, lower context noise, portable institutional knowledge, and lower switching cost across vendors and frameworks.

It should not optimize for raw model output volume, agent count, number of model calls, prompt complexity, dashboard count, vendor-specific trace depth, tool breadth, or uncontrolled automation rate.

---

## 11. Short form

> Build the AI-era law-firm operating layer: vendor-agnostic semantics, explicit decision models, governed proprietary context, contract-locked execution, evidence-backed review, governed skills, and token-aware routing that survive vendor churn, Jevons-driven demand growth, physical AI bottlenecks, framework churn, and foundation-model commoditization.
