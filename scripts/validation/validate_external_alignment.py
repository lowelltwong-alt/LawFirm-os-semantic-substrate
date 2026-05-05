from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
ADR_DIR = ROOT / 'docs' / 'adr'

REQUIRED_ADRS = [
    'ADR-0001-external-standards-adoption-model.md',
    'ADR-0002-foundation-standards-adopt-now.md',
    'ADR-0003-selective-standards-policy.md',
    'ADR-0004-legal-ontology-watchlist.md',
]

REQUIRED_DOCS = [
    ROOT / 'docs' / 'governance' / 'external-ontology-alignment.md',
    ROOT / 'docs' / 'governance' / 'world-class-ontology-criteria.md',
    ROOT / 'docs' / 'poc' / 'CINO_why_this_stack.md',
]


def main() -> int:
    failures = []

    for name in REQUIRED_ADRS:
        path = ADR_DIR / name
        if not path.exists():
            failures.append(f'missing ADR: {path.relative_to(ROOT)}')

    for path in REQUIRED_DOCS:
        if not path.exists():
            failures.append(f'missing required doc: {path.relative_to(ROOT)}')

    if failures:
        print('EXTERNAL ALIGNMENT VALIDATION FAILURES:')
        for failure in failures:
            print(f'- {failure}')
        return 1

    print('External alignment validation scaffold passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
