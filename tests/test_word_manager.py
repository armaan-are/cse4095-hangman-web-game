"""Tests for difficulty-based word loading and selection."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from word_manager import WordListError, WordManager


class WordManagerTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.words_directory = Path(self.temporary_directory.name)
        self._write("easy", " Apple \npear\napple\n\n")
        self._write("medium", "planet\nrocket\n")
        self._write("hard", "telescope\nspaceship\n")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def _write(self, difficulty, content):
        (self.words_directory / f"{difficulty}.txt").write_text(
            content, encoding="utf-8"
        )

    def test_loads_normalizes_skips_blanks_and_deduplicates(self):
        manager = WordManager(self.words_directory)
        self.assertEqual(("apple", "pear"), manager.words_for("EASY"))

    def test_choose_word_uses_requested_list(self):
        manager = WordManager(self.words_directory)
        with patch("word_manager.random.choice", return_value="rocket") as choice:
            self.assertEqual("rocket", manager.choose_word(" medium "))
        choice.assert_called_once_with(("planet", "rocket"))

    def test_invalid_difficulty_is_rejected(self):
        manager = WordManager(self.words_directory)
        for difficulty in (None, "", "expert"):
            with self.subTest(difficulty=difficulty):
                with self.assertRaisesRegex(ValueError, "easy, medium, or hard"):
                    manager.choose_word(difficulty)

    def test_missing_list_fails_clearly(self):
        (self.words_directory / "hard.txt").unlink()
        with self.assertRaisesRegex(WordListError, "missing word list"):
            WordManager(self.words_directory)

    def test_empty_list_fails_clearly(self):
        self._write("medium", "\n  \n")
        with self.assertRaisesRegex(WordListError, "word list is empty"):
            WordManager(self.words_directory)

    def test_nonalphabetic_word_fails_clearly(self):
        self._write("easy", "apple\nice-cream\n")
        with self.assertRaisesRegex(WordListError, "line 2"):
            WordManager(self.words_directory)

    def test_default_paths_do_not_depend_on_working_directory(self):
        original_directory = Path.cwd()
        try:
            os.chdir(self.temporary_directory.name)
            manager = WordManager()
        finally:
            os.chdir(original_directory)
        self.assertGreaterEqual(len(manager.words_for("easy")), 40)


class RealWordListTests(unittest.TestCase):
    def test_all_real_lists_are_valid_unique_and_large_enough(self):
        manager = WordManager()
        length_ranges = {
            "easy": (4, 7),
            "medium": (5, 9),
            "hard": (8, 12),
        }
        for difficulty, (minimum, maximum) in length_ranges.items():
            with self.subTest(difficulty=difficulty):
                words = manager.words_for(difficulty)
                self.assertGreaterEqual(len(words), 40)
                self.assertEqual(len(words), len(set(words)))
                self.assertTrue(all(word.isascii() and word.isalpha() for word in words))
                self.assertTrue(all(minimum <= len(word) <= maximum for word in words))

    def test_random_selection_belongs_to_requested_difficulty(self):
        manager = WordManager()
        for difficulty in WordManager.DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                selected = manager.choose_word(difficulty)
                self.assertIn(selected, manager.words_for(difficulty))


if __name__ == "__main__":
    unittest.main()
