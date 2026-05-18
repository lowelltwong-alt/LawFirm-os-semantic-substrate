"""validate_contract_surface_provenance_modes.py

Deterministic anti-regression validator for the LawFirm OS contract surface
locking bug class.

Goal:
    Prevent any producer, consumer, validator, or test fixture from ever again
    claiming committed-tree provenance (contract_surface_lock.computed_from_commit
    or contract_surface_lock.substrate_repo_commit_sha) while actually hashing
    mutable working-tree or temp-copy filesystem bytes.

Background:
    On Windows with core.autocrlf=true, working-tree bytes can be CRLF while
    Git blob bytes are LF. A consumer that recomputes the surface hash from
    working-tree bytes against a lock that was computed from committed-tree
    bytes will see a false drift. The fix is to validate committed Git-tree
    blob bytes whenever the lock pins a committed commit. This validator
    statically enforces that invariant across all five LawFirm OS repos.

Scope:
    Scans Python source files under scripts/, src/, tests/ in each of:
      - LawFirm-os-semantic-substrate
      - LawFirm-os-orchestrator
      - LawFirm-os-exceptions-lake-runtime (or -main)
      - LawFirm-os-legal-knowledge-runtime
      - LawFirm-os-skills-registry
    A file is inspected only if it mentions one of:
      contract_surface_lock, computed_from_commit, surface_sha256,
      compute_contract_surface
    so this validator does not slow CI on unrelated code.

Rules (each rule fails closed when violated):
    C1  A function writes "computed_from_commit" as a dict literal key or
        subscript assignment, AND in the same function body has a `for`-loop
        whose iterator is a Path.rglob / Path.glob / Path.iterdir / os.walk
        call AND whose body reads file bytes via Path.read_bytes / Path.read_text,
        AND the function does NOT contain any git-plumbing marker (subprocess
        invocation of `git show`, `git ls-tree`, `git archive`, `git cat-file`,
        or a helper like `_git_show_bytes`, `_git_read_blob`, `_git_ls_tree`,
        `_git_cat_file_batch`, `_git_ls_tree_blob_index`, `_git_bytes`,
        `compute_contract_surface_from_git_tree`,
        `discover_included_files_from_git_tree`,
        `compute_committed_surface_result`).
        Meaning: this function silently claims committed-tree provenance for
        bytes it hashed from the filesystem. That is exactly the bug class.

    C2  A function contains an `if` whose test references `working_tree`
        (e.g. `args.working_tree` or `working_tree=True`) AND the if-body
        contains a dict literal/subscript that assigns "computed_from_commit"
        to anything other than the constant None. Meaning: the working-tree
        branch is claiming committed-tree provenance.

    C3  A function calls `shutil.copytree(...)` AND constructs a dict literal
        or subscript assignment with "computed_from_commit", AND does NOT
        invoke `subprocess.run(["git", "init", ...])` /
        `subprocess.run(["git", "archive", ...])` or a `_init_git_repo` /
        `init_git_repo` helper in the same function body. Meaning: this
        fixture copies working-tree bytes and still claims committed-tree
        provenance, without first making those bytes a committed git tree.

Safe patterns (do not trigger):
    - Functions that only use git plumbing (git show / git ls-tree / git
      archive / git cat-file or helpers).
    - Functions that read a single specific file by name (e.g.
      `lock_path.read_text(...)` on contracts.lock.json or a registry JSON)
      without iterating the filesystem via rglob/glob/iterdir.
    - Legacy locks without a contract_surface_lock block (filesystem hashing
      without `computed_from_commit` is acceptable for legacy behaviour).
    - Comments, docstrings, and string literals are ignored (AST traversal
      only inspects executable code).

Output:
    Findings are line-numbered against the source file:
        <repo>/<rel_path>:<lineno>: <rule_id>: <message>
    Exit code 0 means no findings; 1 means at least one finding.

This validator does not modify any file and has no side effects.
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_NAMES = (
    "LawFirm-os-semantic-substrate",
    "LawFirm-os-orchestrator",
    "LawFirm-os-exceptions-lake-runtime",
    "LawFirm-os-exceptions-lake-runtime-main",
    "LawFirm-os-legal-knowledge-runtime",
    "LawFirm-os-skills-registry",
)

SCAN_SUBDIRS = ("scripts", "src", "tests")

RELEVANCE_KEYWORDS = (
    "contract_surface_lock",
    "computed_from_commit",
    "surface_sha256",
    "compute_contract_surface",
)

# Names of helpers / module-level callables that route through Git plumbing.
# Match by terminal call name (function name or attribute name).
GIT_PLUMBING_CALL_NAMES = frozenset(
    {
        "_git_show_bytes",
        "_git_read_blob",
        "_git_ls_tree",
        "_git_ls_tree_blob_index",
        "_git_cat_file_batch",
        "_git_bytes",
        "_git_show",
        "compute_contract_surface_from_git_tree",
        "discover_included_files_from_git_tree",
        "compute_committed_surface_result",
    }
)

# subprocess.run(["git", "<verb>", ...]) verbs that count as committed-tree reads
GIT_PLUMBING_VERBS = frozenset({"show", "ls-tree", "archive", "cat-file"})

# subprocess.run(["git", "<verb>", ...]) verbs that count as building a fresh
# committed git tree for a fixture
GIT_INIT_VERBS = frozenset({"init", "archive"})

# Helper names that initialize a fresh git repo in a fixture context.
GIT_INIT_HELPER_NAMES = frozenset({"_init_git_repo", "init_git_repo", "_init_repo_from_substrate"})

PATH_ITER_METHODS = frozenset({"rglob", "glob", "iterdir"})
PATH_READ_METHODS = frozenset({"read_bytes", "read_text"})


@dataclass(frozen=True)
class Finding:
    rule_id: str
    file: Path
    lineno: int
    message: str

    def render(self, root: Path) -> str:
        try:
            rel = self.file.relative_to(root)
        except ValueError:
            rel = self.file
        return f"{rel.as_posix()}:{self.lineno}: {self.rule_id}: {self.message}"


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------


def _call_terminal_name(call: ast.Call) -> str | None:
    """Return the terminal callable name of a Call node (function name or attr)."""
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _string_list_first_two(node: ast.AST) -> tuple[str | None, str | None]:
    """If node is a list/tuple literal, return its first two string constants."""
    if isinstance(node, (ast.List, ast.Tuple)):
        out: list[str | None] = []
        for elt in node.elts[:2]:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                out.append(elt.value)
            else:
                out.append(None)
        while len(out) < 2:
            out.append(None)
        return out[0], out[1]
    return None, None


def _function_calls_git_verb(func: ast.AST, verbs: frozenset[str]) -> bool:
    """True if any Call in func has a first-arg list whose first two strings are ('git', <verb in verbs>)."""
    for node in ast.walk(func):
        if isinstance(node, ast.Call):
            for arg in node.args:
                head, second = _string_list_first_two(arg)
                if head == "git" and second in verbs:
                    return True
    return False


def _function_calls_named(func: ast.AST, names: frozenset[str]) -> bool:
    for node in ast.walk(func):
        if isinstance(node, ast.Call):
            name = _call_terminal_name(node)
            if name in names:
                return True
    return False


def function_has_git_plumbing(func: ast.AST) -> bool:
    return _function_calls_git_verb(func, GIT_PLUMBING_VERBS) or _function_calls_named(
        func, GIT_PLUMBING_CALL_NAMES
    )


def function_has_git_init(func: ast.AST) -> bool:
    return _function_calls_git_verb(func, GIT_INIT_VERBS) or _function_calls_named(
        func, GIT_INIT_HELPER_NAMES
    )


def function_uses_shutil_copytree(func: ast.AST) -> bool:
    return _function_calls_named(func, frozenset({"copytree"}))


def _filesystem_iterator_iter(node: ast.AST) -> bool:
    """True if node is (sorted(...) wrapping) a Path.rglob/glob/iterdir call or os.walk."""
    inner: ast.AST = node
    if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name) and inner.func.id == "sorted":
        if inner.args:
            inner = inner.args[0]
    if isinstance(inner, ast.Call):
        if isinstance(inner.func, ast.Attribute) and inner.func.attr in PATH_ITER_METHODS:
            return True
        if isinstance(inner.func, ast.Attribute) and inner.func.attr == "walk":
            # os.walk(...)
            owner = inner.func.value
            if isinstance(owner, ast.Name) and owner.id == "os":
                return True
        if isinstance(inner.func, ast.Name) and inner.func.id == "walk":
            return True
    return False


def function_iterates_paths_and_reads_bytes(func: ast.AST) -> bool:
    for node in ast.walk(func):
        if isinstance(node, ast.For) and _filesystem_iterator_iter(node.iter):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                    if sub.func.attr in PATH_READ_METHODS:
                        return True
    return False


def function_writes_computed_from_commit(func: ast.AST) -> int | None:
    """Return the lineno of the first computed_from_commit write, or None."""
    first_line: int | None = None
    for node in ast.walk(func):
        if isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and k.value == "computed_from_commit":
                    if first_line is None or k.lineno < first_line:
                        first_line = k.lineno
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript):
                    s = target.slice
                    if isinstance(s, ast.Constant) and s.value == "computed_from_commit":
                        ln = target.lineno
                        if first_line is None or ln < first_line:
                            first_line = ln
    return first_line


def _references_working_tree(node: ast.AST) -> bool:
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and sub.id == "working_tree":
            return True
        if isinstance(sub, ast.Attribute) and sub.attr == "working_tree":
            return True
    return False


def _block_assigns_computed_to_non_none(stmts: list[ast.AST]) -> int | None:
    """Walk stmts; return lineno of first non-None assignment to computed_from_commit."""
    for stmt in stmts:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Dict):
                for k, v in zip(node.keys, node.values):
                    if isinstance(k, ast.Constant) and k.value == "computed_from_commit":
                        if not (isinstance(v, ast.Constant) and v.value is None):
                            return k.lineno
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Subscript):
                        s = target.slice
                        if isinstance(s, ast.Constant) and s.value == "computed_from_commit":
                            v = node.value
                            if not (isinstance(v, ast.Constant) and v.value is None):
                                return target.lineno
    return None


# ---------------------------------------------------------------------------
# Rule checks
# ---------------------------------------------------------------------------


def _walk_functions(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def check_function(func: ast.AST, file: Path) -> list[Finding]:
    findings: list[Finding] = []
    fname = getattr(func, "name", "<anonymous>")

    writes_commit_line = function_writes_computed_from_commit(func)

    # C1
    if (
        writes_commit_line is not None
        and function_iterates_paths_and_reads_bytes(func)
        and not function_has_git_plumbing(func)
    ):
        findings.append(
            Finding(
                rule_id="C1",
                file=file,
                lineno=writes_commit_line,
                message=(
                    f"function {fname!r} writes contract_surface_lock.computed_from_commit "
                    "and hashes file bytes via Path iteration + Path.read_bytes/read_text "
                    "without any git-plumbing helper. Committed-tree provenance must be "
                    "computed from committed Git-tree blob bytes (git show / git ls-tree / "
                    "git cat-file), not mutable working-tree bytes."
                ),
            )
        )

    # C2
    for node in ast.walk(func):
        if isinstance(node, ast.If) and _references_working_tree(node.test):
            bad_line = _block_assigns_computed_to_non_none(node.body)
            if bad_line is not None:
                findings.append(
                    Finding(
                        rule_id="C2",
                        file=file,
                        lineno=bad_line,
                        message=(
                            f"function {fname!r} sets computed_from_commit to a non-None value "
                            "inside an if-branch whose test references working_tree. The "
                            "working-tree branch must either omit computed_from_commit or set "
                            "it explicitly to None."
                        ),
                    )
                )

    # C3
    if (
        function_uses_shutil_copytree(func)
        and writes_commit_line is not None
        and not function_has_git_init(func)
    ):
        findings.append(
            Finding(
                rule_id="C3",
                file=file,
                lineno=writes_commit_line,
                message=(
                    f"function {fname!r} uses shutil.copytree and claims "
                    "contract_surface_lock.computed_from_commit without calling "
                    "subprocess.run(['git','init',...]) / subprocess.run(['git','archive',...]) "
                    "or a _init_git_repo helper in the same function. A copytree fixture "
                    "must materialise a committed git tree before claiming committed-tree "
                    "provenance."
                ),
            )
        )

    return findings


def scan_python_source(source: str, filename: str | Path = "<inline>") -> list[Finding]:
    """Inspect a Python source string and return a list of Findings.

    Public entry point for testing. The filename argument is used only for
    error reporting; the source is parsed in-memory.
    """
    file = Path(filename)
    try:
        tree = ast.parse(source, filename=str(file))
    except SyntaxError:
        return []
    findings: list[Finding] = []
    for func in _walk_functions(tree):
        findings.extend(check_function(func, file))
    return findings


def scan_python_file(file: Path) -> list[Finding]:
    try:
        source = file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    if not any(kw in source for kw in RELEVANCE_KEYWORDS):
        return []
    return scan_python_source(source, file)


def _iter_python_files(repo_root: Path):
    for sub in SCAN_SUBDIRS:
        d = repo_root / sub
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*.py")):
            parts = set(p.relative_to(repo_root).parts)
            if "__pycache__" in parts or ".pytest_cache" in parts:
                continue
            yield p


def scan_workspace(workspace: Path) -> list[Finding]:
    findings: list[Finding] = []
    for name in REPO_NAMES:
        repo = workspace / name
        if not repo.is_dir():
            continue
        for py in _iter_python_files(repo):
            findings.extend(scan_python_file(py))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Anti-regression validator for the LawFirm OS committed-tree-vs-working-tree contract surface hash bug class."
    )
    ap.add_argument("--workspace", default=".", help="Workspace root containing the LawFirm-os-* repos.")
    args = ap.parse_args()
    workspace = Path(args.workspace).resolve()
    findings = scan_workspace(workspace)
    if findings:
        print("Contract surface provenance-mode validation FAILED.", file=sys.stderr)
        print(
            "Each finding is a place where committed-tree contract surface provenance "
            "could be backed by mutable working-tree or temp-copy filesystem bytes.",
            file=sys.stderr,
        )
        for f in findings:
            print("- " + f.render(workspace), file=sys.stderr)
        return 1
    print("Contract surface provenance-mode validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
