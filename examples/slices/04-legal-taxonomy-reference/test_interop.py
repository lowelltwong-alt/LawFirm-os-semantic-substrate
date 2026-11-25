"""End-to-end tests from preserved local codes to scoped searches and SALI candidates."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import subprocess
import sys
import unittest

from engagement import EngagementView, read_bundle
from interop import Crosswalk, Vocabulary, inputs, run, verify_sali

HERE = Path(__file__).resolve().parent
OWL = Path(os.environ.get("LAWFIRM_TAXONOMY_SALI_OWL", "LMSS.owl"))
DATE = "2026-06-20"


class InteropTests(unittest.TestCase):
    def setUp(self):
        self.bundle, self.vocab, self.source, self.sali = inputs()

    def model(self):
        return Crosswalk(self.source, Vocabulary(self.vocab), {e["id"] for e in self.bundle["engagements"]})

    def view(self, when=DATE):
        return EngagementView(self.bundle, when)

    def assignment(self, code):
        return next(a for a in self.source["assignments"] if a["code"] == code)

    def rule(self, code):
        return next(a for a in self.source["maps"] if a["code"] == code)

    def test_cli_round_trip_source_and_search(self):
        cli = subprocess.run([sys.executable, "-B", str(HERE / "interop.py"), "--sali-owl", str(OWL)],
                             capture_output=True, text=True, check=False)
        self.assertEqual(0, cli.returncode, cli.stderr)
        result = json.loads(cli.stdout)
        self.assertEqual(10, result["verified_external_identifiers_and_named_parents"])
        self.assertEqual(self.source["assignments"], [x["assignment"] for x in result["mapped_sources"]])
        expected = {
            "premises": ["underlying-defense"], "tort_with_narrower_practices": ["underlying-defense"],
            "insurance_with_narrower_practices": ["coverage-declaration", "first-party-advice"],
            "deposition_document": ["underlying-defense"], "deposition_event": ["coverage-declaration"],
            "our_firm_insurer_representation": ["first-party-advice"],
        }
        self.assertEqual(expected, result["search"])
        self.assertTrue(result["sali_candidates"])
        self.assertEqual({"proposed"}, {x["status"] for x in result["sali_candidates"]})
        self.assertNotEqual(
            next(x["iri"] for x in result["sali_candidates"] if x["source_code"] == "DOC-17"),
            next(x["iri"] for x in result["sali_candidates"] if x["source_code"] == "WORK-DEP"),
        )

    def test_paid_or_billed_to_carrier_does_not_establish_client(self):
        mapped = self.model().derive(self.assignment("CARR-COV"))
        self.assertEqual("partial", mapped["status"])
        self.assertEqual(["billing-party"], mapped["unmapped_components"])
        self.assertEqual(["practice-coverage"], [x["target"] for x in mapped["targets"]])
        self.assertEqual("unknown",
                         self.view().party_role("underlying-defense", "carrier", "client")["state"])
        self.assertEqual(["first-party-advice"], self.view().represented("our-firm", "carrier"))

    def test_no_exact_match_for_due_diligence_by_name(self):
        x = self.model().derive(self.assignment("GEN-DD"))
        self.assertEqual("needs-review", x["status"])
        self.assertEqual([], x["targets"])
        self.assertEqual([], self.model().search("work-acquisition-dd", self.view()))

    def test_withdrawal_changes_projection_not_original(self):
        old = self.model()
        old_stamp = deepcopy(self.source["assignments"])
        self.rule("DOC-17")["review_status"] = "withdrawn"
        self.source["mapping_version"] = "0.1.1"
        new = self.model()
        self.assertEqual(["underlying-defense"], old.search("document-deposition", self.view()))
        self.assertEqual([], new.search("document-deposition", self.view()))
        self.assertEqual("withdrawn", new.derive(self.assignment("DOC-17"))["status"])
        self.assertEqual(old_stamp, self.source["assignments"])
        self.assertEqual("0.1.1", new.derive(self.assignment("DOC-17"))["mapping_version"])

    def test_forward_only_broader_mapping_and_reverse_ambiguity(self):
        model = self.model()
        self.assertEqual({"status": "needs-review", "candidates": ["PREM-NSEC"]},
                         model.reverse(["practice-premises"]))
        self.assertEqual({"status": "exact-round-trip", "candidates": ["WORK-DEP"]},
                         model.reverse(["work-deposition"]))
        self.assertEqual({"status": "needs-review", "candidates": ["DOC-17", "DOC-ALT"]},
                         model.reverse(["document-deposition"]))

    def test_unknown_source_code_and_version_are_preserved(self):
        model = self.model()
        row = self.assignment("DOC-17")
        unknown = {**row, "code": "UNKNOWN"}
        outdated = {**row, "source_revision": "archived"}
        for source, status in ((unknown, "unknown-code"), (outdated, "source-version-unavailable")):
            actual = model.derive(source)
            self.assertEqual(status, actual["status"])
            self.assertEqual(source, actual["assignment"])
            self.assertEqual([], actual["targets"])

    def test_ambiguous_direction_never_produces_search_tag(self):
        row = self.rule("DOC-17")["components"][0]
        for relation in ("close", "related", "narrower-target"):
            with self.subTest(relation=relation):
                row["relation"] = relation
                self.assertEqual([], self.model().search("document-deposition", self.view()))

    def test_filing_history_and_tag_history_separate(self):
        local = self.model()
        self.assertEqual([], local.search("document-deposition", self.view("2026-06-04")))
        self.assertEqual(["underlying-defense"], local.search("document-deposition", self.view("2026-06-05")))
        self.assertEqual([], local.search("document-deposition", self.view(), known_by="2026-06-04"))

    def test_mapped_component_cannot_claim_party_or_different_facet(self):
        self.rule("CARR-COV")["unmapped"] = []
        self.rule("CARR-COV")["components"].append(
            {"part": "billing-party", "target": "practice-insurance", "relation": "exact"})
        with self.assertRaisesRegex(ValueError, "invalid target facet"):
            self.model()

    def test_deprecated_term_can_be_read_but_active_mapping_cannot_use_it(self):
        concept = next(x for x in self.vocab["concepts"] if x["id"] == "practice-premises")
        concept.update(status="deprecated", replacement="practice-tort")
        self.assertIn("practice-premises", Vocabulary(self.vocab).concepts)
        with self.assertRaisesRegex(ValueError, "targets deprecated"):
            self.model()
        self.rule("PREM-NSEC")["review_status"] = "withdrawn"
        self.assertEqual([], self.model().search("practice-tort", self.view(), narrower=True))

    def test_structure_rejects_scope_cycles_and_bad_version(self):
        self.source["target_version"] = "different"
        with self.assertRaisesRegex(ValueError, "different vocabulary revision"):
            self.model()
        self.source["target_version"] = self.vocab["version"]
        tort = next(x for x in self.vocab["concepts"] if x["id"] == "practice-tort")
        for parent, message in (("practice-premises", "hierarchy cycle"), ("issue-negligence", "invalid broader")):
            with self.subTest(parent=parent):
                tort["broader"] = parent
                with self.assertRaisesRegex(ValueError, message):
                    self.model()

    def test_missing_compound_component_is_rejected(self):
        self.rule("CARR-COV")["unmapped"] = []
        with self.assertRaisesRegex(ValueError, "component inventory incomplete"):
            self.model()

    def test_new_practice_is_data_only_and_preserves_previous_results(self):
        old = self.model()
        previous = deepcopy(self.bundle)
        old_search = old.search("practice-tort", EngagementView(previous, DATE), narrower=True)
        self.vocab["version"] = "0.2.0"
        self.source["target_version"] = "0.2.0"
        self.source["mapping_version"] = "0.2.0"
        concept = read_bundle(HERE / "practice-extension.example.json")
        self.vocab["concepts"].append(concept)
        self.bundle["matters"].append({"id": "solvent-matter", "incident": "solvent-incident",
                                        "label": "Fictional chemical release civil suit"})
        self.bundle["engagements"].append({"id": "solvent-defense", "matter": "solvent-matter",
                                           "service": "underlying-defense", "period": {"from": "2026-05-01"}})
        self.source["codes"].append({"code": "ENV-CIV", "definition": "Environmental tort litigation",
                                     "components": ["practice-kind"]})
        self.source["maps"].append({"id": "env-map", "code": "ENV-CIV", "review_status": "synthetic-verified",
                                    "rationale": "Synthetic definition matches the environmental tort scope.",
                                    "components": [{"part": "practice-kind", "target": concept["id"],
                                                    "relation": "exact"}], "unmapped": []})
        self.source["assignments"].append({"id": "a-env", "engagement": "solvent-defense",
                                           "code": "ENV-CIV", "source_revision": self.source["version"],
                                           "effective": "2026-05-01", "observed": "2026-05-02"})
        new = self.model()
        self.assertEqual(["underlying-defense"], old_search)
        self.assertEqual(["solvent-defense", "underlying-defense"],
                         new.search("practice-tort", self.view(), narrower=True))
        self.assertEqual(["solvent-defense"], new.search(concept["id"], self.view()))
        self.assertEqual(["underlying-defense"], new.search("practice-premises", self.view()))

    def test_sali_digest_and_wrong_semantic_parent_are_rejected(self):
        vocabulary = Vocabulary(self.vocab)
        with TemporaryDirectory() as folder:
            bad = Path(folder) / "changed.owl"
            bad.write_bytes(b"wrong snapshot")
            with self.assertRaisesRegex(ValueError, "checksum"):
                verify_sali(self.sali, vocabulary, bad)
        self.sali["terms"][0]["parent_iri"] = self.sali["terms"][1]["parent_iri"]
        self.sali["terms"][0]["parent_label"] = self.sali["terms"][1]["parent_label"]
        with self.assertRaisesRegex(ValueError, "named parent mismatch"):
            verify_sali(self.sali, vocabulary, OWL)

    def test_no_exact_sali_chain_from_two_local_concepts(self):
        row = deepcopy(self.sali["terms"][0])
        row["concept"] = "work-deposition"
        self.sali["terms"].append(row)
        with self.assertRaisesRegex(ValueError, "not one to one"):
            verify_sali(self.sali, Vocabulary(self.vocab), OWL)

    def test_release_projection_does_not_change_source_engagements(self):
        before = deepcopy(self.bundle)
        result = run(DATE, OWL)
        self.assertEqual(before, self.bundle)
        after = inputs()[0]
        self.assertEqual(before, after)
        self.assertEqual(["first-party-advice"], result["search"]["our_firm_insurer_representation"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
