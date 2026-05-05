# Repo Ingest and Alignment Prompts

## Deep Repo Ingest Prompt

You are reading a repository that is designed as a governed, layered semantic system rather than a generic codebase or simple RAG stack.

Your task is to understand and explain the repository on its own terms before suggesting changes.

Read the repo in this order:
1. README
2. docs/architecture/PROJECT_SYSTEM_MAP.md
3. docs/architecture/CANONICAL_SPINE_AND_VALIDATION_MODEL.md
4. docs/architecture/8_LAYER_DNA_ADDRESS_MODEL.md
5. docs/roadmap/MASTER_ROADMAP.md
6. docs/roadmap/PHASE_DEPENDENCY_MAP.md
7. docs/governance/REPO_OPERATING_MODEL.md
8. sponsor and pilot docs under docs/poc/
9. validation, schema, graph, and standards artifacts

As you read, explain:
- the canonical spine
- the validation path
- the reason for additive rather than replacement growth
- the role of the 8-layer DNA address model
- the substrate, semantic stack, and sponsor layers
- the key design decisions and why they were made
- what is core architecture versus bounded pilot packaging

Important constraints:
- do not flatten the project into a generic ontology, generic graph, or generic RAG system
- do not propose replacing substrate-native operating semantics with external standards
- do not treat derived graph or retrieval artifacts as canonical truth
- do not ignore the repo's governance and validation posture

Your output should include:
1. end-to-end architecture explanation
2. current design authority and control points
3. reusable subsystems
4. repo-specific assumptions
5. safest next steps if building on top of it

## Reusable Pieces Extraction Prompt

You are analyzing this repository to identify which parts could be reused in another organization without copying the entire system.

Separate the project into:
- reusable architecture patterns
- reusable governance patterns
- reusable validation patterns
- reusable semantic graph patterns
- Law Firm-specific operating semantics
- pilot-specific implementation details

For each category, explain:
- what it is
- why it exists
- whether it is portable
- what would need to be adapted

## Alignment Cleanup Prompt

You are cleaning up and aligning this repository after multiple phases of design and buildout.

Your goal is to improve coherence without changing the architecture's design authority.

You must preserve:
- canonical spine first
- validation-aligned growth
- 8-layer DNA address discipline
- additive semantic stack posture
- substrate-native operating semantics as the design authority
- bounded pilot and sponsor-ready layers

You may improve:
- README guidance
- cross-links between docs
- reading order
- duplicate or stale explanations
- roadmap clarity
- terminology consistency

You must not:
- invent a parallel ontology system
- silently replace canonical concepts with generic ones
- collapse governance, validation, and retrieval into one layer
- rewrite the repository as if it were just a graph database or an Azure deployment template
