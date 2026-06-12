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

We are not fixing (yet):
- Nothing deferred. Both confirmed breaks are being addressed; each as its own PR
  so the breaker can confirm them independently with `/fix-confirmed`.
