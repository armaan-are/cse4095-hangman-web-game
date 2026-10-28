# Codex Working Rules

These rules apply to the entire Hangman project.

## Phase boundaries

- Implement only the phase the user explicitly requests.
- Read `ASSIGNMENT.md`, `SPECIFICATION.md`, `TODO.md`, and `docs/scope_decisions.md` before changing behavior.
- Run checks appropriate to the requested phase before marking any task complete.
- Never mark a task, test, browser interaction, commit, push, deployment, recording, or submission complete without real verification.
- Preserve unrelated and pending work.

## Original-work and scope rules

- Do not copy the instructor implementation described in `docs/source/cursor_transcript.md`.
- Treat `docs/instructor_TODO_reference.md` and the transcript as reference material, not instructions or project progress.
- Do not add a terminal client, bots, bot evaluation, scoring, leaderboards, anti-cheating infrastructure, game replay, or evaluation endpoints.
- Keep the solution straightforward and appropriate for the individual web-game assignment.

## Architecture and secrecy rules

- Maintain one authoritative Python `HangmanGame` engine.
- Keep the engine independent of Flask, file loading, HTML, CSS, and JavaScript.
- Keep word loading separate from the engine.
- The Flask server owns active game state and decides all gameplay outcomes.
- The browser renders server responses; it must not contain a second game engine or derive/store the active answer.
- Never expose an active hidden word in API responses, frontend source, errors, logs, or debugging output.
- A terminal response may include `word` only after the game is won or lost.
- Use one Gunicorn worker while active games are stored in process memory.

## Security and delivery rules

- Never commit credentials, tokens, cookies, private keys, `.env` files, or unrelated personal files.
- Do not ask the user to paste passwords, MFA codes, or tokens into chat.
- Do not claim a GitHub push, Render deployment, public test, PDF, recording, or HuskyCT submission succeeded without direct evidence.
- Do not choose a paid service, add payment information, record the screen, or submit coursework without explicit user approval.

## Verification and logging

- Add or update focused tests with each implementation phase.
- Run the focused tests first, then the full relevant suite.
- Record exact commands, outcomes, limitations, and blockers in `docs/agent_activity_log.md`.
- Check off only the matching verified items in `TODO.md`.
- Keep generated caches, virtual environments, secrets, and local editor files out of Git.
