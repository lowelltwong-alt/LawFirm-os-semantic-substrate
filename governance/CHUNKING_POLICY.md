# Chunking Policy

## Default policy

Use structure-aware chunking as the canonical default.

The default chunking strategy must derive chunks from canonical components and exact span selectors rather than from free-floating semantic windows.

## Canonical boundary source

Canonical chunk boundaries must follow normalized document structure:
- sections
- clauses
- paragraphs
- tables
- footnotes
- exhibits
- appendices

Chunking may group adjacent canonical components for retrieval convenience, but it may not redefine the underlying canonical component boundaries.

## Parent-child rule

Retrieve precise child units, but preserve parent context for reasoning and citation rendering.

That means a chunk may center on a clause or paragraph while still retaining its enclosing section path and parent context.

## Span traceability rule

Every chunk must carry:
- canonical component references
- exact span-selector references
- stable ordering within the chunk set

Grounded answers and evidence bundles must resolve back through those references to exact canonical spans.

## Experimental policy

Semantic chunking is experimental only.

It may be used as an applied retrieval strategy inside a chunk set, but:
- the canonical default remains `structure_aware`
- semantic chunking may not redefine canonical document boundaries
- semantic experiments must still anchor every chunk to canonical components and spans

## Regeneration rule

Chunk sets, embeddings, and indexes are rebuildable derivatives.

Embedding upgrades, reranker changes, and index profile migrations must not require canonical document redefinition or reparsing when the canonical source structure has not changed.

## Migration rule

Index migration plans must reuse canonical source structure and stable chunk lineage.

A new index build may change ranking behavior or operational performance, but it must not become a hidden source of truth for document boundaries.
