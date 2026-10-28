# Testing Evidence

## Automated suite — 2026-10-28

Environment: macOS, system Python 3.9.6, Flask 3.1.2, Node.js syntax checker.

Commands and results:

```text
node --check static/app.js
PASS (no syntax output)

PYTHONWARNINGS=error::ResourceWarning \
PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache \
python3 -m unittest discover -s tests -v
Ran 54 tests in 0.027s — OK

PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache \
python3 -m py_compile game.py word_manager.py server.py tests/*.py
PASS (no syntax output)

git diff --check
PASS (no output)
```

Coverage includes engine rules and boundaries, word-list fixtures and all three real lists, all three REST endpoints, malformed and invalid requests, unknown IDs, concurrent game isolation, post-game refusal, new game after completion, answer secrecy, frontend structure, all 26 letter controls, six drawing parts, relative API paths, safe DOM text assignment, request guards, and frontend inability to load word files.

Clean-environment confirmation:

```text
python3 -m venv /private/tmp/hangman-reliability.yIS7xM/.venv
/private/tmp/hangman-reliability.yIS7xM/.venv/bin/python -m pip install Flask==3.1.2
PYTHONPYCACHEPREFIX=/private/tmp/hangman-reliability.yIS7xM/pycache \
/private/tmp/hangman-reliability.yIS7xM/.venv/bin/python -m unittest discover -s tests -v
Ran 54 tests in 0.082s — OK
```

The first isolated install attempt could not reach PyPI under restricted network access. The exact install was retried with scoped network permission and succeeded; the clean virtual environment then passed all 54 tests.

## Real local HTTP smoke test — 2026-10-28 15:44 EDT

Server command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache \
python3 -m flask --app server run --host 127.0.0.1 --port 5055
```

The sandbox initially denied local port binding with `Operation not permitted`. After scoped localhost permission was granted, Werkzeug served the application at `http://127.0.0.1:5055`.

Observed request and response:

```http
POST /api/games
Content-Type: application/json

{"difficulty":"easy"}
```

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{"game_id":"e4eA5t55-tAlTurazj55gIQX","guessed_letters":[],"incorrect_letters":[],"pattern":"_ _ _ _ _","remaining_guesses":6,"status":"playing"}
```

The active response did not include `word` or an answer value.

Observed GET:

```http
GET /api/games/e4eA5t55-tAlTurazj55gIQX
HTTP/1.1 200 OK

{"game_id":"e4eA5t55-tAlTurazj55gIQX","guessed_letters":[],"incorrect_letters":[],"pattern":"_ _ _ _ _","remaining_guesses":6,"status":"playing"}
```

Observed guess:

```http
POST /api/games/e4eA5t55-tAlTurazj55gIQX/guess
Content-Type: application/json

{"letter":"e"}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"game_id":"e4eA5t55-tAlTurazj55gIQX","guessed_letters":["e"],"incorrect_letters":["e"],"pattern":"_ _ _ _ _","remaining_guesses":5,"status":"playing"}
```

The guess was incorrect for this randomly selected word. The active guess response still contained no `word` field.

Negative checks:

- `POST /api/games` with `{"difficulty":"expert"}` returned HTTP 400 and `{"error":"difficulty must be easy, medium, or hard"}`.
- `GET /api/games/not-a-real-game` returned HTTP 404 and `{"error":"game not found"}`.
- The development-server log recorded the real page, static-asset, game-creation, and guess requests used in the browser walkthrough.

## Current limitations

- A clean dependency installation for the current Flask test surface passed. Requirements locking and a Gunicorn smoke test belong to the Render-readiness phase.
- Public HTTPS behavior cannot be tested until a real GitHub repository and Render service exist.
- The built-in browser does not expose Chrome DevTools Network. The local request/response above is authentic curl/server evidence, but the final demo still needs a manual Chrome DevTools Fetch/XHR capture.
