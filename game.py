"""Core Hangman rules, independent of files, Flask, and user interfaces."""


class InvalidGuessError(ValueError):
    """Raised when a guess is malformed or has already been used."""


class GameFinishedError(ValueError):
    """Raised when a guess is submitted after a game has ended."""


class HangmanGame:
    """Track one server-authoritative Hangman game."""

    def __init__(self, word, max_incorrect_guesses=6):
        normalized_word = self._normalize_word(word)
        if not isinstance(max_incorrect_guesses, int) or max_incorrect_guesses <= 0:
            raise ValueError("max_incorrect_guesses must be a positive integer")

        self.__answer = normalized_word
        self.max_incorrect_guesses = max_incorrect_guesses
        self.guessed_letters = []
        self.incorrect_letters = []
        self.status = "playing"

    @staticmethod
    def _normalize_word(word):
        if not isinstance(word, str):
            raise ValueError("word must be a string")
        normalized = word.strip().lower()
        if not normalized or not normalized.isascii() or not normalized.isalpha():
            raise ValueError("word must contain only A-Z letters")
        return normalized

    @staticmethod
    def _normalize_guess(letter):
        if not isinstance(letter, str):
            raise InvalidGuessError("guess must be exactly one A-Z letter")
        normalized = letter.strip().lower()
        if (
            len(normalized) != 1
            or not normalized.isascii()
            or not normalized.isalpha()
        ):
            raise InvalidGuessError("guess must be exactly one A-Z letter")
        return normalized

    @property
    def pattern(self):
        """Return the visible word with spaces between every position."""
        visible = [
            letter if letter in self.guessed_letters else "_"
            for letter in self.__answer
        ]
        return " ".join(visible)

    @property
    def remaining_guesses(self):
        """Return how many additional incorrect guesses are allowed."""
        return self.max_incorrect_guesses - len(self.incorrect_letters)

    def guess(self, letter):
        """Apply one new letter guess and return client-safe state."""
        if self.status != "playing":
            raise GameFinishedError("game is already finished")

        normalized = self._normalize_guess(letter)
        if normalized in self.guessed_letters:
            raise InvalidGuessError("letter has already been guessed")

        self.guessed_letters.append(normalized)
        if normalized not in self.__answer:
            self.incorrect_letters.append(normalized)

        if all(letter in self.guessed_letters for letter in self.__answer):
            self.status = "won"
        elif self.remaining_guesses == 0:
            self.status = "lost"

        return self.to_state()

    def to_state(self):
        """Return state safe to expose to a client."""
        state = {
            "pattern": self.pattern,
            "guessed_letters": list(self.guessed_letters),
            "incorrect_letters": list(self.incorrect_letters),
            "remaining_guesses": self.remaining_guesses,
            "status": self.status,
        }
        if self.status in {"won", "lost"}:
            state["word"] = self.__answer
        return state
