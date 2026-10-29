# Deployment Evidence

## Current status — 2026-10-29

**VERIFIED: GitHub publication and the free Render deployment are live.**

- GitHub repository: https://github.com/armaan-are/cse4095-hangman-web-game
- Render application: https://cse4095-hangman-web-game.onrender.com
- deployed branch: `main`
- deployed source commit: `57ed38e1d0e0606442c5e8e04e60863a654eccb7`
- Render service ID: `srv-dbhmp4psrm7s73888k8g`
- compute: Free, $0/month, 0.1 CPU, 512 MB RAM
- build: `pip install -r requirements.txt`
- start: `gunicorn --bind 0.0.0.0:$PORT --workers 1 server:app`

## GitHub publication

The repository was created under the student's `armaan-are` account as a public repository. The local `main` branch was pushed to `origin`, and `git ls-remote --heads origin main` returned the same full SHA as local `HEAD`: `57ed38e1d0e0606442c5e8e04e60863a654eccb7`.

## Render build and launch

Render cloned the verified repository, checked out commit `57ed38e`, installed Flask 3.1.2 and Gunicorn 23.0.0, and reported `Build successful`. The runtime log showed the exact one-worker start command, Gunicorn listening on port 10000, a successful health request, `Your service is live`, and the primary HTTPS URL. The first deploy completed in 49.8 seconds at 11:56 AM EDT. No paid plan or payment method was selected.

## Public browser and API verification

The public page loaded over HTTPS with the responsive Hangman interface. A Medium game started without reloading, displayed a seven-letter masked pattern, accepted an `A` guess, reduced the remaining attempts from six to five when the guess was wrong, updated the SVG drawing, listed `A` as tried/incorrect, and disabled the duplicate `A` control.

Independent HTTPS checks produced these real outcomes:

- `POST /api/games` -> HTTP 201 with a new unpredictable game ID and no `word` field.
- `GET /api/games/<game_id>` -> HTTP 200 with the same active masked state and no `word` field.
- `POST /api/games/<game_id>/guess` with `e` -> HTTP 200, updated `_ e _ e _ _`, and still omitted `word`.
- Invalid guess `ee` -> HTTP 400 with `guess must be exactly one A-Z letter`.
- Unknown game ID -> HTTP 404 with `game not found`.
- Sequential guesses completed that game as a real loss: `remaining_guesses` became 0, `status` became `lost`, and only then did the response include `word: desert`.

The free instance may spin down after inactivity and take roughly 50 seconds or more to wake. Games are in memory and can reset after sleep, restart, or redeploy; this matches the documented one-worker architecture.
