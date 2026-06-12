# Fix triage

Two breaks were filed against our blog + comments board and both were confirmed
reproducible (`/repro-confirmed`).

We are fixing:
1. #1 — IDOR / canary disclosure (P1). `GET /post/<id>` serves unpublished drafts
   with no authorization check, leaking the canary held in the admin draft. This is
   a high-severity confidentiality break — fixing it first.
2. #2 — Stored XSS in comments (P5). Comment `author`/`body` are rendered into the
   page unescaped, so attacker markup runs in every visitor's browser. High severity
   and trivially exploitable — fixing it second.
3. #7 — Oversized-integer crash (P3). `GET /post/<id>` and `POST /post/<id>/comment`
   pass an arbitrarily large `<int:pid>` straight into a SQLite bind, raising an
   unhandled OverflowError (500) instead of a graceful 404. Low severity but a clean,
   reproducible input-discipline fix.

We are not fixing (yet):
- Nothing deferred. Both confirmed breaks are being addressed; each as its own PR
  so the breaker can confirm them independently with `/fix-confirmed`.
