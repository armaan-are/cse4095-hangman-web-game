"""Flask API tests for the three required Hangman endpoints."""

import unittest
from unittest.mock import patch

import server


class HangmanApiTests(unittest.TestCase):
    def setUp(self):
        server.app.config.update(TESTING=True)
        self.client = server.app.test_client()
        server.games.clear()

    def create_game(self, difficulty="easy", word="apple"):
        with patch.object(server.word_manager, "choose_word", return_value=word):
            response = self.client.post(
                "/api/games", json={"difficulty": difficulty}
            )
        self.assertEqual(201, response.status_code)
        return response

    def test_root_serves_browser_entry_point(self):
        response = self.client.get("/")
        try:
            self.assertEqual(200, response.status_code)
            self.assertIn(b"Hangman", response.data)
        finally:
            response.close()

    def test_create_game_for_each_difficulty(self):
        for difficulty in ("easy", "medium", "hard"):
            with self.subTest(difficulty=difficulty):
                response = self.create_game(difficulty=difficulty)
                state = response.get_json()
                self.assertEqual("playing", state["status"])
                self.assertEqual("_ _ _ _ _", state["pattern"])
                self.assertEqual(6, state["remaining_guesses"])
                self.assertNotIn("word", state)

    def test_create_generates_distinct_unpredictable_ids(self):
        first_id = self.create_game().get_json()["game_id"]
        second_id = self.create_game().get_json()["game_id"]
        self.assertNotEqual(first_id, second_id)
        self.assertGreaterEqual(len(first_id), 20)

    def test_create_rejects_wrong_content_type(self):
        response = self.client.post("/api/games", data='{"difficulty":"easy"}')
        self.assertEqual(400, response.status_code)
        self.assertIn("application/json", response.get_json()["error"])

    def test_create_rejects_malformed_json(self):
        response = self.client.post(
            "/api/games", data="{", content_type="application/json"
        )
        self.assertEqual(400, response.status_code)
        self.assertIn("JSON object", response.get_json()["error"])

    def test_create_rejects_non_object_json(self):
        response = self.client.post("/api/games", json=["easy"])
        self.assertEqual(400, response.status_code)

    def test_create_rejects_missing_extra_and_invalid_difficulty(self):
        requests = ({}, {"difficulty": "easy", "extra": True}, {"difficulty": "expert"})
        for payload in requests:
            with self.subTest(payload=payload):
                response = self.client.post("/api/games", json=payload)
                self.assertEqual(400, response.status_code)
                self.assertIn("error", response.get_json())

    def test_get_returns_current_safe_state(self):
        created = self.create_game(word="eagle").get_json()
        response = self.client.get(f"/api/games/{created['game_id']}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(created, response.get_json())
        self.assertNotIn("word", response.get_json())

    def test_unknown_game_ids_return_404(self):
        for method, path in (
            (self.client.get, "/api/games/not-real"),
            (self.client.post, "/api/games/not-real/guess"),
        ):
            with self.subTest(path=path):
                response = method(path, json={"letter": "a"}) if method == self.client.post else method(path)
                self.assertEqual(404, response.status_code)
                self.assertEqual({"error": "game not found"}, response.get_json())

    def test_correct_and_wrong_guesses_update_state(self):
        game_id = self.create_game(word="eagle").get_json()["game_id"]
        correct = self.client.post(
            f"/api/games/{game_id}/guess", json={"letter": "E"}
        )
        self.assertEqual(200, correct.status_code)
        self.assertEqual("e _ _ _ e", correct.get_json()["pattern"])
        self.assertEqual(6, correct.get_json()["remaining_guesses"])

        wrong = self.client.post(
            f"/api/games/{game_id}/guess", json={"letter": "z"}
        )
        self.assertEqual(200, wrong.status_code)
        self.assertEqual(5, wrong.get_json()["remaining_guesses"])
        self.assertEqual(["z"], wrong.get_json()["incorrect_letters"])

    def test_guess_validates_body_and_letter(self):
        game_id = self.create_game().get_json()["game_id"]
        requests = (
            ({}, None),
            ({"letter": "a", "extra": True}, None),
            ({"letter": ""}, None),
            ({"letter": "ab"}, None),
            ({"letter": "1"}, None),
        )
        for payload, _ in requests:
            with self.subTest(payload=payload):
                response = self.client.post(
                    f"/api/games/{game_id}/guess", json=payload
                )
                self.assertEqual(400, response.status_code)

    def test_guess_rejects_wrong_content_type_and_malformed_json(self):
        game_id = self.create_game().get_json()["game_id"]
        wrong_type = self.client.post(
            f"/api/games/{game_id}/guess", data='{"letter":"a"}'
        )
        malformed = self.client.post(
            f"/api/games/{game_id}/guess",
            data="{",
            content_type="application/json",
        )
        self.assertEqual(400, wrong_type.status_code)
        self.assertEqual(400, malformed.status_code)

    def test_duplicate_guess_is_400_without_state_change(self):
        game_id = self.create_game().get_json()["game_id"]
        first = self.client.post(
            f"/api/games/{game_id}/guess", json={"letter": "a"}
        )
        duplicate = self.client.post(
            f"/api/games/{game_id}/guess", json={"letter": "A"}
        )
        self.assertEqual(200, first.status_code)
        self.assertEqual(400, duplicate.status_code)
        state = self.client.get(f"/api/games/{game_id}").get_json()
        self.assertEqual(["a"], state["guessed_letters"])

    def test_games_are_isolated(self):
        first_id = self.create_game(word="apple").get_json()["game_id"]
        second_id = self.create_game(word="grape").get_json()["game_id"]
        self.client.post(f"/api/games/{first_id}/guess", json={"letter": "a"})
        first = self.client.get(f"/api/games/{first_id}").get_json()
        second = self.client.get(f"/api/games/{second_id}").get_json()
        self.assertEqual(["a"], first["guessed_letters"])
        self.assertEqual([], second["guessed_letters"])

    def test_win_reveals_word_and_refuses_more_guesses(self):
        game_id = self.create_game(word="book").get_json()["game_id"]
        for letter in "bok":
            response = self.client.post(
                f"/api/games/{game_id}/guess", json={"letter": letter}
            )
        terminal = response.get_json()
        self.assertEqual("won", terminal["status"])
        self.assertEqual("book", terminal["word"])
        refused = self.client.post(
            f"/api/games/{game_id}/guess", json={"letter": "z"}
        )
        self.assertEqual(400, refused.status_code)
        retrieved = self.client.get(f"/api/games/{game_id}")
        self.assertEqual("book", retrieved.get_json()["word"])

    def test_loss_reveals_word_only_on_sixth_miss(self):
        game_id = self.create_game(word="apple").get_json()["game_id"]
        for index, letter in enumerate("zqxyvk", start=1):
            response = self.client.post(
                f"/api/games/{game_id}/guess", json={"letter": letter}
            )
            state = response.get_json()
            if index < 6:
                self.assertNotIn("word", state)
                self.assertEqual("playing", state["status"])
        self.assertEqual("lost", state["status"])
        self.assertEqual("apple", state["word"])

    def test_active_answer_is_absent_from_every_endpoint_response(self):
        created = self.create_game(word="eagle").get_json()
        game_id = created["game_id"]
        responses = [
            created,
            self.client.get(f"/api/games/{game_id}").get_json(),
            self.client.post(
                f"/api/games/{game_id}/guess", json={"letter": "e"}
            ).get_json(),
            self.client.get(f"/api/games/{game_id}").get_json(),
        ]
        for state in responses:
            self.assertEqual("playing", state["status"])
            self.assertNotIn("word", state)
            self.assertNotIn("eagle", state.values())

    def test_new_game_after_completion_has_fresh_independent_state(self):
        finished_id = self.create_game(word="a").get_json()["game_id"]
        finished = self.client.post(
            f"/api/games/{finished_id}/guess", json={"letter": "a"}
        ).get_json()
        self.assertEqual("won", finished["status"])

        fresh = self.create_game(difficulty="hard", word="telescope").get_json()
        self.assertNotEqual(finished_id, fresh["game_id"])
        self.assertEqual("playing", fresh["status"])
        self.assertEqual([], fresh["guessed_letters"])
        self.assertEqual(6, fresh["remaining_guesses"])
        self.assertNotIn("word", fresh)

        old_state = self.client.get(f"/api/games/{finished_id}").get_json()
        self.assertEqual("won", old_state["status"])
        self.assertEqual("a", old_state["word"])


if __name__ == "__main__":
    unittest.main()
