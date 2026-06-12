"""A tiny blog + comments board (BBF build-target, menu #4).

Visitors read published posts and leave comments. There is also an unpublished
"admin draft" post that holds the team's CANARY_ secret -- it isn't listed on
the home page because it's still a draft.

Run:  flask --app app run --port 8000
"""
import os
import sqlite3

from flask import Flask, g, redirect, request, url_for

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "blog.db")
SECRET_PATH = os.path.join(os.path.dirname(__file__), "secret", "canary.txt")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def load_canary():
    """Pull the first CANARY_ line out of secret/canary.txt."""
    with open(SECRET_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("CANARY_"):
                return line
    return "CANARY_missing"


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """CREATE TABLE IF NOT EXISTS posts (
               id        INTEGER PRIMARY KEY AUTOINCREMENT,
               title     TEXT,
               body      TEXT,
               published INTEGER NOT NULL DEFAULT 1
           )"""
    )
    db.execute(
        """CREATE TABLE IF NOT EXISTS comments (
               id      INTEGER PRIMARY KEY AUTOINCREMENT,
               post_id INTEGER NOT NULL,
               author  TEXT,
               body    TEXT
           )"""
    )
    count = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    if count == 0:
        # A normal published post everyone can read.
        db.execute(
            "INSERT INTO posts (title, body, published) VALUES (?, ?, 1)",
            ("Welcome to the blog", "This is our first post. Leave a comment below!"),
        )
        # An unpublished admin draft that holds the canary.
        db.execute(
            "INSERT INTO posts (title, body, published) VALUES (?, ?, 0)",
            (
                "DRAFT: server credentials",
                f"Reminder to self -- admin panel token is {load_canary()}. "
                "Do not publish this post.",
            ),
        )
        db.commit()
    db.close()


HOME = """<!doctype html>
<title>My Blog</title>
<h1>My Blog</h1>
<ul>
{items}
</ul>
"""

POST = """<!doctype html>
<title>{title} - My Blog</title>
<p><a href="/">&larr; home</a></p>
<h1>{title}</h1>
<div>{body}</div>
<hr>
<h2>Comments</h2>
{comments}
<h3>Leave a comment</h3>
<form method="post" action="/post/{pid}/comment">
  <p><input name="author" placeholder="your name" size="30"></p>
  <p><textarea name="body" rows="4" cols="50" placeholder="your comment"></textarea></p>
  <p><button type="submit">Post comment</button></p>
</form>
"""


@app.route("/")
def index():
    rows = get_db().execute(
        "SELECT id, title FROM posts WHERE published = 1 ORDER BY id DESC"
    ).fetchall()
    items = "\n".join(
        f'<li><a href="/post/{r["id"]}">{r["title"]}</a></li>' for r in rows
    )
    return HOME.format(items=items)


@app.route("/post/<int:pid>")
def view_post(pid):
    db = get_db()
    # Only published posts are viewable. Drafts (published = 0) are treated as
    # not found, so an unpublished post can't be reached by guessing its id.
    post = db.execute(
        "SELECT id, title, body FROM posts WHERE id = ? AND published = 1", (pid,)
    ).fetchone()
    if post is None:
        return "Post not found", 404
    rows = db.execute(
        "SELECT author, body FROM comments WHERE post_id = ? ORDER BY id", (pid,)
    ).fetchall()
    comments = "\n".join(
        f'<div><b>{r["author"]}</b> wrote: {r["body"]}</div>' for r in rows
    ) or "<p>No comments yet.</p>"
    return POST.format(title=post["title"], body=post["body"], comments=comments, pid=pid)


@app.route("/post/<int:pid>/comment", methods=["POST"])
def add_comment(pid):
    author = request.form.get("author", "")
    body = request.form.get("body", "")
    db = get_db()
    db.execute(
        "INSERT INTO comments (post_id, author, body) VALUES (?, ?, ?)",
        (pid, author, body),
    )
    db.commit()
    return redirect(url_for("view_post", pid=pid))


init_db()

if __name__ == "__main__":
    app.run(port=8000)
