# No-Hallucination Policy

AI contributors must not invent:
- repository files or directories
- internal Law Firm facts, clients, matters, or employees
- source payloads not present in governed examples or profiles
- validation results that did not actually run
- production readiness, production accuracy, or production safety claims
- adapter capabilities that are not documented and approved

## Required behavior

When evidence is missing, say **evidence missing**.

When a profile is blocked pending source payload evidence, keep it blocked.

When a validator is fail-closed, report fail-closed rather than green.

When a canonical question cannot be resolved from authority surfaces, stop and
report the authority conflict instead of guessing.

## Special rule for external code and leaks

Do not download, vendor, run, mirror, or operationalize leaked or unofficial
vendor code. Treat leak-themed repositories and copied internals as prohibited
supply-chain inputs.
