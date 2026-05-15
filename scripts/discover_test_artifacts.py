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

def main() -> int:
    ap = argparse.ArgumentParser(description='Discover likely test artifacts across the LawFirm OS workspace.')
    ap.add_argument('--workspace', default='.', help='Parent workspace containing LawFirm-os-* repos')
    ap.add_argument('--out', default=None, help='Optional JSON output path')
    args = ap.parse_args()
    workspace = Path(args.workspace).resolve()
    repos = discover_repo_dirs(workspace)
    result = {'schema_version':'test_artifact_discovery.v1','workspace':str(workspace),'repos':{}}
    for repo, repo_dir in sorted(repos.items()):
        result['repos'][repo] = discover_test_artifacts_for_repo(repo_dir)
    text = dump_json(result)
    if args.out:
        Path(args.out).write_text(text, encoding='utf-8')
    else:
        print(text, end='')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
