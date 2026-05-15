# CI Test Routing Boundary

## Purpose

The LawFirm OS CI Test Router is the deterministic gate that decides which validators and tests must run for a change. It reduces compute by routing work to affected tests, while preserving governance-grade fail-closed behavior.

This follows a graph-aware affected-test model: changed files are mapped to architecture surfaces, repos, and downstream dependencies before tests are selected. The router is inspired by mature affected-project CI patterns, but it is adapted for LawFirm OS governance rather than a generic monorepo.

## Authority

The **Semantic Substrate** owns:

- the canonical CI route registry;
- the test architecture registry;
- test artifact metadata schemas;
- repo onboarding rules;
- the final route verifier.

Runtime repos own only their local `ci-test-manifest.json` inventory. They must not define central routing policy.

## Core rule

Every test artifact in any language or framework must be registered in the owning repo's `ci-test-manifest.json` or explicitly excluded with a reason.

This includes pytest, unittest, Jest, Vitest, Playwright, Go tests, Rust tests, Java tests, .NET tests, shell smoke tests, Bats tests, schema tests, golden-file tests, contract tests, workflow tests, security tests, and eval suites.

## Routing hierarchy

1. Always run cheap discovery/registration checks.
2. Classify changed files into change classes.
3. Map change classes to architecture surfaces and risk tiers.
4. Select validators and repo-local tests from `ci-test-manifest.json`.
5. Run cross-repo validators only when cross-repo surfaces changed.
6. Run full workspace regression only for protected/broad/router changes or scheduled runs.
7. Verify selected checks actually ran.

## Fail-closed rules

The router must fail closed when:

- a new repo appears without repo registry membership;
- a new test artifact appears without manifest registration;
- a test declares an unknown language/framework;
- a runtime repo claims canonical routing authority;
- a protected change is not routed to preservation/governance validators;
- a route decision requires a validator/test that did not run.

## New repo rule

A new `LawFirm-os-*` repo must include:

- `README.md`;
- `AGENTS.md`;
- `AI_WORK_START_HERE.md`;
- `skill-agent-manifest.json`;
- `ci-test-manifest.json`.

If it has no tests yet, `ci-test-manifest.json` must include `no_tests_yet_rationale` and `temporary_until`.

## Human and Codex review

Protected changes require Codex/human review when they touch governance, schemas, registries, contract locks, AI instructions, test router policy, or destructive file operations.

## Cross-references

Authoritative artifacts for this boundary, all owned by Semantic Substrate:

- Architecture notes: `docs/CI_TEST_ROUTER_ARCHITECTURE.md`
- Schemas:
  - `schemas/ci-test-route-decision.schema.json`
  - `schemas/repo-ci-test-manifest.schema.json`
  - `schemas/test-artifact-metadata.schema.json`
- Registries:
  - `registry/ci-test-route-registry.json`
  - `registry/test-architecture-registry.json`
  - `registry/test-framework-adapter-registry.json`
- Scripts:
  - `scripts/route_ci_tests.py`
  - `scripts/validate_ci_route_decision.py`
  - `scripts/discover_test_artifacts.py`
  - `scripts/validate_test_artifact_registration.py`
  - `scripts/validate_new_repo_ci_onboarding.py`
- Tests:
  - `tests/test_ci_test_routing.py`
  - `tests/test_test_artifact_registration.py`

Every active LawFirm-os-* repo carries a local `ci-test-manifest.json` declaring its test artifacts. Local manifests are inventory only; they are not routing authority.
