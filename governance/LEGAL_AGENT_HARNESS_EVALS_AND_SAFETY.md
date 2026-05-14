# Legal Agent Harness Evals and Safety Doctrine

## Purpose

This doctrine adds research-driven guardrails for Legal Knowledge Runtime and Orchestrator integrations.

## Research-driven changes

Recent agent-system research reinforces five operating rules:

1. Evaluate the **agent system/harness**, not the base model alone.
2. Treat eval design as adversarial when agents can browse, run tools, or inspect public materials.
3. Use a single manager by default; add subagents only where work is genuinely parallelizable.
4. Protect legal documents against silent corruption during delegated workflows.
5. Separate working memory from record memory.

## Working memory vs. record memory

**Working memory** may include ephemeral plans, retrieval hits, temporary summaries, current hypotheses, and intermediate bundle assembly state.

**Record memory** includes source documents, signed artifacts, matter facts, approved templates, normalized citations, approval decisions, and immutable evidence references.

Working memory is never canonical. Record memory is the source used for legal-grade review and evidence.

## Required eval posture

Legal Knowledge Runtime changes should add or update synthetic/private eval fixtures when they change retrieval, document structure, context bundle assembly, safety checks, or evidence packet semantics.

Public benchmark performance is not enough. Internal evals should include adversarial cases such as:

- prompt injection text inside retrieved documents;
- stale or overruled authority;
- missing schedules or exhibits;
- conflicting definitions;
- lookalike parties;
- cross-matter decoys;
- fabricated citation traps;
- document integrity degradation.

## Promotion rule

Runtime evidence may create proposals. It may not mutate canonical schemas, registries, policies, document types, bundle types, or guardrail doctrine without governed Semantic Substrate review.
