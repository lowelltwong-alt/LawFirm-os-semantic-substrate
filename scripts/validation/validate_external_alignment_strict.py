from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
ADR_DIR = ROOT / 'docs' / 'adr'
REGISTRY_PATH = ROOT / 'standards' / 'external-standards-registry.yaml'
MAPPING_PATH = ROOT / 'standards' / 'intake-conflicts-ai-standards-mapping.yaml'

REQUIRED_ADRS = {
    'ADR-0001',
    'ADR-0002',
    'ADR-0003',
    'ADR-0004',
}
REQUIRED_DOCS = [
    ROOT / 'docs' / 'governance' / 'external-ontology-alignment.md',
    ROOT / 'docs' / 'governance' / 'world-class-ontology-criteria.md',
    ROOT / 'docs' / 'poc' / 'CINO_why_this_stack.md',
]
ALLOWED_ADOPTION_STATUS = {'adopt_now', 'selective', 'watchlist_later'}
REQUIRED_STANDARD_FIELDS = {
    'id',
    'name',
    'adoption_status',
    'why_status',
    'why_fmg_fit',
    'why_not_core',
    'benefits_now',
    'risks_if_overused',
    'revisit_triggers',
    'pilot_usage',
    'adr_ref',
}


def load_yaml(path: Path):
    with path.open('r', encoding='utf-8') as handle:
        return yaml.safe_load(handle)


def main() -> int:
    failures = []

    for path in REQUIRED_DOCS:
        if not path.exists():
            failures.append(f'missing required doc: {path.relative_to(ROOT)}')

    for adr in REQUIRED_ADRS:
        matches = list(ADR_DIR.glob(f'{adr}-*.md'))
        if not matches:
            failures.append(f'missing ADR for {adr}')

    if not REGISTRY_PATH.exists():
        failures.append(f'missing registry: {REGISTRY_PATH.relative_to(ROOT)}')
    if not MAPPING_PATH.exists():
        failures.append(f'missing mapping: {MAPPING_PATH.relative_to(ROOT)}')

    registry_ids = set()
    if REGISTRY_PATH.exists():
        registry = load_yaml(REGISTRY_PATH)
        standards = registry.get('standards', []) if isinstance(registry, dict) else []
        if not isinstance(standards, list) or not standards:
            failures.append('registry standards list is missing or empty')
        else:
            for idx, entry in enumerate(standards, start=1):
                if not isinstance(entry, dict):
                    failures.append(f'registry entry {idx} is not a mapping')
                    continue
                missing = REQUIRED_STANDARD_FIELDS - set(entry.keys())
                if missing:
                    failures.append(f"registry entry {entry.get('id', idx)} missing fields: {sorted(missing)}")
                status = entry.get('adoption_status')
                if status not in ALLOWED_ADOPTION_STATUS:
                    failures.append(f"registry entry {entry.get('id', idx)} has invalid adoption_status: {status}")
                entry_id = entry.get('id')
                if isinstance(entry_id, str):
                    registry_ids.add(entry_id)
                adr_ref = entry.get('adr_ref')
                if isinstance(adr_ref, str) and adr_ref not in REQUIRED_ADRS:
                    failures.append(f"registry entry {entry.get('id', idx)} references unknown adr_ref: {adr_ref}")

    if MAPPING_PATH.exists():
        mapping = load_yaml(MAPPING_PATH)
        objects = mapping.get('pilot_objects', []) if isinstance(mapping, dict) else []
        if not isinstance(objects, list) or not objects:
            failures.append('mapping pilot_objects list is missing or empty')
        else:
            for obj in objects:
                for mapping_entry in obj.get('standard_mappings', []):
                    std_id = mapping_entry.get('standard_id')
                    if std_id not in registry_ids:
                        failures.append(f'mapping references unknown standard_id: {std_id}')

    if failures:
        print('STRICT EXTERNAL ALIGNMENT VALIDATION FAILURES:')
        for failure in failures:
            print(f'- {failure}')
        return 1

    print('Strict external alignment validation passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
