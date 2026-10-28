# CSE 4095 Web-Based Hangman

An original server-authoritative Hangman game built with Python, Flask, HTML, CSS, and JavaScript for the CSE 4095 individual assignment.

The player chooses Easy, Medium, or Hard, then guesses with on-screen buttons or a physical keyboard. Six incorrect guesses end the round. The browser receives only a masked pattern while the game is active; the answer is returned only after a win or loss.

## Architecture

```text
Browser (HTML/CSS/JavaScript)
    -> same-origin fetch() over HTTP/JSON
    -> Flask routes in server.py
    -> HangmanGame + WordManager
```

- `game.py` is the only implementation of Hangman rules. It has no Flask, file, or UI dependency.
- `word_manager.py` validates and selects words from `words/easy.txt`, `medium.txt`, and `hard.txt`.
- `server.py` owns active games in memory and exposes exactly three game endpoints.
- `static/` contains the responsive browser interface. It renders server state and never loads a word list.
- `tests/` covers game rules, word loading, API behavior, secrecy, frontend structure, and deployment configuration.

## Requirements

- Python 3.9 or newer
- A modern browser

## Local setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the development server:

```bash
python -m flask --app server run --host 127.0.0.1 --port 5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000), select a difficulty, and choose **New game**.

To leave the virtual environment:

```bash
deactivate
```

## How to play

1. Select Easy, Medium, or Hard.
2. Choose **New game**.
3. Select a letter button or press an A–Z key.
4. Correct letters reveal every matching position. A wrong new letter adds one drawing part and consumes one of six attempts.
5. Win by revealing the whole word; lose after the sixth incorrect guess.
6. Choose **New game** at any time to start a fresh round without reloading the page.

## REST API

All request bodies must use `Content-Type: application/json`. Unexpected or missing fields are rejected.

### Create a game

```http
POST /api/games
Content-Type: application/json

{"difficulty":"medium"}
```

Success is HTTP 201:

```json
{
  "game_id": "unguessable-id",
  "pattern": "_ _ _ _ _ _",
  "guessed_letters": [],
  "incorrect_letters": [],
  "remaining_guesses": 6,
  "status": "playing"
}
```

### Read current state

```http
GET /api/games/<game_id>
```

A known game returns HTTP 200 with the same client-safe state shape.

### Guess a letter

```http
POST /api/games/<game_id>/guess
Content-Type: application/json

{"letter":"e"}
```

An accepted guess returns HTTP 200. Validation failures return HTTP 400, and unknown IDs return HTTP 404. The `word` field is absent while `status` is `playing`; it is present only when `status` is `won` or `lost`.

## Tests

Run the complete standard-library unittest suite:

```bash
python -m unittest discover -s tests -v
```

Check JavaScript syntax when Node.js is available:

```bash
node --check static/app.js
```

Verified commands, real local API responses, and browser observations are recorded in `docs/testing_evidence.md` and `docs/browser_verification.md`.

## Production and Render

`render.yaml` defines a Python Web Service with:

- build command: `pip install -r requirements.txt`
- start command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 server:app`
- health check: `/`

The single worker is intentional. Active games are held in one process's memory, so multiple workers would not share state.

To test the production command locally:

```bash
export PORT=8000
gunicorn --bind 0.0.0.0:$PORT --workers 1 server:app
```

## Known limitations

- Games are stored only in memory. They reset when the process restarts, redeploys, or a hosting service wakes from sleep.
- A database and persistent accounts are intentionally outside the assignment scope.
- The application has no terminal client, bots, evaluation system, scoring, leaderboard, or replay endpoints.
- A public URL is not valid evidence until the deployed HTTPS service has been independently tested.

## Project records and source credit

`SPECIFICATION.md` preserves the instructor-provided broad system specification. `ASSIGNMENT.md` and `docs/scope_decisions.md` document the narrower individual web-game deliverable. `docs/instructor_TODO_reference.md` and `docs/source/cursor_transcript.md` are reference-only sources; their checked tasks and prior implementation claims are not this project's work.

Development progress and verification are tracked truthfully in `TODO.md` and `docs/agent_activity_log.md`.
