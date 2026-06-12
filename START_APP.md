# START_APP.md — how to run and probe this app

> **Build team:** fill in every `<...>` below once your app runs. Other teams use this file to
> start your app and probe it during Break. Keep it accurate — a break is filed against the app a
> breaker can actually start from these instructions.

## What this app is

- **App:** a blog + comments board (menu #4) — read published posts and leave comments on them.
- **Stack:** Python + Flask

## Start it

```bash
# 1. Install dependencies (one-time, into a private virtual environment)
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Run it
.venv/bin/python -m flask --app app run --port 8000
```

- **Base URL:** http://localhost:8000
- **Stop it:** Ctrl-C in the terminal running it.

> Note: on first run the app creates `blog.db` (a SQLite file) and seeds it with one published
> post and one unpublished admin draft. Delete `blog.db` to start from a clean slate.

## How to interact with it

- **Main endpoints / pages:**
  - `GET /` — home page: lists **published** blog posts.
  - `GET /post/<id>` — view a single post, its comments, and a comment form.
  - `POST /post/<id>/comment` — add a comment from form fields `author` and `body`; redirects back to the post.
- **Accounts / credentials for legitimate use:** none — no login.
- **A benign request that should succeed:**

  ```bash
  curl http://localhost:8000/post/1
  ```

## For breakers

Attack this **running app over HTTP** — do **not** read this repo's source or `secret/` to find a
break. See [AGENTS_BREAK.md](AGENTS_BREAK.md) for the rules and your AI agent's instructions, and
[SPEC.md](SPEC.md) for the five properties (P1–P5) you are probing for.
