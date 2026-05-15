from __future__ import annotations
import argparse, fnmatch, json, os, re, subprocess, sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PATCH_ARTIFACT_PATTERNS = ['*seed-pack*', '*patch*', '*.zip']
KNOWN_REPO_ALIASES = {
    'LawFirm-os-exceptions-lake-runtime': ['LawFirm-os-exceptions-lake-runtime-main'],
    'LawFirm-os-semantic-substrate': ['LawFirm-os-semantic-substrate-main'],
    'LawFirm-os-orchestrator': ['LawFirm-os-orchestrator-main'],
    'LawFirm-os-legal-knowledge-runtime': ['LawFirm-os-legal-knowledge-runtime-main'],
    'LawFirm-os-skills-registry': ['LawFirm-os-skills-registry-main'],
}
DEFAULT_PLANES = {
    'LawFirm-os-semantic-substrate': 'semantic_substrate',
    'LawFirm-os-orchestrator': 'orchestrator',
    'LawFirm-os-exceptions-lake-runtime': 'exception_lake',
    'LawFirm-os-legal-knowledge-runtime': 'legal_knowledge_runtime',
    'LawFirm-os-skills-registry': 'skills_registry',
}

def load_json(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

def dump_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=False) + '\n'

def is_patch_artifact(name: str) -> bool:
    low = name.lower()
    return any(fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(low, pat.lower()) for pat in PATCH_ARTIFACT_PATTERNS)

def canonical_repo_name(path_name: str) -> str:
    if path_name.endswith('-main'):
        base = path_name[:-5]
        if base in DEFAULT_PLANES:
            return base
    return path_name

def normalize_pytest_repo_name(name: str | None) -> str | None:
    if not name or not isinstance(name, str):
        return None
    n = name.strip()
    if not n:
        return None
    for canonical, aliases in KNOWN_REPO_ALIASES.items():
        if n == canonical or n in aliases:
            return canonical
    if n.endswith('-main'):
        base = n[:-5]
        if base in DEFAULT_PLANES:
            return base
    return n

def discover_repo_dirs(workspace: Path) -> dict[str, Path]:
    repos = {}
    for p in workspace.iterdir():
        if not p.is_dir():
            continue
        if not p.name.startswith('LawFirm-os-'):
            continue
        if is_patch_artifact(p.name):
            continue
        canonical = canonical_repo_name(p.name)
        repos[canonical] = p
    return repos

def substrate_dir(workspace: Path) -> Path:
    repos = discover_repo_dirs(workspace)
    if 'LawFirm-os-semantic-substrate' not in repos:
        raise SystemExit('Missing LawFirm-os-semantic-substrate repo in workspace')
    return repos['LawFirm-os-semantic-substrate']

def load_repo_registry(workspace: Path) -> dict[str, Any]:
    p = substrate_dir(workspace) / 'registry' / 'lawfirm-os-repo-registry.json'
    if not p.exists():
        return {'repos': [], 'explicit_exclusions': []}
    return load_json(p)

def active_repo_names(workspace: Path) -> set[str]:
    reg = load_repo_registry(workspace)
    out = set()
    for entry in reg.get('repos', []):
        if entry.get('status') == 'active':
            out.add(entry.get('repo_name') or entry.get('repo_id'))
    return {x for x in out if x}

def repo_plane(repo: str, workspace: Path | None = None) -> str:
    if workspace:
        try:
            reg = load_repo_registry(workspace)
            for entry in reg.get('repos', []):
                if (entry.get('repo_name') == repo or entry.get('repo_id') == repo or entry.get('repo_name') == repo.replace('-main','')):
                    if entry.get('owning_plane'):
                        return entry['owning_plane']
        except Exception:
            pass
    return DEFAULT_PLANES.get(repo, 'unknown')

def read_manifest(repo_dir: Path) -> dict[str, Any] | None:
    p = repo_dir / 'ci-test-manifest.json'
    if not p.exists():
        return None
    return load_json(p)

TEST_PATTERNS = [
    ('python','pytest','pytest_file', re.compile(r'(^|/)tests/test_[^/]*\.py$|(^|/)tests/.+_test\.py$|^scripts/validation/tests/test_[^/]*\.py$'), 'python -m pytest {path} -q'),
    ('typescript','vitest_or_jest','typescript_test_file', re.compile(r'.+\.test\.ts$'), 'npx vitest run {path}'),
    ('typescript','playwright_or_vitest','typescript_spec_file', re.compile(r'.+\.spec\.ts$'), 'npx playwright test {path}'),
    ('javascript','jest_or_vitest','javascript_test_file', re.compile(r'.+\.test\.js$'), 'npx jest {path}'),
    ('javascript','playwright_or_jest','javascript_spec_file', re.compile(r'.+\.spec\.js$'), 'npx playwright test {path}'),
    ('go','go_test','go_package_test', re.compile(r'.+_test\.go$'), 'go test ./...'),
    ('rust','cargo_test','rust_crate_test', re.compile(r'.+_test\.rs$'), 'cargo test'),
    ('java','junit','junit_class', re.compile(r'.+Test\.java$|.*/src/test/.+\.java$'), './gradlew test'),
    ('csharp','dotnet_test','dotnet_test_class', re.compile(r'.+Tests?\.cs$'), 'dotnet test'),
    ('shell','bats','bats_test_file', re.compile(r'.+\.bats$'), 'bats {path}'),
    ('shell','bash','shell_test_script', re.compile(r'.*/test_[^/]*\.sh$|.*/smoke_[^/]*\.sh$|^test_[^/]*\.sh$|^smoke_[^/]*\.sh$'), 'bash {path}'),
]
EXCLUDE_DIRS = {'.git','__pycache__','.pytest_cache','node_modules','target','.venv','venv','.mypy_cache'}

def is_excluded_path(rel: str) -> bool:
    return any(part in EXCLUDE_DIRS for part in rel.split('/'))

def detect_test_artifact(rel: str) -> dict[str, Any] | None:
    if is_excluded_path(rel):
        return None
    if rel.endswith('/conftest.py') or rel == 'tests/conftest.py':
        return None
    for language, framework, artifact_type, regex, cmd in TEST_PATTERNS:
        if regex.match(rel):
            return {
                'language': language,
                'framework': framework,
                'artifact_type': artifact_type,
                'path': rel,
                'runner_command': cmd.format(path=rel),
            }
    return None

def discover_test_artifacts_for_repo(repo_dir: Path) -> list[dict[str, Any]]:
    artifacts = []
    for p in repo_dir.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(repo_dir).as_posix()
        art = detect_test_artifact(rel)
        if art:
            artifacts.append(art)
    return sorted(artifacts, key=lambda x: x['path'])

def manifest_artifact_paths(manifest: dict[str, Any]) -> set[str]:
    return {a.get('path') for a in manifest.get('test_artifacts', []) if a.get('path')}

def exclusion_patterns(manifest: dict[str, Any]) -> list[str]:
    return [x.get('path','') for x in manifest.get('explicit_test_artifact_exclusions', []) if x.get('path')]

def path_explicitly_excluded(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)

def git_output(repo_dir: Path, args: list[str]) -> list[str]:
    proc = subprocess.run(['git','-C',str(repo_dir),*args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]

def changed_files_for_repo(repo_name: str, repo_dir: Path, base_ref: str | None) -> list[str]:
    files = []
    if base_ref:
        for line in git_output(repo_dir, ['diff','--name-only',base_ref,'--']):
            files.append(f'{repo_name}/{line}')
    else:
        for line in git_output(repo_dir, ['diff','--name-only','HEAD','--']):
            files.append(f'{repo_name}/{line}')
    for line in git_output(repo_dir, ['ls-files','--others','--exclude-standard']):
        files.append(f'{repo_name}/{line}')
    return sorted(set(files))

def classify_file(path: str) -> set[str]:
    p = path.replace('\\','/')
    rel = p.split('/',1)[1] if '/' in p else p
    low = rel.lower()
    classes = set()
    if rel in {'AGENTS.md','AI_WORK_START_HERE.md','AI_START_HERE.md','CLAUDE.md'} or low.endswith('/agents.md'):
        classes.add('ai_instruction_change')
    if low.startswith('governance/') or low.startswith('docs/') or low.endswith('.md') and any(x in low for x in ['boundary','governance','front_door','work_start']):
        classes.add('governance_doc_change')
    if low.startswith('registry/') and low.endswith('.json'):
        classes.add('registry_change')
    if low.startswith('schemas/') and low.endswith('.json'):
        classes.add('schema_change')
    if low.endswith('contracts.lock.json'):
        classes.add('contract_lock_change')
    if low.endswith('skill-agent-manifest.json'):
        classes.add('repo_boundary_change')
    if low.endswith('ci-test-manifest.json'):
        classes.add('test_manifest_change')
    if low.startswith('skills/'):
        classes.add('skill_definition_change' if low.endswith('skill.md') else 'skill_metadata_change')
    if low.startswith('.github/workflows/'):
        classes.add('workflow_change')
    if 'ci-test-route' in low or 'route_ci_tests.py' in low or 'validate_ci_route_decision.py' in low or 'test-artifact' in low or 'test_architecture' in low or 'ci_test_routing' in low:
        classes.add('ci_router_change')
    if detect_test_artifact(rel):
        classes.add('test_artifact_change')
    if low.endswith('.py') or low.startswith('src/') or low.startswith('scripts/'):
        classes.add('source_code_change')
    if not classes:
        classes.add('unknown_change')
    return classes

def risk_from_classes(classes: set[str]) -> str:
    protected = {'ai_instruction_change','governance_doc_change','registry_change','schema_change','contract_lock_change','repo_boundary_change','ci_router_change','unknown_change'}
    high = {'workflow_change','skill_definition_change','skill_metadata_change','test_manifest_change'}
    if classes & protected:
        return 'protected'
    if classes & high:
        return 'high'
    if classes & {'source_code_change','test_artifact_change'}:
        return 'medium'
    return 'medium'

def severity_rank(tier: str) -> int:
    return {'low':0,'medium':1,'high':2,'protected':3}.get(tier,1)

def max_risk(a: str, b: str) -> str:
    return a if severity_rank(a) >= severity_rank(b) else b

def load_architecture_registry(workspace: Path) -> dict[str, Any]:
    p = substrate_dir(workspace) / 'registry' / 'test-architecture-registry.json'
    if not p.exists():
        return {'architecture_surfaces': []}
    return load_json(p)

def registry_surface_rows(workspace: Path) -> dict[str, dict[str, Any]]:
    reg = load_architecture_registry(workspace)
    return {e['surface']: e for e in reg.get('architecture_surfaces', []) if e.get('surface')}

def known_architecture_surfaces(workspace: Path) -> set[str]:
    return set(registry_surface_rows(workspace).keys())

def apply_registry_surface_policy(
    affected_surfaces: set[str], workspace: Path,
    cross: bool, full: bool, codex: bool, human: bool, risk: str,
) -> tuple[bool, bool, bool, bool, str]:
    """Use test-architecture-registry.json risk tiers to fail closed on protected/high surfaces."""
    rows = registry_surface_rows(workspace)
    for s in affected_surfaces:
        row = rows.get(s)
        if not row:
            continue
        tier = row.get('risk_tier', '')
        if tier == 'protected':
            cross, codex, human = True, True, True
            risk = max_risk(risk, 'protected')
        elif tier == 'high':
            cross = True
    return cross, full, codex, human, risk

SURFACE_HEURISTIC_RULES = [
    (re.compile(r'^registry/ai-front-door-registry\.json$', re.IGNORECASE), {'ai_front_door'}),
    (re.compile(r'^(AGENTS|AI_WORK_START_HERE|AI_START_HERE|CLAUDE)\.md$', re.IGNORECASE), {'ai_front_door'}),
    (re.compile(r'^registry/skill-agent-.*\.json$', re.IGNORECASE), {'skill_agent_control_plane'}),
    (re.compile(r'^skill-agent-manifest\.json$', re.IGNORECASE), {'skill_agent_control_plane'}),
    (re.compile(r'^registry/managed-patch-(decisions/.*|preservation-policy\.json)$', re.IGNORECASE), {'managed_patch_preservation'}),
    (re.compile(r'^registry/.*\.json$', re.IGNORECASE), {'registry_integrity'}),
    (re.compile(r'^schemas/.*\.json$', re.IGNORECASE), {'schema_surface'}),
    (re.compile(r'^governance/.*', re.IGNORECASE), {'governance_boundary'}),
    (re.compile(r'(^|/)contracts\.lock\.json$', re.IGNORECASE), {'contract_lock'}),
    (re.compile(r'(^|/)ci-test-manifest\.json$', re.IGNORECASE), {'test_artifact_registration', 'repo_onboarding'}),
    (re.compile(r'(ci-test-route|route_ci_tests\.py|validate_ci_route_decision\.py|test-architecture-registry|ci_test_routing)', re.IGNORECASE), {'ci_test_router','cross_repo_integration'}),
]

def architecture_surfaces_for_path(rel: str) -> set[str]:
    out: set[str] = set()
    for matcher, surfaces in SURFACE_HEURISTIC_RULES:
        if matcher.search(rel):
            out |= surfaces
    return out

def collect_affected_surfaces(changed_files: list[str]) -> set[str]:
    out: set[str] = set()
    for f in changed_files:
        rel = f.split('/',1)[1] if '/' in f else f
        out |= architecture_surfaces_for_path(rel)
    return out

def surfaces_from_manifest_triggers(changed_files: list[str], workspace: Path) -> set[str]:
    """Map changed paths to architecture_surface entries declared in ci-test-manifest.json trigger_patterns."""
    out: set[str] = set()
    repos = discover_repo_dirs(workspace)
    for repo, repo_dir in repos.items():
        manifest = read_manifest(repo_dir)
        if not manifest:
            continue
        for item in manifest.get('test_artifacts', []):
            owning_repo = item.get('owning_repo', repo)
            triggers = item.get('trigger_patterns', [])
            surfs = {s for s in item.get('architecture_surface', []) if s}
            if not triggers or not surfs:
                continue
            prefix = owning_repo + '/'
            for cf in changed_files:
                if not cf.startswith(prefix):
                    continue
                rel = cf[len(prefix):]
                if any(fnmatch.fnmatch(rel, pat) for pat in triggers):
                    out |= surfs
    return out

def expand_affected_repos_from_contract_lock(changed_files: list[str], repos: dict[str, Path], affected: set[str]) -> None:
    for f in changed_files:
        low = f.replace('\\','/').lower()
        if not low.endswith('contracts.lock.json'):
            continue
        repo_name = f.split('/',1)[0] if '/' in f else ''
        if repo_name not in repos:
            continue
        lock_path = repos[repo_name] / 'contracts.lock.json'
        if not lock_path.exists():
            continue
        try:
            data = load_json(lock_path)
        except Exception:
            continue
        cr = data.get('contract_repo')
        if isinstance(cr, str):
            cnorm = normalize_pytest_repo_name(cr) or cr
            if cnorm in repos:
                affected.add(cnorm)

def route_tests_by_architecture(workspace: Path, classes: set[str], changed_files: list[str], affected_repos: set[str], affected_surfaces: set[str]) -> tuple[list[str], set[str], list[str]]:
    """Select test artifacts using architecture surfaces and upstream/downstream dependency metadata.

    Returns (selected_test_ids, expanded_pytest_repos, selection_reasons).
    """
    selected_ids: set[str] = set()
    pytest_repos: set[str] = set(affected_repos)
    reasons: list[str] = []
    repos = discover_repo_dirs(workspace)
    for repo, repo_dir in repos.items():
        manifest = read_manifest(repo_dir) or {}
        for item in manifest.get('test_artifacts', []):
            owning_repo = item.get('owning_repo', repo)
            surfaces = set(item.get('architecture_surface', []))
            upstream_raw = item.get('upstream_dependencies', [])
            downstream_raw = item.get('downstream_dependencies', [])
            upstream = {normalize_pytest_repo_name(r) or r for r in upstream_raw if isinstance(r, str)}
            downstream = {normalize_pytest_repo_name(r) or r for r in downstream_raw if isinstance(r, str)}
            covered_classes = set(item.get('change_classes_covered', []))
            triggers = item.get('trigger_patterns', [])
            test_id = item.get('test_id')
            path = item.get('path')
            include = False
            why: list[str] = []
            # 1. Architecture-surface overlap
            if surfaces & affected_surfaces:
                include = True
                why.append('surface=' + ','.join(sorted(surfaces & affected_surfaces)))
            # 2. trigger pattern match (repo-relative AND workspace-relative)
            repo_rel_changed = [f.split('/',1)[1] for f in changed_files if f.startswith(owning_repo + '/') and '/' in f]
            for cf in repo_rel_changed:
                if any(fnmatch.fnmatch(cf, pat) for pat in triggers):
                    include = True
                    why.append('trigger_repo_rel=' + cf)
                    break
            for cf in changed_files:
                if any(fnmatch.fnmatch(cf, pat) for pat in triggers):
                    include = True
                    why.append('trigger_workspace=' + cf)
                    break
            # 3. change-class overlap on affected repo (or substrate, which gates cross-repo)
            if covered_classes & classes and (owning_repo in affected_repos or owning_repo == 'LawFirm-os-semantic-substrate'):
                include = True
                why.append('class=' + ','.join(sorted(covered_classes & classes)))
            # 4. dependency-graph propagation: this test depends on an affected upstream repo
            if upstream & affected_repos:
                include = True
                why.append('upstream=' + ','.join(sorted(upstream & affected_repos)))
            # 5. dependency-graph propagation: consumer tests when a declared downstream is affected
            if downstream & affected_repos:
                include = True
                why.append('downstream_affected=' + ','.join(sorted(downstream & affected_repos)))
            if include and test_id:
                selected_ids.add(test_id)
                pytest_repos.add(owning_repo)
                reasons.append(f'{test_id} <- {",".join(why) or "n/a"}')
    return sorted(selected_ids), pytest_repos, reasons

def main() -> int:
    ap = argparse.ArgumentParser(description='Route LawFirm OS validators/tests from changed files using architecture-surface and dependency metadata.')
    ap.add_argument('--workspace', default='.')
    ap.add_argument('--base-ref', default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--changed-file', action='append', default=[], help='Manually supply changed file path as repo/path for tests or no-git environments')
    args = ap.parse_args()
    workspace = Path(args.workspace).resolve()
    repos = discover_repo_dirs(workspace)
    active = active_repo_names(workspace)
    changed = list(args.changed_file or [])
    if not changed:
        for repo, repo_dir in sorted(repos.items()):
            changed.extend(changed_files_for_repo(repo, repo_dir, args.base_ref))
    changed = sorted(set(changed))
    classes: set[str] = set()
    affected: set[str] = set()
    risk = 'low'
    reasons: list[str] = []
    for f in changed:
        repo = f.split('/',1)[0] if '/' in f else ''
        if repo in repos:
            affected.add(repo)
        c = classify_file(f)
        classes |= c
        file_risk = risk_from_classes(c)
        risk = max_risk(risk, file_risk)
        reasons.append(f'{f}: {",".join(sorted(c))}')
    expand_affected_repos_from_contract_lock(changed, repos, affected)
    affected_surfaces = collect_affected_surfaces(changed) | surfaces_from_manifest_triggers(changed, workspace)
    validators = {'discover_test_artifacts','validate_test_artifact_registration','validate_new_repo_ci_onboarding'}
    cross = False
    full = False
    codex = False
    human = False
    if classes & {'ai_instruction_change','governance_doc_change'}:
        validators |= {'validate_managed_patch_preservation','validate_ai_front_door'}; codex=True; human=True
    if classes & {'registry_change','schema_change'}:
        validators |= {'validate_ai_front_door','validate_test_artifact_registration'}; cross=True; codex=True
    if 'registry_change' in classes or 'repo_boundary_change' in classes:
        validators |= {'validate_skill_agent_control_plane'}; cross=True
    if 'contract_lock_change' in classes:
        validators |= {'validate_contract_lock_drift_workspace'}; cross=True; human=True
    if classes & {'skill_definition_change','skill_metadata_change'}:
        validators |= {'validate_skill_agent_control_plane'}
    if classes & {'ci_router_change','test_manifest_change'}:
        validators |= {'validate_ci_route_decision','validate_test_artifact_registration'}; full=True; codex=True; human=True
    if 'workflow_change' in classes:
        validators |= {'validate_ci_route_decision'}; codex=True
    # Architecture-surface escalations (schemas/registries/governance ⇒ cross-repo validation).
    if affected_surfaces & {'schema_surface','registry_integrity','governance_boundary','ai_front_door','skill_agent_control_plane','managed_patch_preservation'}:
        cross = True
    if 'cross_repo_integration' in affected_surfaces:
        full = True; cross = True; codex = True; human = True
    if 'contract_lock' in affected_surfaces:
        validators |= {'validate_contract_lock_drift_workspace'}; cross = True; human = True
    cross, full, codex, human, risk = apply_registry_surface_policy(
        affected_surfaces, workspace, cross, full, codex, human, risk
    )
    # Unknown / ambiguous changes must fail closed. Registry policy says full workspace + human + Codex review.
    if 'unknown_change' in classes:
        validators |= {
            'discover_test_artifacts',
            'validate_test_artifact_registration',
            'validate_new_repo_ci_onboarding',
            'validate_ai_front_door',
            'validate_managed_patch_preservation',
            'validate_skill_agent_control_plane',
            'validate_contract_lock_drift_workspace',
        }
        cross = True; full = True; codex = True; human = True
        risk = max_risk(risk, 'protected')
    # Route tests via architecture surfaces and dependency graph (replaces previous trigger-only pass).
    routed_test_ids, expanded_pytest_repos, routing_reasons = route_tests_by_architecture(
        workspace, classes, changed, affected, affected_surfaces
    )
    pytest_repos_set: set[str] = set()
    if classes & {'source_code_change','test_artifact_change','test_manifest_change','ci_router_change'}:
        pytest_repos_set |= affected
    pytest_repos_set |= expanded_pytest_repos
    if full:
        pytest_repos_set |= active if active else set(repos.keys())
    pytest_repos = sorted(pytest_repos_set)
    required_artifacts = routed_test_ids
    routing_reasons_capped = routing_reasons[:200]
    decision = {
        'schema_version':'ci_test_route_decision.v1',
        'decision_id':'ci_route_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
        'created_at':datetime.now(timezone.utc).isoformat(),
        'workspace_root':str(workspace),
        'base_ref':args.base_ref,
        'changed_files':changed,
        'change_classes':sorted(classes),
        'risk_tier':risk,
        'affected_repos':sorted(affected),
        'affected_architecture_surfaces':sorted(affected_surfaces),
        'required_validators':sorted(validators),
        'required_pytest_repos':pytest_repos,
        'required_test_artifacts':required_artifacts,
        'requires_cross_repo_validation':cross,
        'requires_full_workspace_tests':full,
        'requires_codex_review':codex or risk == 'protected',
        'requires_human_review':human or risk == 'protected',
        'reason_codes':reasons,
        'routing_reasons':routing_reasons_capped,
        'recommended_commands': []
    }
    # command hints
    for v in decision['required_validators']:
        if v == 'discover_test_artifacts':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\discover_test_artifacts.py --workspace .')
        elif v == 'validate_test_artifact_registration':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\validate_test_artifact_registration.py --workspace .')
        elif v == 'validate_new_repo_ci_onboarding':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\validate_new_repo_ci_onboarding.py --workspace .')
        elif v == 'validate_ci_route_decision':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\validate_ci_route_decision.py --workspace . --decision .ci-route-decision.json')
        elif v == 'validate_ai_front_door':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\validate_ai_front_door.py')
        elif v == 'validate_skill_agent_control_plane':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\validate_skill_agent_control_plane.py --workspace .')
        elif v == 'validate_managed_patch_preservation':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\validate_managed_patch_preservation.py --workspace .')
        elif v == 'validate_contract_lock_drift_workspace':
            decision['recommended_commands'].append('python .\\LawFirm-os-semantic-substrate\\scripts\\validate_contract_lock_drift_workspace.py --workspace .')
    for repo in pytest_repos:
        repo_dir = repos.get(repo)
        if repo_dir:
            decision['recommended_commands'].append(f'cd .\\{repo_dir.name} && python -m pytest -q && cd ..')
    text = dump_json(decision)
    if args.out:
        Path(args.out).write_text(text, encoding='utf-8')
    else:
        print(text, end='')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
