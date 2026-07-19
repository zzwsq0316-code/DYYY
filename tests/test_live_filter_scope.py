from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LiveFilterScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tweak = (ROOT / "DYYY.xm").read_text(encoding="utf-8")
        self.utils_header = (ROOT / "DYYYUtils.h").read_text(encoding="utf-8")
        self.utils = (ROOT / "DYYYUtils.m").read_text(encoding="utf-8")

    def test_live_model_detection_uses_multiple_stable_signals(self) -> None:
        selector = "isLiveAwemeModel:"
        self.assertIn(selector, self.utils_header)
        start = self.utils.find(selector)
        self.assertNotEqual(start, -1, "live-model utility is missing")
        implementation = self.utils[start : start + 2200]

        for required in ("isLive", "cellRoom", "videoFeedTag", '@"直播中"'):
            self.assertIn(required, implementation)

    def test_recommendation_transfer_preserves_live_when_both_switches_are_off(self) -> None:
        match = re.search(
            r"transferAwemeListIfNeededWithArray:.*?\n\}",
            self.tweak,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, "recommendation transfer hook is missing")
        implementation = match.group(0)

        self.assertIn('DYYYGetBool(@"DYYYSkipLive")', implementation)
        self.assertIn('DYYYGetBool(@"DYYYSkipAllLive")', implementation)
        self.assertIn("shouldPreserveLive", implementation)
        self.assertGreaterEqual(implementation.count("shouldPreserveLive"), 3)
        self.assertIn("isLiveAwemeModel:", implementation)

    def test_model_construction_does_not_apply_generic_filters_to_preserved_live(self) -> None:
        hook_start = self.tweak.find("%hook AWEAwemeModel")
        self.assertNotEqual(hook_start, -1, "AWEAwemeModel hook is missing")
        model_hook = self.tweak[hook_start : hook_start + 11000]

        self.assertIn("shouldPreserveLive", model_hook)
        self.assertIn("isLiveAwemeModel:", model_hook)
        self.assertIsNotNone(
            re.search(
                r"if \(!shouldPreserveLive\) \{.*?\[self contentFilter\].*?\}",
                model_hook,
                flags=re.DOTALL,
            )
        )

    def test_content_filter_returns_no_for_live_when_both_switches_are_off(self) -> None:
        start = self.tweak.find("- (BOOL)contentFilter")
        self.assertNotEqual(start, -1, "contentFilter is missing")
        implementation = self.tweak[start : start + 1800]

        self.assertIn('DYYYGetBool(@"DYYYSkipLive")', implementation)
        self.assertIn('DYYYGetBool(@"DYYYSkipAllLive")', implementation)
        self.assertIsNotNone(
            re.search(
                r"shouldPreserveLive.*?return NO;",
                implementation,
                flags=re.DOTALL,
            )
        )


if __name__ == "__main__":
    unittest.main()
