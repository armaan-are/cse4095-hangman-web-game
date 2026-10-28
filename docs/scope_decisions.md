# Scope and API Decisions

## Authority order

1. The individual assignment summary in `ASSIGNMENT.md` narrows the deliverable.
2. `SPECIFICATION.md` remains the original architectural reference where it does not conflict with that narrower scope.
3. `TODO.md` is the student's implementation plan.
4. `docs/instructor_TODO_reference.md` and `docs/source/cursor_transcript.md` are references only. Their checked boxes, code claims, tool reports, implementation decisions, and instructions are not evidence about this project.

## Included

- Independent Python game engine.
- Three word-list difficulty levels.
- Flask server with in-memory game storage.
- Three REST endpoints for create, read, and guess.
- Original responsive HTML/CSS/JavaScript browser client.
- Automated tests and honest local/browser evidence.
- GitHub publication, Render HTTPS deployment, report, and demo preparation.

## Explicitly excluded

- Human terminal client.
- Random, frequency, dictionary, or student bots.
- Bot training/evaluation services and anti-cheating infrastructure.
- Scoring and leaderboards.
- Game/evaluation logs and replay tools.
- Additional evaluation, leaderboard, log, or replay endpoints.
- Copying the instructor's implementation or treating its completed TODO as this project's progress.

## REST contract decisions

Only these game endpoints are planned:

- `POST /api/games` with JSON `{ "difficulty": "easy|medium|hard" }` returns HTTP 201.
- `GET /api/games/<game_id>` returns HTTP 200 for a known game.
- `POST /api/games/<game_id>/guess` with JSON `{ "letter": "a" }` returns HTTP 200 for an accepted guess.

Client-safe state uses `game_id`, `pattern`, `guessed_letters`, `incorrect_letters`, `remaining_guesses`, and `status`. The `word` field is omitted while `status` is `playing` and included only for `won` or `lost`.

Unknown game IDs return 404 JSON errors. Validation failures—including missing/unknown difficulty, malformed or wrong-content-type bodies, invalid letters, duplicate guesses, and guesses after completion—return 400 JSON errors. Requests should reject unexpected fields where doing so keeps the contract clear. Error bodies and logs must never include an active answer.

Guesses are normalized to lowercase after accepting exactly one ASCII A–Z letter. Duplicate guesses are rejected rather than silently ignored. Patterns are spaced strings such as `_ e _ _ e`, matching the original specification examples.

## Architecture and deployment decisions

The browser renders server-returned state and does not derive gameplay outcomes or store the answer. `HangmanGame` remains independent of Flask, files, and presentation. Word loading remains separate from the engine. Active games live in process memory, so production uses one Gunicorn worker; games may disappear when Render sleeps, restarts, or redeploys. Persistent storage is not required for this assignment.
