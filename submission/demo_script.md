# Hangman Demonstration Script (Target: 2:15–2:30)

This script must be recorded against the real public Render HTTPS URL after deployment. Replace bracketed fields only with verified values.

## Preflight

- Close unrelated tabs and notifications; do not show passwords, tokens, email, grades, or personal files.
- Open the verified Render URL: `https://cse4095-hangman-web-game.onrender.com`.
- Open Chrome DevTools before starting the game: **View -> Developer -> Developer Tools -> Network -> Fetch/XHR**.
- Enable **Preserve log** if desired, clear old requests, and keep DevTools narrow enough that the game remains readable.
- Confirm the microphone input and do a short audio test.

## Timed narration and actions

### 0:00–0:20 — Introduction

“This is my CSE 4095 web-based Hangman game running at this public Render HTTPS URL. I built an independent Python game engine, a Flask REST API, and this responsive HTML, CSS, and JavaScript browser interface. The server remains authoritative and keeps an active word private.”

Show the address bar and briefly show the full interface.

### 0:20–0:45 — Difficulty and new game

“The game supports Easy, Medium, and Hard word lists. I will choose `[DIFFICULTY]` and start a new game without reloading the page.”

Select a difficulty and choose **New game**. Point out the masked pattern, six remaining attempts, empty history, and enabled A–Z keyboard.

### 0:45–1:30 — Correct and incorrect guesses

“Each guess is sent to Flask. The browser renders only the returned pattern, guessed letters, incorrect letters, remaining attempts, and status.”

Use one physical keyboard letter and one on-screen letter. Include at least one wrong guess. Point out the disabled guessed key, updated remaining-attempt count, progress bar, and newly visible SVG body part. Then make several additional guesses so the masked pattern visibly changes.

### 1:30–2:00 — End and restart

Finish the round to a win or loss.

“When the game ends, the server changes the status and only then returns the word. Guessing is now disabled. I can select New game to start a fresh independent round without refreshing the browser.”

Show the terminal message and revealed word, then select **New game** and show the reset state.

### 2:00–2:30 — Actual API request and response

In DevTools Network, select the most recent `POST /api/games/<id>/guess` Fetch/XHR request.

“This is an actual guess request. Its JSON payload contains only one letter. The response is HTTP 200 and includes the game ID, masked pattern, guessed and incorrect letters, remaining guesses, and status. While the game is active, there is no `word` field, so the browser cannot inspect the answer.”

Show **Payload** with `{"letter":"..."}`, then **Response** with the real JSON. End on the game and public URL.

## If the request is missing

DevTools only records traffic after it opens. Keep DevTools open, clear the Network list, make one new guess, and select the new Fetch/XHR row. Do not substitute fabricated JSON or a local screenshot for the real public request.

## Manual macOS recording

1. Press **Shift-Command-5**.
2. Choose **Record Selected Portion** or **Record Entire Screen**.
3. Under **Options**, select the intended microphone and a private save location.
4. Frame only the browser and DevTools, then choose **Record**.
5. Stop from the menu-bar recording control.
6. Review the entire video for readable text, audible narration, privacy, real public URL, game end/restart, and the actual Network request/response.
7. Save the final 2–3 minute file under `submission/` and record its exact filename in `SUBMISSION_CHECKLIST.md`.

No recording has been made yet because screen recording remains the student's explicit action. The public deployment is live and ready for the demonstration.
