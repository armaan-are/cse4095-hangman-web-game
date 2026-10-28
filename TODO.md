# TODO — CSE 4095 Web-Based Hangman Game

This is the student's fresh implementation plan. All implementation tasks begin unchecked. `SPECIFICATION.md` remains the original broad reference, while `ASSIGNMENT.md` and `docs/scope_decisions.md` define the narrower assignment scope.

## Working rules

- Complete one phase at a time and verify it before checking any item.
- Keep one authoritative Python game engine; Flask and the browser must not reimplement game rules.
- Never expose an active game's answer in JSON, JavaScript, HTML, logs, or errors.
- Use truthful test, browser, Git, deployment, and submission evidence.
- Do not copy code from `docs/source/cursor_transcript.md`.
- Keep deployment to one Gunicorn worker while games are stored in memory.

## Phase 1 — Project skeleton and engineering rules

- [x] Create the planned root directories and placeholder files without implementing later phases.
- [x] Add `AGENTS.md` with scope, secrecy, verification, logging, and phase-boundary rules.
- [x] Add a minimal `README.md` with Python virtual-environment setup instructions.
- [x] Add `.gitignore` for `.venv`, caches, secrets, editor files, and generated artifacts.
- [x] Add minimal dependency/configuration placeholders appropriate for later Flask work.
- [x] Confirm the source references and planning documents are present.
- [x] Inspect Git state and initialize the project repository if needed.
- [x] Record actual checks and blockers in `docs/agent_activity_log.md`.
- [x] Create a local commit only after the phase checks pass.

Acceptance: the repository has the agreed structure and guardrails, contains no implemented game/API/UI logic, documents a reproducible `.venv` setup, and has an honest local Git checkpoint. GitHub creation remains pending unless authenticated creation is genuinely available and verified.

## Phase 2 — Independent Python game engine

- [x] Implement `HangmanGame` in `game.py`, independent of Flask, files, and UI.
- [x] Track a private answer, guessed letters, incorrect letters, and six allowed incorrect guesses.
- [x] Validate exactly one A–Z letter, normalize case, and reject duplicates consistently.
- [x] Generate the spaced masked pattern and playing/won/lost states.
- [x] Lock guessing after completion.
- [x] Serialize client-safe state and reveal `word` only after win or loss.
- [x] Test initial state, repeated letters, validation, duplicates, correct/wrong guesses, win/loss boundaries, lockout, and active-answer secrecy.
- [x] Run the focused test suite, log the exact result, and commit verified work.

Acceptance: the complete game can be exercised deterministically through Python tests without Flask, word files, or a browser, and every active serialized state omits the answer.

## Phase 3 — Difficulty-based word management

- [x] Implement `word_manager.py` without coupling it to the game engine.
- [x] Add original `words/easy.txt`, `words/medium.txt`, and `words/hard.txt` lists with at least 40 valid words each if no student-owned originals exist.
- [x] Normalize case, ignore blanks, reject nonalphabetic entries, and deduplicate.
- [x] Validate difficulty and select only from its corresponding list.
- [x] Resolve paths independently of the process working directory.
- [x] Test temporary fixtures, failures, selection, and all real lists.
- [x] Run the full suite, record evidence, and commit verified work.

Acceptance: every supported difficulty returns only valid words from its own nonempty list, invalid/missing data fails clearly, and all engine and word-manager tests pass.

## Phase 4 — Flask server and three REST endpoints

- [ ] Create importable Flask app `server:app` and in-memory game storage keyed by unpredictable IDs.
- [ ] Implement `POST /api/games`.
- [ ] Implement `GET /api/games/<game_id>`.
- [ ] Implement `POST /api/games/<game_id>/guess`.
- [ ] Return the agreed JSON state shape and status codes.
- [ ] Validate content type, malformed/missing/unexpected data, difficulty, letters, duplicates, finished games, and unknown IDs.
- [ ] Serve the browser entry point and static assets without adding browser game logic yet.
- [ ] Test all difficulties, isolation, validation, status codes, win/loss, and secrecy in every active response.
- [ ] Run the full suite, record evidence, and commit verified work.

Acceptance: a game can be played to completion through only the three REST endpoints, simultaneous games remain independent, and the answer appears only after a terminal state.

## Phase 5 — Responsive HTML/CSS presentation

- [ ] Build original semantic HTML and responsive CSS.
- [ ] Add difficulty, New Game, masked word, remaining guesses, guessed letters, A–Z controls, status/error regions, and win/loss presentation.
- [ ] Add an SVG scaffold and six separately revealable figure parts.
- [ ] Add keyboard/focus accessibility and mobile layout.
- [ ] Keep gameplay and active answers out of the frontend.
- [ ] Perform available static/render checks, log limitations, and commit verified work.

Acceptance: the static page presents all required states accessibly on common widths, contains exactly six drawable body stages, and does not implement or embed game answers.

## Phase 6 — Browser JavaScript integration

- [ ] Use relative same-origin `fetch()` calls to the three REST endpoints.
- [ ] Render only server-returned game state.
- [ ] Support button and physical A–Z keyboard guesses.
- [ ] Disable duplicates and all guesses after completion.
- [ ] Prevent double submissions and stale responses.
- [ ] Handle network/server errors and restore usable controls.
- [ ] Start a different difficulty/new game without reloading.
- [ ] Use safe text assignment for response data.
- [ ] Run the full suite and any supported frontend smoke checks, log evidence, and commit.

Acceptance: a human can complete and restart a game in the browser while all state decisions remain server-authoritative and stale or failed requests do not corrupt the UI.

## Phase 7 — Reliability and local verification

- [ ] Expand deterministic engine, word-manager, API, and secrecy coverage.
- [ ] Check that active words do not appear in frontend sources.
- [ ] Run all tests from a clean environment plus syntax/lint checks that are already reasonably available.
- [ ] Run a temporary local HTTP smoke test.
- [ ] Perform an actual browser walkthrough for all difficulties, drawing stages, keyboard/buttons, completion, restart, responsive layout, and an error case.
- [ ] Capture a real guess request/response and active-answer secrecy evidence.
- [ ] Write `docs/testing_evidence.md` and `docs/browser_verification.md`.
- [ ] Record exact outcomes and commit verified work.

Acceptance: automated and observed local evidence covers the rubric-critical flows; any manual-only item stays explicitly unchecked.

## Phase 8 — README and Render readiness

- [ ] Document architecture, setup, play, API examples, tests, and limitations.
- [ ] Lock only necessary Flask, Gunicorn, and testing dependencies.
- [ ] Add Render configuration with one worker and `$PORT` binding.
- [ ] Document that in-memory games reset on restart/sleep.
- [ ] Scan tracked content for secrets and unintended instructor code.
- [ ] Perform clean-install and local Gunicorn smoke tests where supported.
- [ ] Record exact results and commit verified work.

Acceptance: a clean checkout can be installed, tested, and started with the documented commands, and production configuration matches the in-memory architecture.

## Phase 9 — GitHub publication and Render deployment

- [ ] Audit the final tracked files, history, branch, and secret scan.
- [ ] Create/use the student's own GitHub repository and verify the real remote.
- [ ] Push the checked branch and verify the remote commit and accessible URL.
- [ ] Create a Render Python Web Service only with explicit approval for any consequential UI choice.
- [ ] Verify build/start settings and inspect real deployment logs.
- [ ] Record the real public HTTPS URL only after it responds.
- [ ] Test the deployed UI and all three endpoints, including bad input and secrecy.
- [ ] Write `docs/deployment_evidence.md` with dated, real evidence.

Acceptance: the student's repository and Render service are independently reachable, synchronized to the verified commit, and pass a public end-to-end playthrough and API checks.

## Phase 10 — Report, demo, and final audit

- [ ] Create an editable first-person report source using only verified project evidence.
- [ ] Quote 2–3 representative prompts actually used.
- [ ] Generate and visually verify a legible 1–2 page PDF.
- [ ] Create a truthful, timed 2–3 minute demo script.
- [ ] Record/review the real public demo only with explicit approval, or clearly leave recording as a student action.
- [ ] Create `submission/SUBMISSION_CHECKLIST.md` with VERIFIED, MISSING, and NEEDS MY ACTION states.
- [ ] Recheck URLs, source completeness, tests, PDF pages, video playback, and secrets.
- [ ] Identify the exact HuskyCT text and two upload files without submitting them.

Acceptance: every rubric item is backed by real evidence, incomplete student actions remain visible, and nothing has been submitted or purchased without explicit approval.

## Manual actions that may require the student

- [ ] Authorize or create the student's own GitHub repository if local authentication cannot do so safely.
- [ ] Authorize GitHub access in Render and choose the intended repository.
- [ ] Approve the Render service configuration; do not choose a paid plan or add payment details.
- [ ] Interact with login, CAPTCHA, MFA, or consent screens when required.
- [ ] Record and review the real 2–3 minute screen demonstration.
- [ ] Upload the report PDF and video and paste the verified URLs into HuskyCT.
- [ ] Submit through HuskyCT before the deadline.

## Final submission checklist

- [ ] Own GitHub repository URL is accessible to the grader.
- [ ] Own Render HTTPS application URL is live.
- [ ] 1–2 page PDF report contains 2–3 real prompts.
- [ ] Approximately 2–3 minute recording shows game start, guesses, end, restart, and a real API request/JSON response.
- [ ] GitHub includes the original specification, revised TODO, README, source, tests, word files, and deployment configuration.
- [ ] Public service is intended to remain available during grading.
- [ ] HuskyCT submission is completed before October 29, 2026 at 11:59 PM Eastern.
