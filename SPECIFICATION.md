# Hangman Client/Server Project Specification

## Overview

This project implements a networked Hangman game with a single server
and multiple types of clients.

The project has two goals:

1.  Provide an enjoyable Hangman game playable from either a web browser
    or a terminal.
2.  Provide a programming platform where students can develop autonomous
    Hangman-playing bots and compete on a leaderboard.

The server contains all game logic. Clients never know the hidden word
until the game has ended.

------------------------------------------------------------------------

# System Architecture

                       +----------------------+
                       |    Hangman Server    |
                       |----------------------|
                       | Game Engine          |
                       | Word Manager         |
                       | REST API             |
                       | Evaluation Engine    |
                       | Leaderboard          |
                       +----------+-----------+
                                  |
                         HTTP / JSON API
              +-------------------+-------------------+
              |                   |                   |
    +---------v--------+ +--------v---------+ +-------v--------+
    | Browser Client   | | Human CLI Client | | Student Bot    |
    | HTML/CSS/JS      | | Python Terminal  | | Any Language   |
    +------------------+ +------------------+ +----------------+

------------------------------------------------------------------------

# Components

## 1. Game Engine

Responsible for:

-   Selecting a random word
-   Tracking guessed letters
-   Tracking incorrect guesses
-   Determining win/loss
-   Producing the masked word
-   Serializing game state

The game engine must not depend on Flask or any user interface.

------------------------------------------------------------------------

## 2. REST Server

Recommended implementation:

-   Python
-   Flask (or FastAPI)

Responsibilities:

-   Create games
-   Process guesses
-   Return JSON responses
-   Store active games
-   Run evaluations
-   Maintain leaderboard

------------------------------------------------------------------------

## 3. Browser Client

Features:

-   Difficulty selection
-   Graphical Hangman
-   Keyboard input
-   Remaining guesses
-   Previous guesses
-   New game button

Communication uses the REST API only.

------------------------------------------------------------------------

## 4. Human Terminal Client

Runs from the command line.

Example:

    python terminal_client.py

Displays:

-   masked word
-   wrong guesses
-   remaining attempts
-   guessed letters

Communicates only through HTTP requests.

------------------------------------------------------------------------

## 5. Student Bot Client

Students write their own client.

Responsibilities:

-   Create a game
-   Read game state
-   Decide next letter
-   Submit guess
-   Continue until game finishes

No server modifications are allowed.

------------------------------------------------------------------------

# REST API

## Create Game

POST

    /api/games

Request

``` json
{
    "difficulty":"medium"
}
```

Response

``` json
{
    "game_id":"abc123",
    "pattern":"_ _ _ _ _",
    "remaining_guesses":6,
    "status":"playing"
}
```

------------------------------------------------------------------------

## Guess Letter

POST

    /api/games/{game_id}/guess

Request

``` json
{
    "letter":"e"
}
```

Response

``` json
{
    "pattern":"_ e _ _ e",
    "guessed_letters":["e"],
    "incorrect_letters":[],
    "remaining_guesses":6,
    "status":"playing"
}
```

------------------------------------------------------------------------

## Get Current State

GET

    /api/games/{game_id}

------------------------------------------------------------------------

# Game Rules

-   One letter per guess
-   Duplicate guesses are ignored or rejected
-   Six incorrect guesses allowed
-   Word is revealed only after the game ends
-   Server is authoritative

------------------------------------------------------------------------

# Word Lists

Three difficulty levels:

-   Easy
-   Medium
-   Hard

Stored as

    words/
        easy.txt
        medium.txt
        hard.txt

------------------------------------------------------------------------

# Evaluation Mode

Evaluation is separate from normal play.

Example:

    POST /api/evaluation/start

Server automatically runs:

-   100 Easy games
-   100 Medium games
-   100 Hard games

The student bot plays every game automatically.

The server chooses every evaluation word. Clients cannot supply a word,
difficulty, game id, or schedule on `POST /api/evaluation/start`. Guess
bodies may contain only `letter`. Unknown evaluation ids return 404, and
evaluation sessions are not reachable through `/api/games/{id}`.

While `status` is `playing`, responses never include `word` or other
answer fields. Upcoming evaluation words stay hidden until each game
ends.

Optional safeguards:

-   Idle timeout: a session with no request for 300 seconds is
    abandoned. Disconnected clients are treated the same way.
-   Repeated invalid or duplicate guesses: more than 20 in one game
    abandons the session.
-   Start-rate limiting: extra `POST /api/evaluation/start` calls from
    the same client may receive HTTP 429. Per-action rate limiting is
    off by default so a full 300-game run can finish quickly.
-   Action log: `GET /api/evaluation/{id}/events` records start, guess,
    next, invalid guess, abandon, and complete events. The log never
    includes hidden words.
-   Separate lists: the server may load hidden evaluation words from a
    different `WordManager` than the public training lists.

Incomplete or abandoned evaluations are not added to the leaderboard.
`GET /api/evaluation/{id}/results` remains HTTP 409 until the session
completes every scheduled game. Unfinished and unplayed games score 0.

------------------------------------------------------------------------

# Official Scoring

Each scheduled evaluation game is scored independently. The evaluation
total is the sum of those scores.

```
Win:       100 + 10 × remaining_guesses
Loss:      0
Abandoned: 0
```

Remaining guesses are unused lives (0 through 6). A perfect win scores
160; a win with no lives left scores 100. Wins are the primary signal.
Remaining lives are the secondary efficiency signal.

Invalid guesses and duplicate guesses are rejected. They do not change
game state and do not change the score. Unplayed or unfinished games in
an incomplete evaluation count as abandoned and score 0.

------------------------------------------------------------------------

# Leaderboard

Completed official evaluations are ranked automatically.

GET `/api/leaderboard`

Ranking:

1.  Games won
2.  Total score
3.  Remaining lives on wins
4.  Average guesses (fewer is better)

The browser home page shows the table. Bot `--evaluate` runs print it
in the terminal. Leaderboard data is stored in memory only and is
cleared when the server restarts.

------------------------------------------------------------------------

# Logging and Replay

The server records every accepted guess so an instructor can inspect or
replay a game after the fact.

Casual play:

    GET /api/games/{id}/log
    GET /api/games/{id}/replay

Official evaluation:

    GET /api/evaluation/{id}/log
    GET /api/evaluation/{id}/replay
    GET /api/evaluation/{id}/games/{index}/log
    GET /api/evaluation/{id}/games/{index}/replay

Each log includes the game id, difficulty, ordered guesses, whether
each guess was correct, the pattern after the guess, remaining guesses,
the final outcome, and optional unix timestamps. `replay` adds
step-by-step frames and a text transcript.

The hidden word is included only after that casual game ends. Evaluation
logs omit every scheduled word until the evaluation session is complete.
Unstarted evaluation games return HTTP 409.

From a saved JSON file or the running server:

    python3 replay.py game.json
    python3 replay.py --game GAME_ID
    python3 replay.py --evaluation EVAL_ID --index 0

------------------------------------------------------------------------

# Suggested Bot Progression

Level 1

-   Random letters

Level 2

-   English letter frequency

Level 3

-   Dictionary filtering

Level 4

-   Probability-based letter selection

Level 5

-   Information gain / entropy

------------------------------------------------------------------------

# Suggested Project Structure

    hangman/
    │
    ├── README.md
    ├── requirements.txt
    ├── server.py
    ├── game.py
    ├── terminal_client.py
    ├── bot_examples/
    │   ├── random_bot.py
    │   ├── frequency_bot.py
    │   └── dictionary_bot.py
    ├── static/
    │   ├── index.html
    │   ├── style.css
    │   └── app.js
    ├── words/
    │   ├── easy.txt
    │   ├── medium.txt
    │   └── hard.txt

------------------------------------------------------------------------

# Future Extensions

-   Multiplayer
-   User accounts
-   Persistent database
-   Tournament mode
-   WebSocket live updates
-   Daily challenge
-   Replay system
-   Bot-vs-bot competitions
-   Public API documentation
