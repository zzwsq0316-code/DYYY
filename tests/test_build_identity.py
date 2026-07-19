from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BuildIdentityTests(unittest.TestCase):
    def test_control_and_runtime_versions_match_and_identify_safe_build(self) -> None:
        control = (ROOT / "control").read_text(encoding="utf-8")
        constants = (ROOT / "DYYYConstants.h").read_text(encoding="utf-8")

        package_version = re.search(r"^Version:\s*(\S+)$", control, re.MULTILINE)
        runtime_version = re.search(r'#define DYYY_VERSION @"([^"]+)"', constants)
        self.assertIsNotNone(package_version)
        self.assertIsNotNone(runtime_version)
        self.assertEqual(package_version.group(1), runtime_version.group(1))
        self.assertIn("396safe1", package_version.group(1))


if __name__ == "__main__":
    unittest.main()
