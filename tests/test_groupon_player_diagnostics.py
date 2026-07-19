from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GrouponPlayerDiagnosticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tweak = (ROOT / "DYYY.xm").read_text(encoding="utf-8")

    def test_partial_player_diagnostic_captures_runtime_controller_context(self) -> None:
        for required in (
            "DYYYCapturePartialPlayerContextIfNeeded",
            "convertRect:contentView.bounds toView:window",
            "UIPasteboard generalPasteboard",
            "playerChain=",
            "activeChain=",
        ):
            self.assertIn(required, self.tweak)

    def test_both_39_6_player_controllers_report_partial_layouts(self) -> None:
        self.assertGreaterEqual(
            self.tweak.count("DYYYCapturePartialPlayerContextIfNeeded(self, contentView)"),
            2,
        )

    def test_diagnostic_never_walks_the_complete_controller_tree_on_main_thread(self) -> None:
        self.assertNotIn("DYYYAppendControllerHierarchy", self.tweak)
        self.assertNotIn("controllerTree:", self.tweak)
        self.assertIn("depth < 16", self.tweak)
        self.assertIn("dispatch_async(dispatch_get_global_queue", self.tweak)
