# Contract Surface Locking Boundary

## Purpose

Contract surface locking prevents recursive consumer lock drift. Consumers should validate the part of the Semantic Substrate that defines their canonical authority, not every audit or decision record committed to the Substrate repository.

## Boundary rule

The Semantic Substrate owns the contract-surface registry and hash algorithm. Runtime repos may consume a contract-surface lock but must not redefine which Substrate files are canonical.

## Authority surface

The authority surface includes canonical schemas, registries, manifests, route registries, boundary doctrine, AI front-door routing policy, skill-agent governance policy, and CI routing policy when those surfaces affect runtime correctness.

## Excluded evidence surface

Managed-patch decisions, audit records, reports, review notes, tests, scripts, and local generated artifacts are not consumer contract authority by default. They may be important evidence, but they should not force recursive consumer lock bumps unless the contract-surface registry explicitly includes them.

## Required behavior

- If an included contract-surface file changes, consumer locks must be refreshed.
- If only excluded audit/evidence files change, consumer locks should remain valid.
- If the contract-surface registry changes, the change is protected and requires human/Codex review.
- Consumers must fail closed if the computed contract-surface hash differs from their lock.
- Consumers may record the Substrate repo commit as provenance, but the contract-surface hash is the authoritative validation gate when present.

## Non-claims

This boundary does not allow runtime repos to mutate the Semantic Substrate, invent route authority, invent event classes, or bypass the Exception Lake evidence boundary.
