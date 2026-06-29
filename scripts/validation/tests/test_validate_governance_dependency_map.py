from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_governance_dependency_map as validator  # noqa: E402


class GovernanceDependencyMapTests(unittest.TestCase):
    def test_map_shape_passes(self) -> None:
        data = validator.validate_dependency_map()
        self.assertEqual(data["map_id"], "lawfirm_os_governance_dependency_map")

    def test_changed_governance_path_requires_map_update(self) -> None:
        with self.assertRaises(validator.DependencyMapError):
            validator.validate_changed_path_gate(
                changed_files=["governance/CROSS_REPO_MAP.md"],
                map_updated=False,
            )

    def test_changed_governance_path_must_have_coverage(self) -> None:
        with self.assertRaises(validator.DependencyMapError):
            validator.validate_changed_path_gate(
                changed_files=[
                    "registry/governance-dependency-map.json",
                    "governance/UNREGISTERED_NEW_POLICY.md",
                ],
                map_updated=True,
            )

    def test_registered_governance_path_passes_when_map_updated(self) -> None:
        validator.validate_changed_path_gate(
            changed_files=[
                "registry/governance-dependency-map.json",
                "governance/CROSS_REPO_MAP.md",
            ],
            map_updated=True,
        )


if __name__ == "__main__":
    unittest.main()
