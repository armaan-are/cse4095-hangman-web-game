# Agent Activity Log

## 2026-10-28 — Planning and source organization

### Requested phase

Review the supplied sources, preserve the original broad specification, replace the instructor's completed TODO with a new student plan, and document assignment scope decisions. No application implementation was authorized in this phase.

### Work completed

- Created a separate `hangman-web-game` workspace so prior Hangman bot/client coursework remains untouched.
- Preserved the supplied specification as `SPECIFICATION.md`.
- Preserved the supplied completed TODO as `docs/instructor_TODO_reference.md`.
- Preserved the Cursor transcript as `docs/source/cursor_transcript.md` for process reference only.
- Preserved the supplied prompt queue as `docs/source/codex_prompt_queue.md`.
- Added `ASSIGNMENT.md`, a fresh unchecked `TODO.md`, and `docs/scope_decisions.md`.
- Documented that terminal clients, bots, evaluation, scoring, leaderboards, anti-cheating, and replay features are outside this assignment's scope.
- Selected a Flask three-endpoint API contract, terminal-only answer disclosure, duplicate-guess rejection, and one-worker in-memory deployment model for later implementation.

### Verification performed

- Confirmed the preserved specification, reference TODO, transcript, and prompt queue exist in the new project directory.
- Confirmed no Python, Flask, HTML, CSS, JavaScript, word-list, test, GitHub, Render, report, or video implementation was created in this planning phase.
- No automated tests were applicable or run because there is no application code yet.

### Honest status and blockers

- This directory has not been initialized as its own Git repository; that belongs to the next phase.
- No GitHub repository, push, deployment, browser test, report PDF, recording, or HuskyCT submission has occurred.
- The full original assignment/rubric was not supplied as a separate file; `ASSIGNMENT.md` records only the concrete assignment summary and checklist present in the supplied prompt queue.

## 2026-10-28 — Project skeleton and engineering rules

### Requested phase

Create the minimal project skeleton and repository rules only. Do not implement the game engine, word loading, Flask routes, browser gameplay, or tests for later phases.

### Work completed

- Added root placeholders for `game.py`, `word_manager.py`, and `server.py`.
- Added placeholder `static/index.html`, `static/style.css`, and `static/app.js` files.
- Added tracked empty `words/`, `tests/`, and `submission/` directories.
- Added `AGENTS.md` with phase boundaries, original-work rules, answer-secrecy requirements, single-worker deployment guidance, security rules, and truthful evidence requirements.
- Added `README.md` with current status, planned architecture, structure, and `.venv` setup commands.
- Added `.gitignore` and an intentionally dependency-free `requirements.txt` placeholder.
- Added `docs/github_setup.md` with manual GitHub repository steps because authenticated GitHub tooling is unavailable.

### Verification performed

- Confirmed every requested skeleton path exists.
- Ran Python syntax compilation for the three placeholder modules using `PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache`; it passed.
- Ran `python3 -m unittest discover -s tests -v` with the same temporary cache setting. It reported `Ran 0 tests` and `OK`, which is expected because implementation tests do not belong in the skeleton phase.
- Searched project-authored files for out-of-scope implementation filenames/endpoints. Matches appeared only in documentation that explicitly excludes those features; no such implementation was added.
- Confirmed the GitHub CLI is not installed, so no GitHub repository or remote was created.

### Check issue and resolution

- The first syntax-check attempt failed before compiling because the system Python tried to write bytecode under a sandbox-protected macOS cache directory. The rerun used a task-specific cache under `/private/tmp` and passed.
- In the same first shell invocation, a loop variable named `path` shadowed zsh's special executable search-path array, making later commands unavailable in that shell. The rerun used `target_file` and completed successfully. Neither issue required a project-code change.

### Honest status and blockers

- There is no application functionality yet; the visible HTML is an implementation-pending placeholder.
- No GitHub remote or push exists. Manual setup remains pending in `docs/github_setup.md`.
- No Flask dependency has been added or installed because Flask implementation is a later phase.
- Initialized a separate local Git repository on branch `main`.
- Created the verified root commit `22f0755` (`chore: initialize Hangman project skeleton`) after the structural, syntax, source-integrity, and secret checks.

## 2026-10-28 — Independent game engine

### Work completed

- Implemented an independent `HangmanGame` with a private normalized answer, ordered guessed/incorrect letters, a configurable six-miss default, spaced patterns, remaining lives, and `playing`/`won`/`lost` states.
- Added consistent ASCII A–Z validation, lowercase normalization, duplicate rejection, and post-game lockout using explicit exceptions.
- Added client-safe serialization that returns copies of mutable lists and includes `word` only after win or loss.
- Added 18 deterministic unit tests for initialization, repeated letters, normalization, invalid words/limits/guesses, duplicates, life accounting, win/loss boundaries, lockout, defensive copies, and active-answer secrecy.

### Verification performed

- `PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache python3 -m unittest tests.test_game -v` — 18 tests passed.
- `PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache python3 -m unittest discover -s tests -v` — 18 tests passed.
- `PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache python3 -m py_compile game.py tests/test_game.py` — passed.
- `git diff --check` — passed.

### Issue and resolution

The first named-module test command failed with `ModuleNotFoundError: No module named 'tests.test_game'` even though discovery ran all 18 tests successfully. Adding `tests/__init__.py` made the focused module import explicit; both focused and discovery commands then passed.

### Scope confirmation

No Flask, word-file, browser, bot, evaluation, scoring, leaderboard, replay, or deployment behavior was added in this phase.

## 2026-10-28 — Difficulty-based word management

### Work completed

- Implemented `WordManager` with module-relative default paths, explicit easy/medium/hard validation, UTF-8 loading, lowercase normalization, blank-line skipping, order-preserving deduplication, and clear missing/empty/invalid-list errors.
- Added original curated lists: 50 easy words, 50 medium words, and 51 hard words. Every word is ASCII alphabetic, unique within its list, and within the documented difficulty length range.
- Added nine word-manager tests using temporary fixtures plus validation of all three real lists and working-directory independence.

### Verification performed

- `PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache python3 -m unittest tests.test_word_manager -v` — 9 tests passed.
- `PYTHONPYCACHEPREFIX=/private/tmp/hangman-web-game-pycache python3 -m unittest discover -s tests -v` — all 27 tests passed.
- Python compilation of the engine, word manager, and their tests — passed.
- `git diff --check` — passed.

### Scope confirmation

The game engine does not import or know about the word manager. No Flask, browser integration, or out-of-scope client/evaluation feature was added.

## 2026-10-28 — Flask server and three REST endpoints

### Work completed

- Implemented importable Flask application `server:app` with separate in-memory `HangmanGame` instances keyed by `secrets.token_urlsafe` identifiers.
- Implemented only `POST /api/games`, `GET /api/games/<game_id>`, and `POST /api/games/<game_id>/guess`, plus `/` for the static browser entry point.
- Added strict JSON-object and exact-field validation with consistent JSON errors: 201 for creation, 200 for successful reads/guesses, 400 for request/game-state validation, and 404 for unknown IDs.
- Added 17 Flask test-client tests covering all difficulties, unique IDs, malformed/wrong-content-type/missing/extra data, invalid difficulty/letters, unknown IDs, correct/wrong/duplicate guesses, isolated games, win/loss, post-game refusal, and answer secrecy across every active endpoint response.

### Verification performed

- `PYTHONWARNINGS=error::ResourceWarning ... python3 -m unittest tests.test_server -v` — 17 tests passed without warnings.
- `PYTHONWARNINGS=error::ResourceWarning ... python3 -m unittest discover -s tests -v` — all 44 tests passed without warnings.
- Python compilation of `server.py` and `tests/test_server.py` — passed.
- `git diff --check` — passed.

### Issue and resolution

The first passing test run emitted a `ResourceWarning` for the static index response. The test now closes that response explicitly, and the suite passes with resource warnings promoted to errors.

### Scope confirmation

The browser files remain presentation placeholders; no JavaScript gameplay logic, terminal client, bot, evaluation, scoring, leaderboard, or replay route was added.

## 2026-10-28 — Responsive HTML/CSS presentation

### Work completed

- Replaced the placeholder with an original responsive “Hangman Workshop” interface using semantic controls, labelled sections, polite/alert live regions, visible focus states, and reduced-motion support.
- Added difficulty selection, New Game, mystery pattern, attempts, guessed/incorrect summaries, terminal word area, and a complete disabled A–Z button grid for later JavaScript wiring.
- Added an accessible SVG scaffold with exactly six separately revealable figure parts and progress presentation.
- Added desktop, tablet, and mobile layouts without external assets or embedded game answers.
- Added five static presentation tests for required hooks, the complete alphabet, six ordered body parts, live regions, responsive/focus CSS, and absence of sample answer text in visible markup.

### Verification performed

- `python3 -m unittest tests.test_frontend_static -v` — 5 tests passed.
- Full discovery suite — all 49 tests passed.
- `git diff --check` — passed.

### Issue and resolution

The first answer-text assertion falsely matched `apple` inside CSS's standard `-apple-system` font family. The test was corrected to inspect visible HTML text rather than CSS vendor identifiers; the focused and full suites then passed.

### Limitation

This phase performed structural/static verification only. Actual rendered browser behavior and responsive visual observation remain for the dedicated local browser phase after JavaScript integration.
