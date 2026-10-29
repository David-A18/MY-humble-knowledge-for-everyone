from contextlib import closing
import sqlite3
with closing(sqlite3.connect(":memory:")) as db:
    db.execute("CREATE VIRTUAL TABLE docs USING fts5(body)")
    db.execute("INSERT INTO docs VALUES('synthetic knowledge')")
    assert db.execute("SELECT body FROM docs WHERE docs MATCH 'knowledge'").fetchone()[0] == "synthetic knowledge"
print("Python and SQLite FTS5 ready")
