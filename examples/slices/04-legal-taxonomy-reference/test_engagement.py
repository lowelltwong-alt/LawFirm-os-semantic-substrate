"""Disclosed conformance tests for the synthetic engagement candidate."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

from engagement import EngagementView, lint, read_bundle

ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "worked-matters.json"


class EngagementTests(unittest.TestCase):
    def setUp(self):
        self.data = read_bundle(EXAMPLES)

    def view(self, day="2026-06-20", known_by=None):
        return EngagementView(self.data, day, known_by)

    def value(self, result, expected):
        self.assertEqual("known", result.get("state"))
        self.assertEqual(expected, result.get("value"))
        self.assertTrue(result.get("evidence"))

    def position(self, day, issue="duty-to-defend", excess=False):
        policy = "excess-policy" if excess else "primary-policy"
        actor = "excess-carrier" if excess else "carrier"
        return self.view(day).coverage("coverage-declaration", policy, issue, actor, "position")

    def test_clean_bundle(self):
        self.assertEqual([], lint(self.data))

    def test_default_counsel_distinguishes_engagements(self):
        self.assertEqual(["underlying-defense"], self.view().represented("our-firm", "hotel"))
        self.assertEqual(["first-party-advice"], self.view().represented("our-firm", "carrier"))
        self.assertEqual(["coverage-declaration"], self.view().represented("outside-firm", "carrier"))

    def test_client_evidence_removed(self):
        self.data["roles"] = [row for row in self.data["roles"]
                              if not (row["engagement"] == "first-party-advice" and row["role"] == "client")]
        self.assertEqual([], self.view().represented("our-firm", "carrier"))

    def test_party_role_dispute_is_not_known(self):
        client = self.data["roles"][2]
        self.data["roles"].append({**client, "state": "disputed"})
        result = self.view().party_role("underlying-defense", "hotel", "client")
        self.assertEqual("disputed", result["state"])
        self.assertNotIn("value", result)
        self.assertEqual([], self.view().represented("our-firm", "hotel"))

    def test_payer_and_instructing_party(self):
        view = self.view()
        self.value(view.party_role("underlying-defense", "carrier", "payer"), "affirmed")
        self.value(view.party_role("underlying-defense", "hotel", "instructing-party"), "affirmed")
        self.assertEqual("unknown", view.party_role("underlying-defense", "carrier", "instructing-party")["state"])

    def test_counsel_handoff_is_closed_open(self):
        self.assertEqual(["underlying-defense"], self.view("2026-07-19").represented("our-firm", "hotel"))
        self.assertEqual([], self.view("2026-07-20").represented("our-firm", "hotel"))
        self.assertEqual(["underlying-defense"], self.view("2026-07-20").represented("successor", "hotel"))

    def test_distinct_trial_appellate_and_coverage_roles(self):
        view = self.view()
        self.value(view.litigation_role("underlying-defense", "tort-trial", "hotel"), "defendant")
        self.value(view.litigation_role("underlying-defense", "tort-appeal", "hotel"), "appellant")
        self.value(view.litigation_role("underlying-defense", "tort-appeal", "estate"), "appellee")
        self.value(view.litigation_role("coverage-declaration", "coverage-trial", "carrier"), "plaintiff")
        self.assertEqual("unknown", view.litigation_role("underlying-defense", "tort-trial", "carrier")["state"])

    def test_position_replacement_does_not_overwrite_excess(self):
        self.value(self.position("2026-03-04"), "reserved")
        self.value(self.position("2026-03-05"), "denied")
        self.value(self.position("2026-03-05", excess=True), "reserved")

    def test_overlapping_positions_stay_disputed(self):
        result = self.position("2026-03-08", issue="indemnity")
        self.assertEqual({"state": "disputed", "candidates": ["denied", "reserved"],
                          "evidence": ["indemnity-denial", "indemnity-reservation"]}, result)

    def test_position_is_not_outcome(self):
        key = ("coverage-declaration", "primary-policy", "duty-to-defend", "court", "outcome")
        self.assertEqual("unknown", self.view("2026-03-20").coverage(*key)["state"])
        self.value(self.view("2026-04-05").coverage(*key), "owed")
        self.assertEqual("unknown", self.view().coverage("underlying-defense", *key[1:])["state"])
        self.assertEqual("unknown", self.view().coverage(key[0], "excess-policy", *key[2:])["state"])

    def test_evidence_cutoff_does_not_see_future_receipt(self):
        key = ("coverage-declaration", "primary-policy", "duty-to-defend", "court", "outcome")
        self.assertEqual("unknown", self.view("2026-04-07", "2026-04-04").coverage(*key)["state"])

    def test_earlier_knowledge_does_not_see_later_counsel_or_policy_changes(self):
        view = self.view("2026-07-20", "2026-07-14")
        self.assertEqual(["underlying-defense"], view.represented("our-firm", "hotel"))
        self.assertEqual([], view.represented("successor", "hotel"))
        view = self.view("2026-03-06", "2026-03-04")
        self.value(view.coverage("coverage-declaration", "primary-policy",
                                 "duty-to-defend", "carrier", "position"), "reserved")

    def test_filing_is_dated_and_scoped(self):
        engagement, forum = "first-party-advice", "state-trial-court"
        self.value(self.view("2026-02-20").filing(engagement, forum), "not-filed")
        self.assertEqual("unknown", self.view("2026-02-19").filing(engagement, forum)["state"])
        self.assertEqual("unknown", self.view("2026-02-21").filing(engagement, forum)["state"])
        self.assertEqual("unknown", self.view("2026-02-20").filing(engagement, "federal-court")["state"])
        self.assertEqual("inapplicable", self.view().filing("notice-advice", forum)["state"])

    def test_reversed_input_keeps_results(self):
        first = self.position("2026-03-08", issue="indemnity")
        self.data = {key: list(reversed(value)) if isinstance(value, list) else value
                     for key, value in self.data.items()}
        self.assertEqual(first, self.position("2026-03-08", issue="indemnity"))
        self.test_default_counsel_distinguishes_engagements()

    def test_each_mutation_is_rejected_for_its_exact_reason(self):
        changes = [
            ("roles", 3, "role", "client", "unsupported_role_evidence:roles[3]:client:invoice"),
            ("roles", 4, "evidence", "defense-invoice",
             "unsupported_role_evidence:roles[4]:instructing-party:invoice"),
            ("roles", 7, "proceeding", "coverage-trial", "role_proceeding_mismatch:roles[7]"),
            ("roles", 9, "role", "defendant", "role_stage_mismatch:roles[9]:defendant"),
            ("roles", 2, "evidence", "missing", "dangling_reference:roles[2]:evidence:missing"),
            ("coverage", 3, "evidence", "primary-denial", "unsupported_coverage_evidence:coverage[3]:carrier-notice"),
            ("coverage", 2, "actor", "carrier", "position_actor_mismatch:coverage[2]"),
            ("coverage", 0, "value", "owed", "invalid_coverage_value:coverage[0]:owed"),
            ("filing", 0, "scope", "engagement", "unsupported_filing_evidence:filing[0]:court-docket"),
            ("filing", 0, "period", {"from": "2026-02-20"}, "negative_filing_snapshot_required:filing[0]"),
            ("engagements", 0, "period", {"from": "2026-02-30"}, "schema:engagements.0.period.from:"),
        ]
        for collection, index, field, value, expected in changes:
            with self.subTest(reason=expected):
                changed = deepcopy(self.data)
                changed[collection][index][field] = value
                actual = lint(changed)
                if expected.startswith("schema:"):
                    self.assertEqual(1, len(actual), actual)
                    self.assertTrue(actual[0].startswith(expected), actual)
                else:
                    self.assertEqual([expected], actual)

    def test_duplicate_id(self):
        self.data["parties"].append(self.data["parties"][0])
        self.assertEqual(["duplicate_id:parties:our-firm"], lint(self.data))

    def test_duplicate_json_key(self):
        with TemporaryDirectory() as scratch:
            path = Path(scratch) / "bad.json"
            path.write_text('{"roles": [], "roles": []}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"duplicate JSON key: roles"):
                read_bundle(path)

    def test_link_cycle_rejected(self):
        self.data["proceedings"][0]["prior"] = "tort-appeal"
        self.assertEqual(["proceeding_cycle:tort-appeal", "proceeding_cycle:tort-trial"], lint(self.data))

    def test_cli_baseline_and_negative(self):
        command = [sys.executable, "-B", str(ROOT / "engagement.py")]
        result = subprocess.run([*command, str(EXAMPLES)], capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"valid": true', result.stdout)
        with TemporaryDirectory() as scratch:
            path = Path(scratch) / "bad.json"
            path.write_text('{"synthetic": false}', encoding="utf-8")
            result = subprocess.run([*command, str(path)], capture_output=True, text=True, check=False)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn('"valid": false', result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
