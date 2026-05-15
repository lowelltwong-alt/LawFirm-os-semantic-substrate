# Contract Surface Locking Architecture

## Problem

Whole-repo commit locks create recursion when the Semantic Substrate also stores evidence about lock bumps. Committing a managed-patch decision after updating consumer locks advances the Substrate HEAD, which makes those consumer locks stale again.

## Design

Consumers now use a two-part model:

```json
{
  "contract_sha": "<substrate repo commit used as provenance>",
  "contract_surface_lock": {
    "surface_id": "lawfirm_os_semantic_substrate.consumer_contract_surface.v1",
    "surface_sha256": "<hash of included contract files only>",
    "surface_registry_path": "registry/contract-surface-registry.json",
    "hash_algorithm": "lawfirm_os_contract_surface_sha256.v1"
  }
}
```

When `contract_surface_lock` is present, consumers validate the surface digest. The repo commit remains useful for provenance, but later excluded evidence/audit commits do not break consumers.

## Hash algorithm

The v1 algorithm sorts all included file paths, computes each file's SHA-256 digest, and then hashes the ordered triples of path, file digest, and file size. The selected files are controlled by `registry/contract-surface-registry.json`.

## Contract-surface versus evidence-surface

| Surface | Examples | Consumer lock impact |
|---|---|---|
| Contract authority | schemas, registries, contract exports, boundary governance | Changes require lock refresh |
| Evidence/audit | managed-patch decisions, reports, review notes, tests, scripts | Changes do not require lock refresh unless explicitly included |

## Rollout path

1. Add the Substrate contract-surface registry and scripts.
2. Commit the Substrate contract-surface registry.
3. Compute surface hash from the committed Substrate tree.
4. Update consumers to include `contract_surface_lock`.
5. Update consumer loaders to validate surface hashes instead of only exact Substrate HEAD.
6. After this, managed-patch decisions may be committed without recursively invalidating consumer locks.
