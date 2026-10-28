# Local Browser Verification

Date: 2026-10-28, approximately 15:44–15:46 EDT  
Browser: Codex in-app browser  
URL: `http://127.0.0.1:5055/`

## Verified observations

- The page loaded with its stylesheet and JavaScript and showed the responsive Hangman Workshop interface.
- Medium game creation returned a seven-position active pattern and enabled all A–Z controls.
- Clicking **Z** produced one incorrect guess, five remaining attempts, a disabled Z button, and one drawing stage.
- Pressing physical keyboard key **E** updated the same game to pattern `_ e _ _ _ e _` and disabled E.
- Starting a new Easy game without reloading produced a five-position pattern.
- Starting a new Hard game without reloading produced an eight-position pattern.
- A Hard game was played to loss. The UI reached `LOST`, displayed zero attempts, revealed `UMBRELLA` only after loss, showed all six figure parts, and left zero enabled letter buttons.
- After that completed game, New Game started a fresh Easy game without a page reload.
- The Easy game was played to win using public pattern feedback and the project's student-owned Easy list. Guesses `e`, `a`, `d`, `b`, `r` produced `BREAD`, status `WON`, and the terminal message “The word was ‘BREAD’.” There were no incorrect guesses.
- The server never returned an active word during the observed curl or browser-backed play.
- Responsive computed-layout checks observed two game-card columns at a 1091 px browser width and one column at 354 px. The mobile keyboard computed to seven columns.
- The desktop layout displayed side-by-side drawing and play columns; the mobile layout stacked them and retained usable controls.
- After the local server was stopped, New Game displayed `Could not start a game: Failed to fetch`. The New Game button became enabled again, confirming error recovery.

## Real request evidence tied to the walkthrough

The Flask access log recorded 200/201 requests for `/`, `/static/app.js`, `/static/style.css`, `POST /api/games`, and multiple `POST /api/games/<id>/guess` calls during the interaction. Exact request/response JSON from the same live server is recorded in `docs/testing_evidence.md`.

## Not yet verified

- Chrome DevTools Network-panel screenshot with Payload and Response panes. The in-app browser has no DevTools panel; this must be captured manually in Google Chrome for the final recording.
- Public Render URL and HTTPS playthrough. No remote service exists yet.
- Cross-browser behavior outside the in-app Chromium-based browser.
