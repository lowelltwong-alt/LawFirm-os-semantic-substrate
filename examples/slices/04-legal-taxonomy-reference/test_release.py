"""Check immutable candidate snapshots and reproduce their local query results."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json
import os
import subprocess
import sys
import unittest

from release import HERE, freeze, read_archive, strict_json, verify

OWL = Path(os.environ.get("LAWFIRM_TAXONOMY_SALI_OWL", "LMSS.owl"))


def simulation_payload(base, source, bumped=True):
    _, contents = read_archive(base)
    source.mkdir()
    for name, data in contents.items():
        (source / name).write_bytes(data)
    path = source / "fictional-firm-crosswalk.json"
    dictionary = strict_json(path.read_bytes())
    target = next(rule for rule in dictionary["maps"] if rule["code"] == "DOC-17")
    target["review_status"] = "withdrawn"
    if bumped:
        dictionary["mapping_version"] = "0.1.1"
    path.write_text(json.dumps(dictionary, indent=2) + "\n", encoding="utf-8")


def replay(archive, destination, owl=OWL):
    _, contents = read_archive(archive)
    destination.mkdir()
    for name, data in contents.items():
        (destination / name).write_bytes(data)
    command = [sys.executable, "-B", str(destination / "interop.py"), "--sali-owl", str(owl)]
    return json.loads(subprocess.check_output(command))


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.base = self.root / "base.zip"
        self.original = freeze(HERE, self.base, "0.1.0")

    def test_identical_input_builds_identical_zip(self):
        repeat = self.root / "repeat.zip"
        self.assertEqual(self.original, freeze(HERE, repeat, "0.1.0"))
        self.assertEqual(self.base.read_bytes(), repeat.read_bytes())

    def test_existing_archive_cannot_be_rewritten(self):
        before = self.base.read_bytes()
        with self.assertRaises(FileExistsError):
            freeze(HERE, self.base, "0.1.1", self.base)
        self.assertEqual(before, self.base.read_bytes())

    def test_new_release_needs_new_version(self):
        with self.assertRaisesRegex(ValueError, "higher version"):
            freeze(HERE, self.root / "next.zip", "0.1.0", self.base)

    def test_mapping_edit_without_revision_is_rejected(self):
        changed = self.root / "source"
        simulation_payload(self.base, changed, bumped=False)
        with self.assertRaisesRegex(ValueError, "crosswalk revision"):
            freeze(changed, self.root / "next.zip", "0.1.1", self.base)

    def test_tampered_payload_fails_at_exact_check(self):
        broken = self.root / "broken.zip"
        with ZipFile(self.base) as old, ZipFile(broken, "w") as new:
            for name in old.namelist():
                data = old.read(name)
                new.writestr(name, data + b"\n" if name == "interop.py" else data)
        with self.assertRaisesRegex(ValueError, "payload mismatch"):
            verify(broken)

    def test_unexpected_file_fails(self):
        extra = self.root / "extra.zip"
        extra.write_bytes(self.base.read_bytes())
        with ZipFile(extra, "a") as archive:
            archive.writestr("unknown.txt", "extra file")
        with self.assertRaisesRegex(ValueError, "unexpected"):
            verify(extra)

    def test_wrong_predecessor_or_independent_fingerprint_fails(self):
        alternative = self.root / "alternative.zip"
        freeze(HERE, alternative, "0.0.9")
        next_release = self.root / "next.zip"
        freeze(HERE, next_release, "0.1.1", self.base)
        with self.assertRaisesRegex(ValueError, "predecessor fingerprint"):
            verify(next_release, alternative)
        with self.assertRaisesRegex(ValueError, "independent receipt"):
            verify(next_release, fingerprint=self.original["fingerprint"])

    def test_external_source_pin(self):
        self.assertTrue(verify(self.base, owl=OWL)["external_sali_checked"])
        other = self.root / "wrong.owl"
        other.write_bytes(b"unverified external snapshot")
        with self.assertRaisesRegex(ValueError, "external SALI dependency checksum"):
            verify(self.base, owl=other)

    def test_snapshot_replay_before_and_after_mapping_withdrawal(self):
        source = self.root / "source"
        simulation_payload(self.base, source)
        new_path = self.root / "new.zip"
        new_manifest = freeze(source, new_path, "0.1.1", self.base)
        self.assertTrue(verify(new_path, self.base, OWL, new_manifest["fingerprint"])["predecessor_verified"])
        self.assertNotEqual(self.original["fingerprint"], new_manifest["fingerprint"])

        prior = replay(self.base, self.root / "old")
        current = replay(new_path, self.root / "new")
        self.assertEqual(["underlying-defense"], prior["search"]["deposition_document"])
        self.assertEqual([], current["search"]["deposition_document"])
        self.assertEqual(prior["search"]["deposition_event"], current["search"]["deposition_event"])
        expected = deepcopy(prior["search"])
        expected["deposition_document"] = []
        self.assertEqual(expected, current["search"])
        old_rows = {x["assignment"]["id"]: x["assignment"] for x in prior["mapped_sources"]}
        new_rows = {x["assignment"]["id"]: x["assignment"] for x in current["mapped_sources"]}
        self.assertEqual(old_rows, new_rows)
        self.assertEqual(prior, replay(self.base, self.root / "old-again"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
