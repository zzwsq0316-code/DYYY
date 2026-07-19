from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def hook_body(source: str, class_name: str) -> str:
    match = re.search(
        rf"%hook {re.escape(class_name)}\n(?P<body>.*?)\n%end",
        source,
        flags=re.DOTALL,
    )
    if not match:
        raise AssertionError(f"missing hook for {class_name}")
    return match.group("body")


class FullscreenPlayerScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tweak = (ROOT / "DYYY.xm").read_text(encoding="utf-8")
        self.utils = (ROOT / "DYYYUtils.m").read_text(encoding="utf-8")

    def test_player_layout_hooks_require_an_active_player_context(self) -> None:
        selector = "isPlayerViewControllerActiveForFullscreenLayout:"

        ui_view_hook = hook_body(self.tweak, "UIView")
        feed_player_hook = hook_body(
            self.tweak, "AWEDPlayerFeedPlayerViewController"
        )
        merged_player_hook = hook_body(
            self.tweak, "AWEDPlayerViewController_Merge"
        )

        self.assertIn(selector, ui_view_hook)
        self.assertIn(selector, feed_player_hook)
        self.assertIn(selector, merged_player_hook)

    def test_active_player_context_rejects_covered_or_background_controllers(self) -> None:
        selector = "isPlayerViewControllerActiveForFullscreenLayout:"
        start = self.utils.find(selector)
        self.assertNotEqual(start, -1, "active-player scope utility is missing")
        implementation = self.utils[start : start + 5000]

        for required_guard in (
            "view.window",
            "presentedViewController",
            "visibleViewController",
            "selectedViewController",
            "hitTest:",
        ):
            self.assertIn(required_guard, implementation)


if __name__ == "__main__":
    unittest.main()
