# Managed Patch Preservation Boundary

## Purpose

This boundary prevents AI agents, patch scripts, and generated governance overlays from accidentally replacing repo-specific doctrine, registry entries, schemas, validation code, or workflow maps with generic bootstrap text or generated code.

The research update changes the bar for this gate: AI coding agents are not only at risk of deleting Markdown sections. They can silently corrupt long documents, miss file-edit side effects, weaken policies through wording changes, delete public code symbols, drop JSON registry identifiers, and pass ordinary tests while governance content is gone.

LawFirm OS may add new control-plane instructions, skill-agent metadata, AI front-door pointers, schemas, registries, validators, and workflow maps. Those additions must normally be merged into existing files while preserving the original repository-specific meaning.

## Core doctrine

Default change mode is:

```text
preserve_and_add
```

Allowed change modes:

| Mode | Meaning | Default scrutiny |
|---|---|---|
| `preserve_and_add` | Add a managed block while retaining existing content | normal validator pass |
| `merge` | Combine old and new content into a coherent final artifact | normal validator pass |
| `replace` | Replace existing content with new content | strict decision record + approval for protected files |
| `delete` | Delete existing content | strict decision record + approval for protected files |
| `regenerate` | Replace generated content from an authoritative generator | decision record unless explicitly allowlisted |

## Research-driven additions in v2

The validator now treats the following as first-class risks:

1. **Document corruption:** removed headings, removed repo-specific doctrine, missing backup content, and large low-similarity rewrites are suspicious.
2. **Permission-gate bypass through file edits:** a change made through file mutation can be as dangerous as a shell command, so protected file edits are audited directly.
3. **Registry and schema erosion:** removed JSON keys, IDs, paths, refs, route IDs, event classes, skill IDs, workflow IDs, and tool IDs are suspicious.
4. **Code-surface erosion:** removed public Python classes/functions/methods in protected source, script, or test surfaces are suspicious.
5. **Policy weakening:** removing strict language such as `must`, `forbidden`, `fail closed`, or `approval required` while adding permissive language such as `optional`, `may`, `skip`, or `auto-approve` is suspicious.
6. **Contract-lock drift:** changes to `contracts.lock.json` require provenance and committed-substrate review.
7. **Broad blast radius:** a patch touching many protected files requires a workspace-level decision record.
8. **Higher reasoning review:** destructive changes to protected files require `model_review_level: extra_high`, human approval, merge consideration, and an explanation of why merge is not sufficient.

## Protected files

The following surfaces are protected because loss of their content can silently weaken governance:

- `AGENTS.md`
- `AI_WORK_START_HERE.md`
- `AI_START_HERE.md`
- `README.md`
- `CLAUDE.md`
- `.cursor/rules/*.mdc`
- `.github/copilot-instructions.md`
- `.github/workflows/*.yml|*.yaml`
- `.pre-commit-config.yaml`
- `pyproject.toml`, lockfiles, dependency manifests, `Makefile`, `Dockerfile`
- `governance/**/*.md`
- `docs/**/*.md|*.yaml|*.yml` when they contain boundary, architecture, workflow, or validation doctrine
- `registry/**/*.json`
- `manifests/**/*.json`
- `exports/**/*.json`
- `schemas/**/*.json`
- `policies/**/*.json`
- `prompts/**/*.md|*.txt`
- `scripts/**/*.py`
- `tests/**/*.py`
- `src/**/*.py`
- `SKILL.md`
- `SKILL_METADATA.json`
- `AGENT.md`
- `AGENT_METADATA.json`
- `tools/**/*.json`
- `workflows/**/*.json`
- `workflow/**/*.json`
- `skill-agent-manifest.json`
- `contracts.lock.json`

## Required behavior for AI agents

Before replacing, deleting, or regenerating protected content, an agent must explicitly decide:

1. Should existing content be preserved and new content added?
2. Should existing content and new content be merged?
3. Is total replacement necessary?
4. If replacement is necessary, what old content is being intentionally removed and why?
5. Why is merge not sufficient?
6. Does the change affect canonical authority, governance, AI front-door routing, schemas, registries, skills, workflow composition, contract locks, source code symbols, or evidence boundaries?
7. What automated checks were run?
8. Did a high-reasoning reviewer inspect the diff?
9. Is human approval required?

The deterministic validator enforces this by requiring a `managed-patch-decision` record for suspicious replacements, broad blast-radius changes, and destructive changes to protected surfaces.

## Managed blocks

For Markdown files, generated bootstrap text should use managed markers:

```markdown
<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->
...
<!-- END LAWFIRM_OS_BOOTSTRAP -->
```

Repo-specific content should remain outside the managed block, preferably inside:

```markdown
<!-- BEGIN REPO_SPECIFIC_INSTRUCTIONS -->
...
<!-- END REPO_SPECIFIC_INSTRUCTIONS -->
```

A file that has a bootstrap block but no remaining repo-specific content is suspicious and should fail validation unless an approved replacement decision exists.

## Decision records

Decision records may live in either place:

```text
LawFirm-os-semantic-substrate/registry/managed-patch-decisions/<repo>/<sanitized-target-path>.json
<repo>/.lawfirm-os/managed-patch-decisions/<sanitized-target-path>.json
```

For broad patch sets, workspace-level decisions live at:

```text
LawFirm-os-semantic-substrate/registry/managed-patch-decisions/workspace/blast-radius-<digest>.json
```

For protected files, `replace`, `delete`, and `regenerate` require:

```json
{
  "old_content_reviewed": true,
  "merge_considered": true,
  "why_merge_not_sufficient": "...",
  "human_review_required": true,
  "human_review_status": "approved",
  "model_review_level": "extra_high",
  "user_intent_alignment_summary": "...",
  "diff_review_summary": "...",
  "replacement_justification": "...",
  "alternatives_considered": ["preserve_and_add", "merge", "replace"],
  "automated_checks_run": ["validate_managed_patch_preservation.py"]
}
```

## What this boundary does not prevent

This boundary does not prohibit necessary rewrites. It only requires that destructive changes be explicit, reviewed, and auditable.

It also does not make AI-generated decisions canonical. Automated decisions remain proposal or runtime evidence unless promoted through the governed path.

## Validation

Run from the parent workspace:

```powershell
python .\LawFirm-os-semantic-substrate\scripts\validate_managed_patch_preservation.py --workspace .
```

For branch/PR comparison:

```powershell
python .\LawFirm-os-semantic-substrate\scripts\validate_managed_patch_preservation.py --workspace . --base-ref origin/main
```

For recent pushed-main forensic checks:

```powershell
python .\LawFirm-os-semantic-substrate\scripts\validate_managed_patch_preservation.py --workspace . --include-last-commit
```

For generated decision stubs:

```powershell
python .\LawFirm-os-semantic-substrate\scripts\validate_managed_patch_preservation.py --workspace . --create-decision-stubs
```
