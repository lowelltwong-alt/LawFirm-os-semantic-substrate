# Legal Knowledge Runtime Boundary

## Role

The Legal Knowledge Runtime is the governed document-ingestion, retrieval, and context-bundle runtime for LawFirm OS.

It may:

- validate legal document ingestion manifests;
- parse and normalize document structure;
- build derived metadata, lexical, document-tree, vector, graph, and compiled-bundle indexes;
- assemble Legal Context Bundles;
- emit legal retrieval traces and runtime records;
- emit candidate-only improvement signals to the Exception Lake.

It must not:

- define canonical legal meaning;
- create or mutate `route_id`, `event_class`, schemas, registries, or governance doctrine;
- write directly to the Semantic Substrate;
- store full real-client document payloads in Exception Lake;
- bypass matter, privilege, confidentiality, or retention labels;
- treat a retrieved bundle as legal advice or final work product.

## Runtime unit

The main unit is the **Legal Context Bundle**.

A bundle is task-shaped context assembled from approved retrieval primitives and supported by a retrieval trace. It is runtime evidence, not canon.

## Retrieval primitives

Legal Knowledge Runtime may combine:

- metadata retrieval,
- lexical retrieval,
- document-tree retrieval,
- vector retrieval,
- graph retrieval,
- compiled-bundle reuse.

No primitive is privileged by default. The retrieval plan selects primitives according to the bundle contract.

## Required gates

Every ingestion and retrieval path must pass:

1. synthetic or approved-data gate;
2. access-policy gate;
3. privilege/confidentiality gate;
4. parser/index profile gate;
5. evidence-trace completeness gate;
6. human-review gate when legal finality or protected content is involved.
