# Deployment Evidence

## Current status — 2026-10-28

**MISSING: no GitHub remote repository and no Render service exist yet.**

Local deployment readiness is verified:

- branch: `main`
- Render-readiness commit: `0eb79ce`
- clean dependency install: Flask 3.1.2 and Gunicorn 23.0.0
- automated suite: 58 tests passed
- local production smoke: one Gunicorn sync worker served `GET /` with HTTP 200 and `POST /api/games` with HTTP 201
- configuration: `render.yaml` binds `0.0.0.0:$PORT`, uses one worker, and launches `server:app`

## GitHub attempt

The GitHub CLI is not installed. The controlled browser opened `https://github.com/new` and was redirected to GitHub's sign-in page. No username, password, passkey, OAuth approval, MFA value, or other credential was entered. No repository was created, no remote was added, and no push was claimed.

Required student action: sign in to GitHub in the visible browser. After sign-in, create the student's own repository, add the verified URL as `origin`, push `main`, and independently verify the remote commit.

## Render status

Render deployment was not attempted because the required GitHub repository does not yet exist. No plan was selected, no payment method was added, and no public URL was invented.

After GitHub publication, create a Python Web Service using the repository and the values in `render.yaml`. Choose a free plan only if Render currently offers it. The real build log, service settings, public HTTPS URL, and public API/browser checks must be appended here before deployment can be called complete.
