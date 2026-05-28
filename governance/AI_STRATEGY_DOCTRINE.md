# AI Strategy Doctrine — LawFirm OS

**Status:** proposed canonical governance doctrine
**Plane:** Semantic Substrate / control plane
**Applies to:** LawFirm OS repos, AI front-door routing, Orchestrator strategy, model/provider policy, skill trust plane
**Decision owner:** human governance / Semantic Substrate maintainers

---

## 1. Doctrine statement

LawFirm OS does not make a single-vendor AI bet.

Its strategy is to build the durable operating layer that retains value regardless of which AI company, model family, memory architecture, agent framework, local/cloud deployment pattern, token supplier, or skill ecosystem wins.

The durable layer is:

```text
canonical meaning
+ decision models
+ evidence packets
+ run ledgers
+ approval gates
+ policy registries
+ model/provider adapters
+ skill trust records
+ governed promotion paths
```

AI vendors, model providers, cloud services, local runtimes, memory tools, agent frameworks, MCP servers, skill marketplaces, and token suppliers are implementation surfaces. They may provide capability, speed, cost advantages, and tooling ergonomics, but they do not own semantic authority.

---

## 2. Why this is the strategy

The AI market is moving too quickly to make a durable architecture depend on one winner.

The strategically robust move is to preserve value under multiple futures:

| Future | LawFirm OS response |
|---|---|
| One dominant AI provider wins | Keep provider behind a ModelAdapter; retain semantic and audit authority internally. |
| Several frontier providers remain viable | Route by risk, cost, latency, data policy, eval performance, and availability. |
| Local models become good enough for many workflows | Use local runtimes for privacy, cost, resilience, and repeated low-risk work. |
| Cloud models remain best for hard reasoning | Use cloud models as bounded capability suppliers under policy and audit. |
| Hybrid local/cloud becomes normal | Keep transport and model policy adapterized. |
| Memory architecture changes | Keep record memory, working memory, and canonical memory distinct. |
| Token costs fall | Expect Jevons-style demand expansion; preserve token budgets and admission control. |
| Compute, memory, and energy constrain supply | Preserve vendor diversity, fallback paths, token efficiency, and workload triage. |
| Agent frameworks change | Keep run envelopes, evidence packets, approval records, and decision models portable. |
| Skill ecosystems expand | Treat skills as supply-chain artifacts requiring quarantine, scans, grading, approval, trust records, and revocation. |

---

## 3. Game-theory and strategy logic

### 3.1 Minimax regret

The architecture should minimize regret across uncertain AI futures.

The system should not over-optimize for one vendor, memory architecture, or framework if that creates high switching cost, weak bargaining power, or loss of institutional memory.

Decision rule:

```text
Prefer the option that preserves the most institutional value under the widest set of plausible AI futures.
```

### 3.2 Real-options value

Adapters, registries, pinned contracts, schemas, and evidence packets are not bureaucracy. They are options.

They preserve the right, but not the obligation, to switch:

- model vendor;
- runtime;
- memory store;
- skill provider;
- deployment location;
- tracing backend;
- approval workflow;
- storage substrate;
- evaluation harness.

### 3.3 Supplier power and token supply chain

At scale, AI vendors become part of a supply chain of tokens, latency, capacity, data-policy assurances, and model-specific capabilities.

LawFirm OS should manage that supply chain like any critical dependency:

- maintain alternatives;
- define vendor boundaries;
- track cost and availability;
- preserve evidence outside vendor dashboards;
- avoid semantic lock-in;
- avoid hidden hosted-tool dependency;
- keep local fallback where feasible.

### 3.4 Principal-agent risk

The human/user/legal institution is the principal. The AI agent is an agent with bounded delegated authority.

Therefore the system must track:

- who or what acted;
- on whose behalf;
- under which authority;
- with which evidence;
- inside which scope;
- with which approval;
- with which revocation path;
- with which audit trail.

### 3.5 Mechanism design

The system should create incentives and constraints that make safe behavior easier than unsafe behavior.

Required mechanisms:

- default-deny tool access;
- decision-model gates;
- evidence-completeness gates;
- human approval for irreversible or external actions;
- no canonical mutation from runtime;
- no unstated prompt authority;
- no vendor trace as system of record.

---

## 4. Durable-value layers

| Layer | What LawFirm OS owns | Why it remains valuable |
|---|---|---|
| Ontology | route IDs, event classes, work-product types, legal task classes, governance concepts | Meaning outlasts model vendors. |
| Decision models | decision owner, criteria, evidence minimums, thresholds, reversibility, escalation | Decisions become the bottleneck when AI output scales. |
| Evidence packets | proposed output, provenance, validation, contract lock, approval state | Lets humans decide faster without reconstructing context. |
| Run ledger | actions, actors, versions, tool calls, model calls, policy gates | Audit survives vendor and framework changes. |
| Adapters | ModelAdapter, AgentRuntimeAdapter, TransportAdapter, ExceptionSink, TraceSink | Keeps implementation replaceable. |
| Skill trust plane | skill discovery, quarantine, scanning, grading, trust records, revocation | Skills scale as a supply chain and attack surface. |
| Governance path | evidence → pressure vector → proposal → human approval → promotion | Runtime learning improves canon without bypassing accountability. |

---

## 5. Doctrinal rules

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

---

## 6. Required downstream behavior

### AI front door

The AI front door must route AI-strategy questions here before answering.

### Orchestrator

The Orchestrator must load strategy/decision doctrine as context when designing or changing model routing, harness selection, autonomy policy, tool permissions, or evidence-packet flow.

### Exception Lake

Exception Lake should capture decision defects, not just model defects:

- missing decision owner;
- ambiguous criteria;
- insufficient evidence;
- wrong approval path;
- threshold mismatch;
- automated action with low reversibility;
- decision latency;
- overproduction of weak proposals;
- human override patterns.

### Skills registry

Skills must declare:

- task class;
- decision points affected;
- evidence required;
- allowed autonomy level;
- required human gate;
- data scope;
- revocation path;
- trust status.

---

## 7. Short form

> Build the AI-era law-firm operating layer: vendor-agnostic semantics, explicit decision models, contract-locked execution, evidence-backed review, governed skills, and token-aware routing that survive vendor churn, Jevons-driven demand growth, and physical AI bottlenecks.
