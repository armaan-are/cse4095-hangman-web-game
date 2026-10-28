"""Static structure tests for the browser presentation."""

import unittest
from html.parser import HTMLParser
from pathlib import Path


STATIC_DIRECTORY = Path(__file__).resolve().parents[1] / "static"


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.figure_parts = []
        self.letter_buttons = []
        self.live_regions = []
        self.svg_count = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        classes = set(attributes.get("class", "").split())
        if "figure-part" in classes:
            self.figure_parts.append(attributes.get("data-part"))
        if tag == "button" and "data-letter" in attributes:
            self.letter_buttons.append(attributes["data-letter"])
        if attributes.get("aria-live"):
            self.live_regions.append(attributes["aria-live"])
        if tag == "svg":
            self.svg_count += 1

    def handle_data(self, data):
        self.text.append(data)


class FrontendPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (STATIC_DIRECTORY / "index.html").read_text(encoding="utf-8")
        cls.css = (STATIC_DIRECTORY / "style.css").read_text(encoding="utf-8")
        cls.javascript = (STATIC_DIRECTORY / "app.js").read_text(encoding="utf-8")
        cls.parser = StructureParser()
        cls.parser.feed(cls.html)

    def test_required_interface_hooks_exist(self):
        required_ids = {
            "difficulty",
            "new-game",
            "game-message",
            "error-message",
            "word-pattern",
            "guessed-letters",
            "incorrect-letters",
            "attempts-text",
            "keyboard",
        }
        self.assertTrue(required_ids.issubset(self.parser.ids))

    def test_exactly_six_ordered_figure_parts_exist(self):
        self.assertEqual(["1", "2", "3", "4", "5", "6"], self.parser.figure_parts)
        self.assertEqual(1, self.parser.svg_count)

    def test_accessible_complete_alphabet_keyboard_exists(self):
        self.assertEqual(list("abcdefghijklmnopqrstuvwxyz"), self.parser.letter_buttons)
        self.assertGreaterEqual(len(self.parser.live_regions), 2)

    def test_responsive_and_focus_styles_exist(self):
        self.assertIn("@media (max-width: 850px)", self.css)
        self.assertIn("@media (max-width: 560px)", self.css)
        self.assertIn(":focus-visible", self.css)
        self.assertIn("prefers-reduced-motion", self.css)

    def test_no_answer_is_embedded_in_frontend(self):
        visible_text = " ".join(self.parser.text).lower().split()
        for word in ("apple", "eagle", "telescope"):
            self.assertNotIn(word, visible_text)

    def test_javascript_uses_required_relative_api_calls(self):
        self.assertIn('requestJson("/api/games"', self.javascript)
        self.assertIn("/api/games/${gameId}/guess", self.javascript)
        self.assertIn("fetch(url", self.javascript)

    def test_javascript_uses_safe_text_rendering(self):
        self.assertIn("textContent", self.javascript)
        self.assertNotIn("innerHTML", self.javascript)
        self.assertNotIn("document.write", self.javascript)

    def test_javascript_guards_requests_and_keyboard_input(self):
        self.assertIn("requestVersion", self.javascript)
        self.assertIn("requestPending", self.javascript)
        self.assertIn('addEventListener("keydown"', self.javascript)
        self.assertIn("currentState.status !== \"playing\"", self.javascript)


if __name__ == "__main__":
    unittest.main()
