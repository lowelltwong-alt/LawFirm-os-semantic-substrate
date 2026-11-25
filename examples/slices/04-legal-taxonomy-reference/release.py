"""Create and verify a content-pinned, standalone taxonomy candidate snapshot."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from zipfile import BadZipFile, ZipFile, ZipInfo
import json
import re

HERE = Path(__file__).resolve().parent
PAYLOAD = (
    "engagement.py", "engagement.schema.json", "fictional-firm-crosswalk.json", "interop.py",
    "interop.schema.json", "practice-extension.example.json", "practice-vocabulary.json",
    "sali-alignment.proposed.json", "test_engagement.py", "test_interop.py", "worked-matters.json",
)
MANIFEST = "release-manifest.json"
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def digest(data):
    return sha256(data).hexdigest()


def strict_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(data, object_pairs_hook=unique)


def ordered_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def version_parts(value):
    if not isinstance(value, str) or not VERSION.fullmatch(value):
        raise ValueError(f"expected a numeric major.minor.patch release: {value}")
    return tuple(map(int, value.split(".")))


def describe(payload, release, predecessor):
    version_parts(release)
    vocabulary = strict_json(payload["practice-vocabulary.json"])
    dictionary = strict_json(payload["fictional-firm-crosswalk.json"])
    standard = strict_json(payload["sali-alignment.proposed.json"])
    return {
        "format": "lawfirm-taxonomy-release-candidate-v1",
        "release": release,
        "predecessor": predecessor,
        "components": {
            "vocabulary": {"id": vocabulary["id"], "version": vocabulary["version"]},
            "source_dictionary": {"id": dictionary["id"], "version": dictionary["version"]},
            "crosswalk_version": dictionary["mapping_version"],
            "sali": {k: standard[k] for k in ("release", "commit", "sha256", "ontology", "license")},
        },
        "payload": {name: {"bytes": len(payload[name]), "sha256": digest(payload[name])}
                    for name in PAYLOAD},
        "authority": "candidate-only",
    }


def predecessor_validation(current, previous, manifest, prior):
    if version_parts(manifest["release"]) <= version_parts(prior["release"]):
        raise ValueError("new release must have a higher version")
    a, b = (strict_json(p["practice-vocabulary.json"]) for p in (previous, current))
    if a != b and a["version"] == b["version"]:
        raise ValueError("vocabulary changed without a new vocabulary revision")
    a, b = (strict_json(p["fictional-firm-crosswalk.json"]) for p in (previous, current))
    if a["codes"] != b["codes"] and a["version"] == b["version"]:
        raise ValueError("dictionary changed without a new dictionary revision")
    if a["maps"] != b["maps"] and a["mapping_version"] == b["mapping_version"]:
        raise ValueError("mapping changed without a new crosswalk revision")


def read_archive(path):
    with ZipFile(path) as archive:
        if sorted(archive.namelist()) != sorted((*PAYLOAD, MANIFEST)):
            raise ValueError("archive has missing, unexpected or duplicate entries")
        payload = {name: archive.read(name) for name in PAYLOAD}
        claimed = strict_json(archive.read(MANIFEST))
    if set(claimed) != {"format", "release", "predecessor", "components", "payload", "authority", "fingerprint"}:
        raise ValueError("invalid manifest field inventory")
    expected = describe(payload, claimed["release"], claimed["predecessor"])
    if claimed != {**expected, "fingerprint": digest(ordered_json(expected))}:
        raise ValueError("release manifest or payload mismatch")
    return claimed, payload


def freeze(source, output, release, predecessor=None):
    payload = {}
    for name in PAYLOAD:
        path = Path(source) / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"payload needs a regular file: {name}")
        payload[name] = path.read_bytes()
    if predecessor:
        prior, previous = read_archive(predecessor)
        reference = {field: prior[field] for field in ("release", "fingerprint")}
    else:
        reference = None
    manifest = describe(payload, release, reference)
    if predecessor:
        predecessor_validation(payload, previous, manifest, prior)
    manifest["fingerprint"] = digest(ordered_json(manifest))
    with Path(output).open("xb") as target:
        with ZipFile(target, "w") as archive:
            for name, data in sorted({**payload, MANIFEST: ordered_json(manifest)}.items()):
                archive.writestr(ZipInfo(name), data)
    return manifest


def verify(path, predecessor=None, owl=None, fingerprint=None):
    manifest, payload = read_archive(path)
    if fingerprint and manifest["fingerprint"] != fingerprint:
        raise ValueError("release fingerprint does not match independent receipt")
    linked = None
    if predecessor:
        prior, previous = read_archive(predecessor)
        if {k: prior[k] for k in ("release", "fingerprint")} != manifest["predecessor"]:
            raise ValueError("predecessor fingerprint or release mismatch")
        predecessor_validation(payload, previous, manifest, prior)
        linked = True
    if owl and digest(Path(owl).read_bytes()) != manifest["components"]["sali"]["sha256"]:
        raise ValueError("external SALI dependency checksum mismatch")
    return {"snapshot_integrity": True, "predecessor_verified": linked, "external_sali_checked": bool(owl),
            "release": manifest["release"], "fingerprint": manifest["fingerprint"],
            "authority": "candidate-only; no qualification or write clearance"}


def main():
    parser = ArgumentParser(description=__doc__)
    verbs = parser.add_subparsers(dest="verb", required=True)
    build = verbs.add_parser("freeze")
    build.add_argument("--source", type=Path, default=HERE)
    build.add_argument("--version", required=True)
    build.add_argument("--output", required=True, type=Path)
    build.add_argument("--predecessor", type=Path)
    check = verbs.add_parser("verify")
    check.add_argument("archive", type=Path)
    check.add_argument("--predecessor", type=Path)
    check.add_argument("--sali-owl", type=Path)
    check.add_argument("--fingerprint")
    args = parser.parse_args()
    try:
        result = (freeze(args.source, args.output, args.version, args.predecessor) if args.verb == "freeze"
                  else verify(args.archive, args.predecessor, args.sali_owl, args.fingerprint))
    except (OSError, ValueError, TypeError, KeyError, BadZipFile) as exc:
        parser.exit(1, f"{exc}\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
