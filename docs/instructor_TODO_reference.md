# TODO — Hangman Client/Server Project

This file is the implementation roadmap for the Hangman project.

The authoritative system requirements are defined in `Hangman_Project_Specification.md`.

## Implementation Rules

- Implement one phase at a time.
- Complete and test all items in the current phase before moving to the next phase.
- Do not change the architecture or REST API defined in `Hangman_Project_Specification.md` unless necessary.
- If a deviation is necessary, document it in the README and update the specification.
- Keep the game engine independent from Flask, the browser UI, and the terminal UI.
- The server must remain authoritative.
- Never expose the hidden word before a game ends.
- Add tests as each phase is implemented rather than postponing testing until the end.

---

## Phase 1 — Project Skeleton and Core Game Engine

### Tasks

- [x] Create the project directory structure.
- [x] Add `words/easy.txt`.
- [x] Add `words/medium.txt`.
- [x] Add `words/hard.txt`.
- [x] Create `game.py`.
- [x] Implement a `HangmanGame` class.
- [x] Store the hidden word internally.
- [x] Track guessed letters.
- [x] Track incorrect letters.
- [x] Track the maximum number of incorrect guesses.
- [x] Implement single-letter guess validation.
- [x] Detect duplicate guesses.
- [x] Implement masked-word generation.
- [x] Implement win detection.
- [x] Implement loss detection.
- [x] Implement game status values such as `playing`, `won`, and `lost`.
- [x] Implement a method that returns a client-safe game-state dictionary.
- [x] Reveal the answer only after the game ends.
- [x] Add unit tests for the game engine.

### Completion Criteria

The game engine can be tested entirely without running a web server.

All core rules are covered by unit tests.

---

## Phase 2 — Word Management

### Tasks

- [x] Create a word-loading module or helper functions.
- [x] Load Easy, Medium, and Hard word lists.
- [x] Validate that loaded words contain only alphabetic characters.
- [x] Remove accidental duplicates when loading.
- [x] Support random word selection by difficulty.
- [x] Return an error for an invalid difficulty.
- [x] Add tests for word loading and word selection.

### Completion Criteria

The program can request a random word from each difficulty level reliably.

Invalid difficulty values are rejected cleanly.

---

## Phase 3 — Basic REST Server

### Tasks

- [x] Create `server.py`.
- [x] Configure Flask or FastAPI.
- [x] Add in-memory storage for active games.
- [x] Generate unique game IDs.
- [x] Implement `POST /api/games`.
- [x] Implement `GET /api/games/{game_id}`.
- [x] Implement `POST /api/games/{game_id}/guess`.
- [x] Validate difficulty input.
- [x] Validate guess input.
- [x] Return JSON responses consistently.
- [x] Return appropriate HTTP status codes.
- [x] Handle unknown game IDs.
- [x] Handle malformed requests.
- [x] Ensure the hidden word is never leaked during an active game.
- [x] Add API tests.

### Completion Criteria

A complete Hangman game can be played using only `curl` or another HTTP client.

The browser and terminal clients are not required for this phase.

---

## Phase 4 — Human Terminal Client

### Tasks

- [x] Create `terminal_client.py`.
- [x] Connect to the Hangman server over HTTP.
- [x] Let the user choose Easy, Medium, or Hard.
- [x] Start a new game through the REST API.
- [x] Display the masked word.
- [x] Display guessed letters.
- [x] Display incorrect letters.
- [x] Display remaining incorrect guesses.
- [x] Prompt for one letter at a time.
- [x] Submit guesses through the REST API.
- [x] Handle invalid input locally when appropriate.
- [x] Handle server errors gracefully.
- [x] Display win and loss messages.
- [x] Allow the user to start another game.

### Completion Criteria

A human player can play a full game from a terminal without using the browser.

The terminal client contains no Hangman game logic beyond presentation and input handling.

---

## Phase 5 — Browser Client

### Tasks

- [x] Create `static/index.html`.
- [x] Create `static/style.css`.
- [x] Create `static/app.js`.
- [x] Add a difficulty selector.
- [x] Add a New Game button.
- [x] Display the masked word.
- [x] Display guessed letters.
- [x] Display incorrect letters.
- [x] Display remaining guesses.
- [x] Add an on-screen alphabet keyboard.
- [x] Disable already-guessed letters.
- [x] Use `fetch()` to communicate with the REST API.
- [x] Draw the Hangman state visually.
- [x] Update the drawing after incorrect guesses.
- [x] Display win and loss messages.
- [x] Provide a restart/new-game flow.
- [x] Make the interface usable on common desktop and mobile browser sizes.

### Completion Criteria

A human player can play the same server-hosted game from a browser.

No hidden word is stored in browser-side JavaScript.

---

## Phase 6 — Reference Automated Clients

### Tasks

- [x] Create `bot_examples/`.
- [x] Implement `random_bot.py`.
- [x] Implement `frequency_bot.py`.
- [x] Define a common bot interaction pattern.
- [x] Create a reusable HTTP client helper if useful.
- [x] Make each bot capable of playing a complete game automatically.
- [x] Print game results and summary statistics.
- [x] Ensure bots use only information exposed through the REST API.
- [x] Document how students can write their own bot.

### Completion Criteria

At least two automated clients can independently play games against the server.

One bot should clearly outperform random guessing over many games.

---

## Phase 7 — Dictionary-Based Bot Example

### Tasks

- [x] Implement `dictionary_bot.py`.
- [x] Load an allowed training dictionary.
- [x] Filter candidate words by current pattern.
- [x] Remove candidates containing known incorrect letters.
- [x] Respect known letter positions.
- [x] Track letters already guessed.
- [x] Compute candidate-letter frequencies.
- [x] Choose the next letter using the remaining candidates.
- [x] Fall back to global letter frequency if no candidates remain.
- [x] Compare its performance against the random and frequency bots.

### Completion Criteria

The dictionary bot completes games without server-side knowledge and demonstrates a measurable improvement over simpler reference bots.

---

## Phase 8 — Evaluation Mode

### Tasks

- [x] Separate normal game play from official evaluation mode.
- [x] Add an evaluation-session model.
- [x] Generate a unique evaluation ID.
- [x] Define the number of evaluation games.
- [x] Support evaluation across Easy, Medium, and Hard words.
- [x] Ensure the server controls all evaluation words.
- [x] Prevent skipping or restarting unfavorable evaluation games.
- [x] Require games to be played in the intended sequence.
- [x] Record wins and losses.
- [x] Record total guesses.
- [x] Record incorrect guesses.
- [x] Record remaining guesses after wins.
- [x] Record per-game results.
- [x] Add evaluation API endpoints.
- [x] Add tests for evaluation integrity.

### Completion Criteria

A bot can start an evaluation session, play every assigned game, and receive an official result summary.

A client cannot choose or inspect the hidden evaluation words.

---

## Phase 9 — Scoring System

### Tasks

- [x] Define the official scoring formula.
- [x] Make wins the primary performance signal.
- [x] Use guess efficiency as a secondary signal or tiebreaker.
- [x] Define how losses are scored.
- [x] Define how invalid guesses affect scoring.
- [x] Define how duplicate guesses affect scoring.
- [x] Define how abandoned games affect scoring.
- [x] Record total score for each evaluation.
- [x] Add tests for scoring calculations.
- [x] Document the scoring rules clearly for students.

### Completion Criteria

Given the same game history, the scoring system always produces the same result.

The scoring formula is simple enough to explain and verify independently.

---

## Phase 10 — Leaderboard

### Tasks

- [x] Define a leaderboard record format.
- [x] Store participant or bot name.
- [x] Store total games.
- [x] Store games won.
- [x] Store win rate.
- [x] Store average guesses.
- [x] Store average remaining guesses on wins.
- [x] Store total score.
- [x] Rank results consistently.
- [x] Add a leaderboard API endpoint.
- [x] Add a browser leaderboard view.
- [x] Display rankings in the terminal if useful.
- [x] Decide whether leaderboard data should persist across server restarts.

### Completion Criteria

Completed evaluation runs can be ranked automatically and displayed consistently.

---

## Phase 11 — Evaluation Integrity and Anti-Cheating Safeguards

### Tasks

- [x] Ensure game state responses never contain the answer while status is `playing`.
- [x] Ensure evaluation words are server-controlled.
- [x] Prevent clients from requesting arbitrary evaluation game IDs.
- [x] Reject malformed or unauthorized evaluation requests.
- [x] Add optional rate limiting if needed.
- [x] Add optional per-request timeout rules.
- [x] Log evaluation actions.
- [x] Detect repeated invalid guesses.
- [x] Define behavior for disconnected clients.
- [x] Define behavior for incomplete evaluations.
- [x] Keep training word lists separate from hidden evaluation lists if desired.

### Completion Criteria

A student can solve the assignment using the documented API, but cannot gain the hidden word through normal API responses.

---

## Phase 12 — Logging and Replay

### Tasks

- [x] Define a game-log format.
- [x] Record game ID.
- [x] Record difficulty.
- [x] Record each guess in order.
- [x] Record whether each guess was correct.
- [x] Record pattern after each guess.
- [x] Record remaining guesses after each move.
- [x] Record final outcome.
- [x] Add optional timestamps.
- [x] Add a replay utility or endpoint.
- [x] Ensure logs do not expose hidden evaluation words before evaluation completion.

### Completion Criteria

An instructor can inspect or replay a completed game step by step for debugging or grading.

---

## Phase 13 — Testing

### Tasks

- [x] Complete unit tests for `HangmanGame`.
- [x] Complete tests for word loading.
- [x] Complete REST API tests.
- [x] Test duplicate guesses.
- [x] Test invalid letters.
- [x] Test invalid difficulty.
- [x] Test missing game IDs.
- [x] Test win paths.
- [x] Test loss paths.
- [x] Test answer disclosure rules.
- [x] Test terminal-client integration.
- [x] Test browser-client integration.
- [x] Test automated bots.
- [x] Test evaluation sessions.
- [x] Test scoring.
- [x] Test leaderboard ordering.
- [x] Add an end-to-end automated test.

### Completion Criteria

The major user flows and failure cases are covered by automated tests.

---

## Phase 14 — Documentation and Packaging

### Tasks

- [x] Create or update `README.md`.
- [x] Document installation.
- [x] Document how to start the server.
- [x] Document how to use the browser client.
- [x] Document how to use the terminal client.
- [x] Document the REST API.
- [x] Document how to write a student bot.
- [x] Provide example requests and responses.
- [x] Document scoring.
- [x] Document evaluation rules.
- [x] Document leaderboard behavior.
- [x] Add dependency information such as `requirements.txt` or `pyproject.toml`.
- [x] Verify that a fresh installation works from the documented instructions.

### Completion Criteria

A new user can clone the project, install dependencies, start the server, play from the terminal or browser, and run a sample bot using only the documentation.

---

# Optional Future Phases

These should not be implemented until the core project is stable.

## Persistent Storage

- [ ] Store games in a database.
- [ ] Store evaluations in a database.
- [ ] Persist leaderboard results.

## Accounts and Authentication

- [ ] Student accounts.
- [ ] API keys or tokens.
- [ ] Authenticated evaluation submissions.

## Tournament Mode

- [ ] Batch evaluation of multiple bots.
- [ ] Scheduled tournaments.
- [ ] Tournament history.
- [ ] Public results page.

## Advanced Bot Analysis

- [ ] Entropy-based guessing.
- [ ] Information-gain strategies.
- [ ] Performance charts.
- [ ] Per-difficulty statistics.
- [ ] Head-to-head bot comparisons.

## Multiplayer

- [ ] Human-vs-human modes.
- [ ] Custom words.
- [ ] Spectator mode.

---

# Recommended Development Order

Use this order unless there is a compelling reason to change it:

1. Core Game Engine
2. Word Management
3. REST Server
4. Human Terminal Client
5. Browser Client
6. Reference Automated Clients
7. Dictionary-Based Bot
8. Evaluation Mode
9. Scoring
10. Leaderboard
11. Evaluation Integrity
12. Logging and Replay
13. Full Testing
14. Documentation and Packaging

The project should remain runnable after every completed phase.
