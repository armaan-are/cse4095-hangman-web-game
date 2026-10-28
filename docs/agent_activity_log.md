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
