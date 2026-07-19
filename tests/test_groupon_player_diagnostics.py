from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GrouponPlayerDiagnosticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tweak = (ROOT / "DYYY.xm").read_text(encoding="utf-8")

    def test_runtime_player_layout_contains_no_groupon_diagnostic_side_effects(self) -> None:
        for forbidden in (
            "DYYYCapturePartialPlayerContextIfNeeded",
            "DYYYControllerChainDescription",
            "groupon player diagnostic",
            "groupon_player_context.txt",
            "已复制团购播放器诊断信息",
        ):
            self.assertNotIn(forbidden, self.tweak)
