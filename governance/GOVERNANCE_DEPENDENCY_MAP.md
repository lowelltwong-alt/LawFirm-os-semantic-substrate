# Governance Dependency Map

Status: active control-plane governance surface.

The canonical machine-readable map is `registry/governance-dependency-map.json`.
It records which governance-facing LawFirm OS surfaces depend on each other,
which child repos mirror the rule locally, and which validators keep the map
from drifting.

## Core Rule

If this repo changes governance-facing files, check the upstream governance
dependency map and update the map, front doors, tables of contents, local mirror
files, validators, tests, and PR-description requirements when affected.

The same rule is mirrored in downstream repos through
`.ai/control/governance-dependency-map-mirror.json`. A child mirror is a local
enforcement surface only. It does not authorize a child repo to override the
Semantic Substrate or weaken governance.

## Governance-Facing Scope

Governance-facing files include:

- AI front doors, AI tables of contents, agent instructions, repo role files,
  and README sections that describe authority.
- `governance/`, `docs/governance/`, `registry/`, `manifests/`, `schemas/`,
  `contracts.lock.json`, `repo_topology.yaml`, and `skill-agent-manifest.json`.
- Validation, CI, PR-description, and issue-template files that can change what
  passes review.
- Runtime docs or code paths that alter client data boundaries, privacy,
  compliance, legal-context assembly, automation authority, human approvals,
  Exception Lake admission, skill authority, or intake/budget/conflct boundaries.

## Child Mirror Template

Each child repo mirror must include:

```json
{
  "object_type": "governance_dependency_map_mirror",
  "schema_version": "governance_dependency_map_mirror.v1",
  "owner_repo": "LawFirm-os-example",
  "upstream_dependency_map": {
    "repo": "LawFirm-os-semantic-substrate",
    "path": "registry/governance-dependency-map.json",
    "artifact_id": "LFGD-008",
    "rule": "governance_map_update_gate",
    "source_of_truth": true
  },
  "authority": {
    "local_repo_may_override_upstream_dependency_map": false,
    "local_repo_may_weaken_upstream_governance": false,
    "local_repo_may_treat_local_convenience_as_governance_authority": false,
    "local_repo_must_stop_if_upstream_map_conflicts": true
  }
}
```

Child repos may add stricter local watched paths, but may not remove the upstream
authority flags or convert local workflow convenience into governance authority.

## Red-Team Finding

Code changes can add validators and workflows, but they cannot by themselves
make GitHub require those checks before merge. As of the 2026-06-29 preflight,
`main` branch protection / required-check settings were not reported as enabled
for the LawFirm OS repos checked by `gh api`.

Blocked owner question: should the owner enable branch protection and required
status checks for the governance dependency-map, child mirror, and PR-description
workflows across all LawFirm OS repos?

## LawFirm OS Translation Notes

This pattern is adapted from the Logos governance dependency-map gate. In
LawFirm OS terms, the protected concerns are client and matter data, intake
workflows, legal operations, privacy, compliance, automation authority,
jurisdiction/scope assumptions, human approval gates, and repository ownership.

The map does not authorize legal advice, production automation, external writes,
real client data ingestion, raw matter payload storage, or AI-generated
governance authority.
