# Contract Surface Hash Spine

## Purpose

The contract surface hash spine is the explicit cross-repo authority compatibility gate for the LawFirm OS five-repo system. It binds the four runtime consumer repos to a single, content-addressed snapshot of the Semantic Substrate's contract authority surface, so that every cross-repo runtime object can carry a verifiable claim of "I was produced under this substrate contract."

This document codifies the rule already encoded in `registry/contract-surface-registry.json`, the `contract-surface-locking-patch` lineage, and the per-consumer `contracts.lock.json` files. It is the canonical reference for PR-01 of the LawFirm OS overnight roadmap.

## What the spine is

A single 64-character hex digest — `contract_surface_sha256` — computed by `lawfirm_os_contract_surface_sha256.v1` over the substrate's contract-authority files at a specific committed Git tree. The algorithm:

1. Reads the file list and exclusion patterns from the named surface in `registry/contract-surface-registry.json`.
2. Enumerates committed-tree blobs in the substrate at a pinned commit.
3. For each included blob: emits the relative path, the blob's sha256, and its byte length into a canonical ordering.
4. Returns `sha256(algorithm_id || surface_id || sorted_blob_records)`.

The surface intentionally excludes managed-patch decision records, audit/review files, reports, docs, tests, scripts, and local generated artifacts. Those are evidence, not authority — they must not force consumer lock churn.

## What each repo declares

| Repo | Role | What it does with the spine |
|---|---|---|
| `LawFirm-os-semantic-substrate` | authority | Owns the surface registry, the hash algorithm, and the canonical surface_sha256 at HEAD. |
| `LawFirm-os-orchestrator` | consumer | Pins `contracts.lock.json` `contract_surface_lock.surface_sha256` and refuses to operate if the pin does not validate against the substrate. |
| `LawFirm-os-exceptions-lake-runtime-main` | consumer | Same pin; refuses to admit evidence packets whose authority lock does not present this surface_sha256. |
| `LawFirm-os-legal-knowledge-runtime` | consumer (added in PR-01) | Same pin; refuses to emit source/claim/coverage/verification records under any other substrate authority. |
| `LawFirm-os-skills-registry` | consumer (added in PR-01) | Same pin; refuses to mint SkillTrustRecords under any other substrate authority. |

The spine is **content-addressed**, not commit-addressed. Two substrate commits can produce the same surface_sha256 if they differ only in excluded files (managed-patch decisions, audit records, etc.). Consumers therefore do not need to re-pin every time the substrate accepts a routine audit commit.

## Validation contract

A consumer's lock is valid iff:

1. `contract_surface_lock.surface_id` exists in the substrate's `contract-surface-registry.json`.
2. `contract_surface_lock.surface_registry_path` resolves to that registry on disk.
3. `contract_surface_lock.hash_algorithm` equals `lawfirm_os_contract_surface_sha256.v1`.
4. Recomputing the surface at `contract_surface_lock.computed_from_commit` against `contract_surface_lock.surface_id` reproduces `contract_surface_lock.surface_sha256` byte-for-byte.
5. Recomputing the surface at the substrate's current `HEAD` against the same `surface_id` ALSO reproduces `contract_surface_lock.surface_sha256`. If it does not, either (a) the substrate's surface has moved forward and consumers must refresh, or (b) the consumer's lock is stale.
6. No uncommitted surface-included file is dirty in the substrate working tree. (Uncommitted surface change without a refreshed lock is a guaranteed drift hazard.)

These checks are implemented by `scripts/validate_contract_lock_drift_workspace.py` (per-consumer drift) and the new `tests/test_contract_surface_spine.py` (cross-consumer agreement) added in PR-01.

## Cross-consumer agreement (added in PR-01)

All consumer locks present in the workspace **must agree** on:
- `contract_surface_lock.surface_sha256`
- `contract_surface_lock.surface_id`
- `contract_surface_lock.hash_algorithm`
- `contract_surface_lock.surface_registry_path`

They may differ on `generated_by`, `generated_at`, `manifest_first_loading.preferred_path`, and `non_claims`. They may also differ on `contract_sha` and `substrate_repo_commit_sha` if generated at different commits, **provided** each commit independently produces the same `surface_sha256` (which is the whole point of content-addressing).

The cross-repo agreement is what makes the five-repo OS one OS. A consumer that pins to a different `surface_sha256` than its siblings is, by definition, operating under a different substrate authority — and must be quarantined.

## Non-claims

This spine does not:
- Permit any consumer repo to mutate the Substrate.
- Permit any consumer repo to invent `route_id`, `event_class`, schema meaning, approval doctrine, or tool authority.
- Replace the per-object evidence chain (ContextBundle → ExecutionRequest → … → EvidencePacket → ExceptionLakeRecord). It is the **base** of that chain, not the chain itself.
- Permit silent consumer-lock advancement. Refresh requires running `scripts/update_consumer_contract_surface_locks.py` (or equivalent) and committing the result.

## Architecture-flow registry hookup (TODO PR-09)

PR-09 introduces the `architecture-flow-registry.json` that catalogs governed objects and their lifecycle ownership. When that lands, the `contract_surface_sha256` object will be registered as the root of the spine with ownership `semantic_substrate.control_plane`. Until PR-09, this governance document is the canonical reference.

## Related governance documents

- `governance/CONTRACT_SURFACE_LOCKING_BOUNDARY.md` — the lower-level rule about which substrate files are authority surface vs. evidence surface.
- `governance/CANONICAL_SPINE_POLICY.md` — the broader policy about canonical-vs-evidence separation.
- `governance/CONTEXT_BUNDLE_CONTRACT.md` *(planned in PR-02/03)* — the next object in the spine after `contract_surface_sha256`.
- `governance/EVIDENCE_PACKET_CONTRACT.md` *(planned in PR-05)* — the consumer-side carrier for the chained spine hashes.
- `governance/EXECUTION_PASSPORT.md` *(planned in PR-04)* — the runtime authority gate that every bounded action must clear.
