from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]

SKIP_DIR_NAMES = {
    '.git',
    '.venv',
    'venv',
    '__pycache__',
    'node_modules',
}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def main() -> int:
    failures: list[str] = []

    for path in sorted(ROOT.rglob('*.yaml')):
        if should_skip(path):
            continue
        try:
            with path.open('r', encoding='utf-8') as handle:
                yaml.safe_load(handle)
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    if failures:
        print('REPO YAML PARSE FAILURES:')
        for failure in failures:
            print(f'- {failure}')
        return 1

    print('Repo-wide YAML parsing passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
