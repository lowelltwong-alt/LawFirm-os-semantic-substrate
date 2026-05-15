# CI Test Router Architecture Notes

## Design intent

The CI Test Router is a small deterministic control-plane service implemented as local Python scripts. It is not a new runtime plane. It exists to keep LawFirm OS safe and efficient as validators grow.

The router mirrors the LawFirm OS architecture:

- Semantic Substrate owns canonical routing policy.
- Runtime repos declare local test inventories.
- Exception Lake remains evidence-only.
- Orchestrator remains execution-only.
- Skills Registry remains skill-definition inventory only.

## Why a router

Running every validator and every repo's full test suite on every small change will become expensive and may encourage bypassing tests. The router keeps a cheap always-on layer while routing larger checks only when the change surface requires them.

## Why a graph

The graph is not only a code import graph. It is a governance graph:

```text
Semantic Substrate -> Orchestrator -> Exception Lake
Semantic Substrate -> Legal Knowledge Runtime -> Orchestrator adapter
Semantic Substrate -> Skills Registry
Semantic Substrate -> CI router and AI front door
```

A Semantic Substrate registry change can affect every repo. A source-only Legal Knowledge Runtime parser change usually should not run Skills Registry security tests. A contract lock change should run contract drift checks and affected consumers.

## New test artifact contract

A test artifact is any executable or evaluable test surface in any language or framework. It must declare what it protects, what should trigger it, and what it must not claim authority over.

This prevents low-level agents from adding tests that pass locally but are invisible to CI routing.

## Review guidance for Codex/Claude

When reviewing this patch, check:

1. Is routing authority centralized in Semantic Substrate?
2. Do runtime repos only declare local manifests?
3. Are test artifacts registered in language-agnostic form?
4. Do protected surfaces route to preservation/governance validators?
5. Does unknown input fail closed?
6. Can a new repo enter silently? It should not.
7. Can a new test enter silently? It should not.
