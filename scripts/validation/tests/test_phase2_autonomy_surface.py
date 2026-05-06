from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


NEW_PHASE2_SCHEMA_PATHS = [
    Path("schemas/innovation/opportunity-scorecard.schema.json"),
    Path("schemas/innovation/idea-object.schema.json"),
    Path("schemas/autonomy/autonomy-lane-passport.schema.json"),
    Path("schemas/autonomy/autonomy-decision-record.schema.json"),
    Path("schemas/autonomy/autonomy-reclassification-record.schema.json"),
    Path("schemas/autonomy/assumption-record.schema.json"),
    Path("schemas/autonomy/assumption-watch-record.schema.json"),
    Path("schemas/autonomy/green-restoration-packet.schema.json"),
    Path("schemas/harness/harness-plan.schema.json"),
    Path("schemas/harness/agent-review-record.schema.json"),
    Path("schemas/harness/frontier-review-record.schema.json"),
    Path("schemas/harness/codex-task-packet.schema.json"),
    Path("schemas/research/research-request-object.schema.json"),
    Path("schemas/research/research-brief-object.schema.json"),
    Path("schemas/research/incident-analogy-record.schema.json"),
]

ROOT_EXISTING_PHASE2_SURFACES = {
    "opportunity-object": Path("schemas/opportunity-object.schema.json"),
    "sprint-object": Path("schemas/sprint-object.schema.json"),
    "pilot-object": Path("schemas/pilot-object.schema.json"),
    "validation-gate-record": Path("schemas/validation-gate-record.schema.json"),
    "scale-package-object": Path("schemas/scale-package-object.schema.json"),
    "discovery-signal": Path("schemas/discovery-signal.schema.json"),
}

NEW_REGISTRY_PATHS = [
    Path("registry/innovation-object-registry.json"),
    Path("registry/autonomy-lane-registry.json"),
    Path("registry/assumption-watch-registry.json"),
    Path("registry/harness-policy-registry.json"),
    Path("registry/red-flag-trigger-registry.json"),
    Path("registry/research-signal-registry.json"),
]


def load_json(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class Phase2AutonomySurfaceTests(unittest.TestCase):
    def test_new_phase2_schemas_parse_and_are_registered(self) -> None:
        schema_registry = load_json(Path("registry/schema-registry.json"))
        registered_paths = {Path(entry["path"]) for entry in schema_registry["schemas"]}

        for rel_path in NEW_PHASE2_SCHEMA_PATHS:
            with self.subTest(path=str(rel_path)):
                schema = load_json(rel_path)
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema.get("type"), "object")
                self.assertIn(rel_path, registered_paths)

    def test_root_existing_innovation_schemas_are_not_duplicated_under_grouped_dirs(self) -> None:
        for object_type, root_path in ROOT_EXISTING_PHASE2_SURFACES.items():
            with self.subTest(object_type=object_type):
                self.assertTrue((ROOT / root_path).exists())
                for grouped_dir in ("innovation", "autonomy", "harness", "research"):
                    duplicate = ROOT / "schemas" / grouped_dir / f"{object_type}.schema.json"
                    self.assertFalse(
                        duplicate.exists(),
                        f"{duplicate.relative_to(ROOT)} duplicates existing root schema {root_path}",
                    )

    def test_phase2_registries_parse_and_reference_existing_targets(self) -> None:
        for registry_path in NEW_REGISTRY_PATHS:
            with self.subTest(registry=str(registry_path)):
                registry = load_json(registry_path)
                serialized = json.dumps(registry)
                for candidate in serialized.split('"'):
                    if candidate.startswith(("schemas/", "registry/", "governance/")):
                        self.assertTrue((ROOT / candidate).exists(), f"Missing target from {registry_path}: {candidate}")

    def test_phase2_core_law_and_human_green_authority_are_registered(self) -> None:
        lanes = load_json(Path("registry/autonomy-lane-registry.json"))
        harness = load_json(Path("registry/harness-policy-registry.json"))
        red_flags = load_json(Path("registry/red-flag-trigger-registry.json"))

        self.assertEqual(
            lanes["core_law"],
            {
                "risk_color_controls_authority": True,
                "hardness_controls_harness_depth": True,
                "leverage_controls_priority": True,
            },
        )
        self.assertTrue(all(entry["human_required_to_create_or_restore"] for entry in lanes["risk_colors"] if entry["risk_color"] == "green"))
        self.assertEqual({level["harness_level"] for level in harness["harness_levels"]}, {"H0", "H1", "H2", "H3", "H4", "H5"})
        self.assertIn("direct_canonical_mutation", red_flags["red_flag_triggers"])
        self.assertIn("new_route_id", red_flags["red_flag_triggers"])
        self.assertIn("new_event_class", red_flags["red_flag_triggers"])


if __name__ == "__main__":
    unittest.main()
