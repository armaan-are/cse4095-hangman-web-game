"""Load, validate, and select words by difficulty."""

import random
from pathlib import Path


class WordListError(ValueError):
    """Raised when a configured word list cannot be used."""


class WordManager:
    """Own validated word lists without coupling them to the game engine."""

    DIFFICULTIES = ("easy", "medium", "hard")

    def __init__(self, words_directory=None):
        if words_directory is None:
            words_directory = Path(__file__).resolve().parent / "words"
        self.words_directory = Path(words_directory)
        self._words = {
            difficulty: self._load_words(difficulty)
            for difficulty in self.DIFFICULTIES
        }

    def _load_words(self, difficulty):
        path = self.words_directory / f"{difficulty}.txt"
        if not path.is_file():
            raise WordListError(f"missing word list: {path}")

        words = []
        seen = set()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            raise WordListError(f"could not read word list: {path}") from error

        for line_number, line in enumerate(lines, start=1):
            word = line.strip().lower()
            if not word:
                continue
            if not word.isascii() or not word.isalpha():
                raise WordListError(
                    f"invalid word in {path.name} at line {line_number}"
                )
            if word not in seen:
                seen.add(word)
                words.append(word)

        if not words:
            raise WordListError(f"word list is empty: {path}")
        return tuple(words)

    def words_for(self, difficulty):
        """Return the immutable validated words for one difficulty."""
        normalized = self._normalize_difficulty(difficulty)
        return self._words[normalized]

    def choose_word(self, difficulty):
        """Choose one random word from exactly the requested difficulty."""
        return random.choice(self.words_for(difficulty))

    def _normalize_difficulty(self, difficulty):
        if not isinstance(difficulty, str):
            raise ValueError("difficulty must be easy, medium, or hard")
        normalized = difficulty.strip().lower()
        if normalized not in self.DIFFICULTIES:
            raise ValueError("difficulty must be easy, medium, or hard")
        return normalized
