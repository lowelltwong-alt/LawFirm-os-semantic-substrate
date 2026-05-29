---
artifact: true
artifact_type: technical_crosswalk
status: proposed
canon_status: not_canon_until_approved
authority: explanatory_only
review_cycle: 6 months
stale_after: 2026-11-29
---

# Shannon Information Theory and Semantic Authority

Status: Non-canonical concept note.
Authority: Explanatory only. Does not create schemas, IDs, policies, routes, registries, event classes, endpoint maps, or source-of-truth claims.

## BLUF

This substrate is the control plane: it owns ontology, evidence/provenance contracts, governance, and registries. Information theory provides a precise way to describe why the substrate must exist *upstream* of runtimes. Runtime systems transmit, transform, and consume signals over a noisy channel; the substrate is what preserves signal structure, source identity, and mutation boundary so downstream evidence cannot rewrite canon. The mathematics below clarify that property; they do not produce authority.

Conceptual lineage: this note draws on Shannon (1948), Cover & Thomas (*Elements of Information Theory*), and MacKay (*Information Theory, Inference, and Learning Algorithms*); see the **References** section. No file outside this repository is required to read this note.

## Boundary

This note does **not**:

- create canonical authority of any kind;
- modify any schema in `schemas/`, `schema/`, `registry/`, `governance/`, `ontology/`, or `manifests/`;
- introduce new route IDs, event classes, policy IDs, endpoint IDs, or `contracts.lock.json` entries;
- redefine the `exception-event -> pressure-vector -> adaptation-proposal -> promotion-decision` path;
- replace `AUTHORITY_MAP.yaml`, `governance/CROSS_REPO_MAP.md`, or any AI front door artifact;
- assert that runtime observations are canon. They remain evidence.

Where Shannon and substrate appear to conflict, substrate wins.

## Communication model

| Shannon layer | Substrate-local equivalent |
|---|---|
| Information source | Canonical ontology, registries, governance contracts, policy IDs, evidence/provenance schemas |
| Transmitter | `registry/` entries, schema files, manifest exports, `AUTHORITY_MAP.yaml`, AI front door |
| Channel | Cross-repo consumption: orchestrator manifest pinning, exceptions-lake contract loading, legal-knowledge contract reading |
| Noise | Schema drift, unpinned reads, stale clones, contract-lock omissions, undocumented registry mutations, ad-hoc field additions |
| Receiver | Consumer runtimes: orchestrator, exceptions-lake-runtime, legal-knowledge-runtime, skills-registry |
| Destination | Governed evidence packets, append-only ledgers, validation outcomes, promotion decisions |
| Redundancy | `contracts.lock.json`, `registry/schema-registry.json`, `registry/innovation-object-registry.json`, AUTHORITY_MAP, JSON-Schema validation, CROSS_REPO_MAP |
| Error correction | Governed promotion path (exception → pressure → proposal → decision), reclassification, schema migration with compatibility-preserving cleanup PRs |
| Channel capacity | Reviewer bandwidth, schema-validator throughput, contract-loading reliability, the discipline of mutation-boundary rules |

## Real math used

Notation:

- $X$ = source state (a fact about which schema, registry, or governance contract controls a downstream decision).
- $Y$ = what a consumer runtime actually observes after retrieval/validation.
- $Z$ = a downstream artifact (evidence packet, validation outcome, promotion decision).
- $\hat{X}$ = the runtime's reconstruction or classification of $X$.

### Entropy

```math
H(X) = -\sum_{x} p(x)\,\log_2 p(x)
```

Substrate interpretation:

- The substrate's job is to make $p(x)$ peaked and well defined for governance-relevant variables (which schema applies, which registry entry controls, which lifecycle state holds). High substrate entropy = many plausible canonical interpretations = governance failure.

### Conditional entropy

```math
H(X \mid Y) = -\sum_{x,y} p(x,y)\,\log_2 p(x \mid y)
```

Substrate interpretation:

- After a runtime retrieves and validates substrate contracts (the observed $Y$), residual uncertainty $H(X \mid Y)$ measures how much canonical ambiguity remains. Validation, AUTHORITY_MAP lookups, and registry pins are designed to reduce it.

### Mutual information

```math
I(X;Y) \;=\; H(X) - H(X \mid Y)
```

Substrate interpretation:

- A schema, registry entry, or manifest is valuable to a consumer runtime only insofar as it carries mutual information with the governance-relevant variable the runtime must decide on. Bloated contracts that do not reduce $H(X \mid Y)$ are pure overhead.

### Channel capacity

```math
C \;=\; \max_{p(x)} I(X;Y)
```

Substrate interpretation (analogy, not measurement):

- The cross-repo channel (substrate → consumer runtime) has a practical capacity. If consumers must absorb more contract surface than they can validate, the effective channel becomes noisy and runtimes start filling gaps with assumptions. The compatibility-preserving-cleanup-PR rule keeps the contract surface within capacity.

### Data processing inequality

If $X \to Y \to Z$ is a Markov chain:

```math
I(X;Z) \;\le\; I(X;Y)
```

Substrate interpretation (the most important one for this repo):

- A downstream evidence packet, validation outcome, or promotion-decision draft can carry **at most** as much information about the canonical source state as the substrate channel preserved upstream. No amount of downstream polish (orchestrator routing, exceptions-lake aggregation, legal-knowledge summarization) creates new canonical authority. This is exactly the substrate's mutation-boundary doctrine, expressed as a theorem.

### Optional, only if real distributions exist

```math
D_{\mathrm{KL}}(P \,\Vert\, Q) \;=\; \sum_{x} P(x)\,\log_2 \frac{P(x)}{Q(x)}
```

Substrate interpretation:

- *If* the substrate ever publishes empirical baselines (for example, baseline distribution over which schemas govern which exception classes), $D_{\mathrm{KL}}$ would be the natural measure of contract drift. **Today this is optional and data-dependent.** Do not invent a baseline to make the math look serious.

## Integration implications

These are conceptual implications, not new requirements:

1. **Mutation boundary is a coding bound, not a preference.** The data processing inequality makes it formal: no Markov-downstream artifact (evidence, summary, classifier output) can carry more canonical information than the upstream substrate channel transmitted. The boundary is the bound.
2. **`contracts.lock.json` is structured redundancy.** Pinning hashes/versions is exactly the role of a checksum / version anchor in coded transmission. It buys error detection at the cost of some duplication, which is the right tradeoff.
3. **AUTHORITY_MAP collapses uncertainty.** A consumer that resolves authority via AUTHORITY_MAP is reducing $H(X \mid Y)$. Skipping that resolution leaves higher residual entropy and increases the probability of a downstream classification error (Fano-style intuition).
4. **Phase 2 `schemas/` vs Phase 1 `schema/` is a channel-capacity choice.** Splitting by concern (`autonomy/`, `harness/`, `research/`, `innovation/`) keeps the contract surface inside reviewer/validator capacity. Flat lumping would have raised noise without adding mutual information.
5. **Generic hubs do not earn authority.** A registry entry that points everywhere reduces uncertainty about nothing in particular. Specificity is what mutual information rewards.

## Safe design questions

For each new substrate change a maintainer should be able to answer:

1. What is the authoritative source for this change (which existing registry, schema, or governance file)?
2. How is the change encoded so consumers can detect it (`contracts.lock.json`, registry version, schema id, AUTHORITY_MAP entry)?
3. Where can channel noise enter (unpinned reads, stale clones, undocumented field additions, mixed `schema/` vs `schemas/` references)?
4. Is the consumer surface still within capacity (can a runtime validate against the updated contracts without skipping)?
5. What independent redundancy detects regressions (registry validators, JSON-Schema validation, CROSS_REPO_MAP, AUTHORITY_MAP)?
6. What governed error-correction path covers this if a runtime observes a mismatch (exception → pressure → proposal → decision)?
7. What authority decides promotion of the change?

## Non-goals

- This note does not say Shannon math proves the substrate's design. The substrate's design comes from governance, not from theorems.
- This note does not introduce route entropy, mutual-information thresholds, or KL divergence as required runtime metrics. Any such metric must be proposed through the governed path, with real data, and with explicit acknowledgment that pseudo-probabilities are not probabilities.
- This note does not assert that Shannon, Kant, Spinoza, Logos, or any philosophical framework is a source of substrate authority. The substrate's authority is the substrate's authority.

## References

Conceptual only. No long copyrighted excerpts.

- Claude E. Shannon, "A Mathematical Theory of Communication," *Bell System Technical Journal*, 1948.
- Thomas M. Cover and Joy A. Thomas, *Elements of Information Theory*, Wiley.
- David J. C. MacKay, *Information Theory, Inference, and Learning Algorithms*, Cambridge University Press.
