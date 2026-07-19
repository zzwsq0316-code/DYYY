from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ChatLayoutABTestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tweak = (ROOT / "DYYY.xm").read_text(encoding="utf-8")
        self.utils_header = (ROOT / "DYYYUtils.h").read_text(encoding="utf-8")
        self.utils = (ROOT / "DYYYUtils.m").read_text(encoding="utf-8")

    def test_utils_exposes_safe_abtest_boolean_lookup(self) -> None:
        selector = "isABTestEnabledForKey:"
        self.assertIn(selector, self.utils_header)
        start = self.utils.find(selector)
        self.assertNotEqual(start, -1, "ABTest lookup utility is missing")
        implementation = self.utils[start : start + 2500]

        for required in (
            "AWEABTestManager",
            "sharedManager",
            "consistentABTestDic",
            "getValueOfConsistentABTestWithKey:",
            "boolValue",
        ):
            self.assertIn(required, implementation)

    def test_chat_layout_uses_media_detail_abtest_instead_of_version_only(self) -> None:
        match = re.search(
            r'if \(!useFullHeight && \[currentReferString isEqualToString:@"chat"\]\) '
            r"\{(?P<body>.*?)\n    \}",
            self.tweak,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, "chat layout branch is missing")
        body = match.group("body")

        self.assertIn('isABTestEnabledForKey:@"im_media_detail_page_opt"', body)
        self.assertIn("usesNewChatLayout", body)
        self.assertRegex(body, r"isLegacyChatLayout\s*\|\|\s*usesNewChatLayout")

    def test_private_message_layout_uses_broad_runtime_context_detection(self) -> None:
        self.assertIn("DYYYIsPrivateMessagePlaybackContext(self)", self.tweak)
        lowered = self.tweak.lower()
        for marker in (
            '@"chat"',
            '@"message"',
            '@"private"',
            '@"richcontent"',
        ):
            self.assertIn(marker, lowered)


if __name__ == "__main__":
    unittest.main()
