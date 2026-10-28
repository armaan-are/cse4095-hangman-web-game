# CSE 4095 Web-Based Hangman

This repository is the student's original implementation of a server-authoritative Hangman game for the CSE 4095 individual assignment.

## Current status

Only project planning and the minimal repository skeleton exist. The game engine, word manager, Flask API, browser interface, tests, deployment, report, and demonstration have not been implemented yet.

The intended request path is:

```text
Browser (HTML/CSS/JavaScript)
    -> fetch() over same-origin HTTP/JSON
    -> Flask routes
    -> HangmanGame and WordManager
```

Only the server will know the active hidden word.

## Planned structure

```text
.
├── game.py
├── word_manager.py
├── server.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── words/
├── tests/
├── docs/
├── submission/
├── requirements.txt
└── TODO.md
```

## Local Python environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` is intentionally empty during the skeleton phase. Flask, Gunicorn, and test dependencies will be added and verified in their implementation phases.

To leave the environment:

```bash
deactivate
```

## Source documents

- `ASSIGNMENT.md` records the supplied assignment summary and deliverables.
- `SPECIFICATION.md` preserves the original broader specification.
- `TODO.md` is the student's unchecked phased implementation plan.
- `docs/scope_decisions.md` records which original-specification features are out of scope.
- `docs/instructor_TODO_reference.md` and `docs/source/cursor_transcript.md` are reference-only sources and do not represent this project's progress.

## Verification policy

Every phase must be implemented and tested separately. A checkbox is completed only after direct verification, and external actions such as pushes and deployments are reported separately from local work.
