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
    """Map checkout folder aliases (e.g. *-main) to canonical repo names for evidence matching."""
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
    ('python','pytest','pytest_file', re.compile(r'(^|/)tests/test_[^/]*\.py$|(^|/)tests/.+_test\.py$|^scripts/validation/tests/test_[^/]*\.py$'), 'python scripts/run_full_pytest.py {path} -q'),
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
    protected = {'ai_instruction_change','governance_doc_change','registry_change','schema_change','contract_lock_change','repo_boundary_change','ci_router_change'}
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

REQUIRED = ['schema_version','decision_id','created_at','workspace_root','changed_files','change_classes','risk_tier','affected_repos','required_validators','required_pytest_repos','required_test_artifacts','requires_cross_repo_validation','requires_full_workspace_tests','requires_codex_review','requires_human_review','reason_codes']
PROTECTED_CLASSES = {'ai_instruction_change','governance_doc_change','registry_change','schema_change','contract_lock_change','repo_boundary_change','ci_router_change'}
UNKNOWN_CHANGE_REQUIRED_VALIDATORS = {
    'discover_test_artifacts',
    'validate_test_artifact_registration',
    'validate_new_repo_ci_onboarding',
    'validate_ai_front_door',
    'validate_managed_patch_preservation',
    'validate_skill_agent_control_plane',
    'validate_contract_lock_drift_workspace',
}

def main() -> int:
    ap = argparse.ArgumentParser(description='Validate a CI route decision and final-run evidence if supplied.')
    ap.add_argument('--workspace', default='.')
    ap.add_argument('--decision', required=True)
    ap.add_argument('--ran-validator', action='append', default=[],
                    help='Repeatable. Validator id that was actually run. Must be in required_validators in strict mode.')
    ap.add_argument('--ran-test-artifact', action='append', default=[],
                    help='Repeatable. Test artifact test_id that was actually run. Must be in required_test_artifacts in strict mode.')
    ap.add_argument('--ran-pytest-repo', action='append', default=[],
                    help='Repeatable. Repo name whose pytest suite was actually run. Must be in required_pytest_repos in strict mode.')
    ap.add_argument('--allow-missing-run-evidence', action='store_true',
                    help='Planning mode. Disables strict run-evidence checks. Strict commit/push gates must NOT use this flag.')
    args = ap.parse_args()
    workspace = Path(args.workspace).resolve()
    decision = load_json(Path(args.decision))
    errors = []
    for f in REQUIRED:
        if f not in decision:
            errors.append(f'missing decision field {f}')
    if decision.get('schema_version') != 'ci_test_route_decision.v1':
        errors.append('schema_version must be ci_test_route_decision.v1')
    classes = set(decision.get('change_classes', []))
    validators = set(decision.get('required_validators', []))
    required_tests = set(decision.get('required_test_artifacts', []))
    required_pytest_repos_list = decision.get('required_pytest_repos', [])
    required_pytest_repos: set[str] = set()
    pytest_norm_errors: list[str] = []
    for raw in required_pytest_repos_list:
        norm = normalize_pytest_repo_name(raw)
        if not norm:
            pytest_norm_errors.append(f'invalid required_pytest_repos entry: {raw!r}')
        else:
            required_pytest_repos.add(norm)
    errors.extend(pytest_norm_errors)
    if classes & PROTECTED_CLASSES and decision.get('risk_tier') != 'protected':
        errors.append('protected change class requires risk_tier=protected')
    if 'contract_lock_change' in classes and 'validate_contract_lock_drift_workspace' not in validators:
        errors.append('contract_lock_change must require validate_contract_lock_drift_workspace')
    if 'ai_instruction_change' in classes and 'validate_ai_front_door' not in validators:
        errors.append('ai_instruction_change must require validate_ai_front_door')
    if 'ci_router_change' in classes and not decision.get('requires_full_workspace_tests'):
        errors.append('ci_router_change must require full workspace tests')
    if 'unknown_change' in classes:
        # Registry policy: unknown changes must escalate to full workspace + human + Codex review.
        if decision.get('risk_tier') != 'protected':
            errors.append('unknown_change must escalate risk_tier to protected')
        if not decision.get('requires_full_workspace_tests'):
            errors.append('unknown_change must require full workspace tests')
        if not decision.get('requires_cross_repo_validation'):
            errors.append('unknown_change must require cross-repo validation')
        if not decision.get('requires_codex_review'):
            errors.append('unknown_change must require Codex review')
        if not decision.get('requires_human_review'):
            errors.append('unknown_change must require human review')
        missing_unknown_vals = UNKNOWN_CHANGE_REQUIRED_VALIDATORS - validators
        if missing_unknown_vals:
            errors.append(
                'unknown_change must require validators: ' + ', '.join(sorted(missing_unknown_vals))
            )
        try:
            u_active = {normalize_pytest_repo_name(r) or r for r in active_repo_names(workspace) if r}
        except SystemExit:
            u_active = set()
        missing_unknown_pytest = u_active - required_pytest_repos
        if missing_unknown_pytest:
            errors.append(
                'unknown_change must list pytest for every active repo in required_pytest_repos: '
                + ', '.join(sorted(missing_unknown_pytest))
            )
    # When full workspace tests are required, required_pytest_repos must enumerate every active repo.
    if decision.get('requires_full_workspace_tests'):
        try:
            active = {normalize_pytest_repo_name(r) or r for r in active_repo_names(workspace) if r}
        except SystemExit:
            active = set()
        missing_active_in_required = active - required_pytest_repos
        if missing_active_in_required:
            errors.append(
                'requires_full_workspace_tests=true but required_pytest_repos missing active repos: '
                + ', '.join(sorted(missing_active_in_required))
            )
    if not args.allow_missing_run_evidence:
        ran_validators = set(args.ran_validator)
        ran_tests = set(args.ran_test_artifact)
        ran_pytest_raw = [normalize_pytest_repo_name(x) for x in args.ran_pytest_repo]
        if any(x is None for x in ran_pytest_raw):
            errors.append('invalid --ran-pytest-repo value (empty or unknown)')
        ran_pytest_repos = {x for x in ran_pytest_raw if x}
        missing_validators = validators - ran_validators
        missing_tests = required_tests - ran_tests
        missing_pytest_repos = required_pytest_repos - ran_pytest_repos
        if missing_validators:
            errors.append('required validators did not run: ' + ', '.join(sorted(missing_validators)))
        if missing_tests:
            errors.append('required test artifacts did not run: ' + ', '.join(sorted(missing_tests)))
        if missing_pytest_repos:
            errors.append('required pytest repos did not run: ' + ', '.join(sorted(missing_pytest_repos)))
        if decision.get('requires_full_workspace_tests'):
            try:
                active = {normalize_pytest_repo_name(r) or r for r in active_repo_names(workspace) if r}
            except SystemExit:
                active = set()
            missing_active_run = active - ran_pytest_repos
            if missing_active_run:
                errors.append(
                    'requires_full_workspace_tests=true but pytest did not run for: '
                    + ', '.join(sorted(missing_active_run))
                )
        unknown_validators = ran_validators - validators
        if unknown_validators:
            errors.append(
                'unknown ran validators not in required_validators: '
                + ', '.join(sorted(unknown_validators))
            )
        unknown_tests = ran_tests - required_tests
        if unknown_tests:
            errors.append(
                'unknown ran test artifacts not in required_test_artifacts: '
                + ', '.join(sorted(unknown_tests))
            )
        unknown_pytest_repos = ran_pytest_repos - required_pytest_repos
        if unknown_pytest_repos:
            errors.append(
                'unknown ran pytest repos not in required_pytest_repos: '
                + ', '.join(sorted(unknown_pytest_repos))
            )
    if errors:
        print('CI route decision validation failed:', file=sys.stderr)
        for e in errors:
            print(f'- {e}', file=sys.stderr)
        return 1
    print('CI route decision validation passed.')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
