"""Unit tests for the independent Hangman engine."""

import unittest

from game import GameFinishedError, HangmanGame, InvalidGuessError


class HangmanGameTests(unittest.TestCase):
    def test_initial_state_is_safe(self):
        state = HangmanGame("eagle").to_state()
        self.assertEqual("_ _ _ _ _", state["pattern"])
        self.assertEqual([], state["guessed_letters"])
        self.assertEqual([], state["incorrect_letters"])
        self.assertEqual(6, state["remaining_guesses"])
        self.assertEqual("playing", state["status"])
        self.assertNotIn("word", state)

    def test_word_is_normalized(self):
        game = HangmanGame("  EAGLE  ")
        for letter in "eagl":
            state = game.guess(letter)
        self.assertEqual("won", state["status"])
        self.assertEqual("eagle", state["word"])

    def test_invalid_words_are_rejected(self):
        for word in (None, "", "two words", "word2", "café"):
            with self.subTest(word=word):
                with self.assertRaises(ValueError):
                    HangmanGame(word)

    def test_invalid_guess_limit_is_rejected(self):
        for limit in (0, -1, 1.5, "6"):
            with self.subTest(limit=limit):
                with self.assertRaises(ValueError):
                    HangmanGame("apple", limit)

    def test_correct_guess_reveals_every_repeated_letter(self):
        state = HangmanGame("eagle").guess("E")
        self.assertEqual("e _ _ _ e", state["pattern"])
        self.assertEqual(6, state["remaining_guesses"])
        self.assertEqual([], state["incorrect_letters"])

    def test_wrong_guess_consumes_exactly_one_life(self):
        state = HangmanGame("eagle").guess("z")
        self.assertEqual(5, state["remaining_guesses"])
        self.assertEqual(["z"], state["incorrect_letters"])
        self.assertEqual(["z"], state["guessed_letters"])

    def test_case_and_surrounding_spaces_are_normalized(self):
        state = HangmanGame("apple").guess(" A ")
        self.assertEqual(["a"], state["guessed_letters"])
        self.assertEqual("a _ _ _ _", state["pattern"])

    def test_invalid_guesses_are_rejected_without_mutation(self):
        game = HangmanGame("apple")
        for guess in (None, "", " ", "ab", "1", "!", "é"):
            with self.subTest(guess=guess):
                with self.assertRaises(InvalidGuessError):
                    game.guess(guess)
                self.assertEqual([], game.to_state()["guessed_letters"])

    def test_duplicate_correct_guess_is_rejected_without_mutation(self):
        game = HangmanGame("apple")
        game.guess("a")
        with self.assertRaisesRegex(InvalidGuessError, "already"):
            game.guess("A")
        self.assertEqual(["a"], game.to_state()["guessed_letters"])
        self.assertEqual(6, game.remaining_guesses)

    def test_duplicate_wrong_guess_is_rejected_without_extra_cost(self):
        game = HangmanGame("apple")
        game.guess("z")
        with self.assertRaises(InvalidGuessError):
            game.guess("z")
        self.assertEqual(5, game.remaining_guesses)
        self.assertEqual(["z"], game.incorrect_letters)

    def test_win_reveals_word(self):
        game = HangmanGame("book")
        for letter in "bok":
            state = game.guess(letter)
        self.assertEqual("won", state["status"])
        self.assertEqual("b o o k", state["pattern"])
        self.assertEqual("book", state["word"])

    def test_last_correct_guess_wins_with_no_life_cost(self):
        game = HangmanGame("a")
        state = game.guess("a")
        self.assertEqual("won", state["status"])
        self.assertEqual(6, state["remaining_guesses"])

    def test_sixth_wrong_guess_loses_and_reveals_word(self):
        game = HangmanGame("apple")
        for letter in "zqxyvk":
            state = game.guess(letter)
        self.assertEqual("lost", state["status"])
        self.assertEqual(0, state["remaining_guesses"])
        self.assertEqual("apple", state["word"])

    def test_game_stays_playing_before_sixth_wrong_guess(self):
        game = HangmanGame("apple")
        for letter in "zqxyv":
            state = game.guess(letter)
        self.assertEqual("playing", state["status"])
        self.assertEqual(1, state["remaining_guesses"])
        self.assertNotIn("word", state)

    def test_finished_win_rejects_more_guesses(self):
        game = HangmanGame("a")
        game.guess("a")
        with self.assertRaises(GameFinishedError):
            game.guess("b")

    def test_finished_loss_rejects_more_guesses(self):
        game = HangmanGame("a")
        for letter in "bcdefg":
            game.guess(letter)
        with self.assertRaises(GameFinishedError):
            game.guess("a")

    def test_returned_lists_cannot_mutate_game(self):
        game = HangmanGame("apple")
        state = game.guess("a")
        state["guessed_letters"].append("p")
        self.assertEqual(["a"], game.to_state()["guessed_letters"])

    def test_active_state_never_contains_answer_as_a_value(self):
        game = HangmanGame("eagle")
        for letter in "ez":
            state = game.guess(letter)
            self.assertNotIn("word", state)
            self.assertNotIn("eagle", state.values())


if __name__ == "__main__":
    unittest.main()
