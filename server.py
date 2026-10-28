"""Flask REST API for the server-authoritative Hangman game."""

import secrets

from flask import Flask, jsonify, request

from game import GameFinishedError, HangmanGame, InvalidGuessError
from word_manager import WordManager


app = Flask(__name__, static_folder="static", static_url_path="/static")
word_manager = WordManager()
games = {}


def error_response(message, status_code):
    """Return a consistent JSON error response."""
    return jsonify({"error": message}), status_code


def json_object_with_exact_fields(expected_fields):
    """Return a JSON object or an error response for a strict request body."""
    if not request.is_json:
        return None, error_response("request must use application/json", 400)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, error_response("request body must be a JSON object", 400)

    actual_fields = set(payload)
    if actual_fields != set(expected_fields):
        expected = ", ".join(sorted(expected_fields))
        return None, error_response(
            f"request body must contain exactly: {expected}", 400
        )
    return payload, None


def state_for(game_id, game):
    """Add the public game identifier to client-safe engine state."""
    return {"game_id": game_id, **game.to_state()}


def new_game_id():
    """Generate an unpredictable identifier not already in memory."""
    while True:
        game_id = secrets.token_urlsafe(18)
        if game_id not in games:
            return game_id


@app.get("/")
def index():
    """Serve the browser client entry point."""
    return app.send_static_file("index.html")


@app.post("/api/games")
def create_game():
    """Create a new game for the requested difficulty."""
    payload, error = json_object_with_exact_fields({"difficulty"})
    if error:
        return error

    try:
        word = word_manager.choose_word(payload["difficulty"])
    except ValueError as validation_error:
        return error_response(str(validation_error), 400)

    game_id = new_game_id()
    game = HangmanGame(word)
    games[game_id] = game
    return jsonify(state_for(game_id, game)), 201


@app.get("/api/games/<game_id>")
def get_game(game_id):
    """Return current client-safe state for a known game."""
    game = games.get(game_id)
    if game is None:
        return error_response("game not found", 404)
    return jsonify(state_for(game_id, game)), 200


@app.post("/api/games/<game_id>/guess")
def guess_letter(game_id):
    """Apply one guess to a known active game."""
    game = games.get(game_id)
    if game is None:
        return error_response("game not found", 404)

    payload, error = json_object_with_exact_fields({"letter"})
    if error:
        return error

    try:
        game.guess(payload["letter"])
    except (InvalidGuessError, GameFinishedError) as validation_error:
        return error_response(str(validation_error), 400)

    return jsonify(state_for(game_id, game)), 200


if __name__ == "__main__":
    app.run(debug=True)
