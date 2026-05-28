# Decision Bottleneck and Decision Model Doctrine

**Status:** proposed control-plane doctrine
**Plane:** Semantic Substrate
**Related:** AI strategy doctrine, AIRCA/LAIRCA supporting decision architecture, Orchestrator TOC, Exception Lake evidence model

---

## 1. Core thesis

As AI makes analysis, drafting, summarization, coding, classification, and retrieval cheaper, the bottleneck shifts from producing work to deciding what should happen next.

The durable constraint becomes:

```text
decision capacity
+ decision quality
+ decision accountability
+ decision latency
+ decision evidence
```

In LawFirm OS, decisions must be modeled explicitly.

A model may generate options. A tool may gather evidence. The Orchestrator may package the run. Exception Lake may preserve evidence. But the decision model defines what counts as enough, who owns the judgment, and what action is allowed.

---

## 2. Decision science interpretation

Decision intelligence treats information, analytics, and AI as inputs to action. The goal is not more data, more dashboards, more predictions, or more model output. The goal is better action under uncertainty.

LawFirm OS should therefore ask of every workflow:

1. What decision is being made?
2. Who owns it?
3. What alternatives exist?
4. What evidence is required?
5. What risk is tolerable?
6. What is reversible?
7. What requires human approval?
8. What is the cost of delay?
9. What is the cost of a wrong decision?
10. What runtime evidence should improve future decision models?

---

## 3. Susskind-style decomposition extended for LawFirm OS

Legal work should not be treated as one indivisible professional act.

Decompose in layers:

```text
matter
-> legal / operational workstream
-> task
-> work primitive
-> decision point
-> evidence requirement
-> authority gate
-> output / action
-> audit record
```

### Work primitives

| Primitive | Question |
|---|---|
| Ingest | What input enters the system? |
| Extract | What signal must be pulled from the input? |
| Transform | What format or structure is needed? |
| Evaluate | What criteria determine adequacy, risk, or correctness? |
| Synthesize | What recommendation, packet, or artifact is produced? |
| Dispatch | Where does it go, and what authority is required? |

### Decision overlay

Every primitive that can change outcome, risk, or authority needs a decision model.

Example:

```text
extract clause risk
-> decide risk class
-> decide evidence sufficiency
-> decide reviewer role
-> decide whether output is draft-only, client-visible, or blocked
```

---

## 4. Decision model object

A decision model is a structured control-plane artifact.

Minimum fields:

| Field | Meaning |
|---|---|
| `decision_model_id` | Stable identifier. |
| `decision_name` | Human-readable decision. |
| `decision_owner_role` | Who owns finality. |
| `task_class` | Workflow or task this decision applies to. |
| `decision_type` | route, classify, approve, escalate, automate, defer, reject, promote, source, spend, disclose, send, file. |
| `alternatives` | Allowed choices. |
| `criteria` | What must be evaluated. |
| `evidence_minimums` | Required evidence packet fields. |
| `risk_tier` | low, medium, high, protected. |
| `reversibility` | reversible, partially reversible, irreversible. |
| `stakes_size` | small, moderate, large, existential. |
| `autonomy_allowed` | none, recommend, draft, act-with-approval, act-autonomously. |
| `approval_required` | yes/no and approver role. |
| `latency_target` | how long the decision can wait. |
| `defect_modes` | ways the decision can fail. |
| `metrics` | how to measure decision quality and flow. |
| `promotion_path` | how the decision model changes. |

---

## 5. TOC mapping: decisions as the constraint

### Identify the constraint

The constraint is not usually model speed. It is the human/organizational ability to make accountable decisions from AI-produced proposals.

### Exploit the constraint

Make every decision easier:

- prevalidate route and event class;
- expose evidence sufficiency;
- show decision alternatives;
- show risk tier and reversibility;
- identify missing data;
- package the approval record;
- reduce rework.

### Subordinate everything else

Do not generate more outputs than decision capacity can absorb.

Subordinate model calls, agents, tools, queueing, dashboards, and automation to decision throughput.

### Elevate the constraint

Only elevate after measuring the decision bottleneck.

Possible elevation moves:

- better decision-model registry;
- clearer approval authority;
- better evidence packet structure;
- route-specific decision templates;
- decision-support UI;
- training / playbooks;
- escalation lanes;
- automated low-risk decisions with strong evals.

### Repeat

Once one decision bottleneck improves, the constraint may move to evidence gathering, approval latency, vendor capacity, compute, cost, or policy change management.

---

## 6. Drum-buffer-rope for decisions

| TOC concept | LawFirm OS interpretation |
|---|---|
| Drum | Sustainable rate of accountable decisions, not raw AI outputs. |
| Buffer | Prevalidated evidence packets and decision-ready queues. |
| Rope | Admission control: do not emit proposals unless they are decision-ready. |

Rope rule:

```text
No decision-request packet may enter review unless it has a decision_model_id, evidence_packet_id, route_id, risk_tier, reversibility class, and approval rule.
```

---

## 7. Decision defects

Decision defects must be stored in Exception Lake as first-class defects.

| Defect | Description | Default containment |
|---|---|---|
| Missing decision owner | No role has final authority. | Block or route to governance. |
| Ambiguous criteria | Decision depends on unstated judgment. | Needs review and model update. |
| Weak evidence | Required evidence is absent. | Hold until evidence is complete. |
| Wrong threshold | Decision standard too loose or too strict. | Flag for decision-model review. |
| Approval bypass | Protected decision made without required approval. | Hard fail. |
| Automation overreach | AI acted where only recommendation was allowed. | Revoke, audit, and incident-review. |
| Delay defect | Decision exceeded latency target. | Escalate queue and analyze bottleneck. |
| Overproduction | Too many weak packets crowd reviewer capacity. | Tighten rope/admission rules. |
| False precision | Model confidence substitutes for decision criteria. | Require decision criteria and evidence. |
| Reversibility mismatch | Irreversible action treated as reversible. | Hard fail and update policy. |

---

## 8. Game-theory interpretation

### Vendor game

If LawFirm OS embeds decisions in vendor prompts, the vendor captures institutional judgment. If it stores decisions in portable decision models, the firm keeps bargaining power.

### Attention game

When AI makes outputs abundant, human attention becomes scarce. Systems that flood decision-makers with weak proposals lose. Systems that ration attention with evidence-ready packets win.

### Signaling game

A decision model signals seriousness to reviewers, auditors, vendors, and future AI agents. It says: this is not a loose recommendation; this is a governed decision surface.

### Commitment game

Explicit decision models convert vague preferences into commitments:

- what the system may do;
- what it must not do;
- what evidence is enough;
- who must approve;
- what can change automatically;
- what requires promotion.

### Option game

The best strategy preserves optionality across model vendors and runtimes while committing strongly to internal decision records and semantic authority.

---

## 9. Required Orchestrator behavior

The Orchestrator must:

1. Load applicable decision model before model/tool execution when a decision is involved.
2. Record `decision_model_id` in run ledger and evidence packet.
3. Validate evidence minimums before review emission.
4. Escalate when decision criteria are incomplete.
5. Prevent autonomous action above allowed autonomy level.
6. Emit decision defects to Exception Lake.
7. Treat decision-model changes as substrate/governance changes, not runtime self-modification.

---

## 10. Short form

> AI scales outputs. LawFirm OS scales accountable decisions.
