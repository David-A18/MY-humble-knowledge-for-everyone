"""Single-partition teaching aggregator: atomic dedupe and state, explicit lateness."""
import argparse
import hashlib
import json
import sqlite3
import sys

class Aggregator:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)
        self.db.executescript("""
          CREATE TABLE IF NOT EXISTS seen(id TEXT PRIMARY KEY, fingerprint TEXT);
          CREATE TABLE IF NOT EXISTS totals(region TEXT, start INTEGER, count INTEGER, cents INTEGER, PRIMARY KEY(region,start));
          CREATE TABLE IF NOT EXISTS late(id TEXT PRIMARY KEY, payload TEXT);
          CREATE TABLE IF NOT EXISTS progress(id INTEGER PRIMARY KEY CHECK(id=1), max_ts INTEGER);
        """)

    def close(self):
        self.db.close()

    def apply(self, event):
        if (not isinstance(event, dict) or not isinstance(event.get("id"), str) or not event["id"]
            or not isinstance(event.get("region"), str) or not event["region"]
            or type(event.get("ts")) is not int or event["ts"] < 0
            or type(event.get("amount_cents")) is not int):
            raise ValueError("Invalid event schema")
        encoded = json.dumps(event, sort_keys=True, separators=(",", ":"))
        fingerprint = hashlib.sha256(encoded.encode()).hexdigest()
        start = event["ts"] // 60 * 60
        with self.db:
            old = self.db.execute("SELECT fingerprint FROM seen WHERE id=?", (event["id"],)).fetchone()
            if old:
                if old[0] != fingerprint:
                    raise ValueError("Conflicting event ID: " + event["id"])
                return "duplicate"
            row = self.db.execute("SELECT max_ts FROM progress WHERE id=1").fetchone()
            maximum = max(row[0] if row else event["ts"], event["ts"])
            watermark = maximum - 30
            self.db.execute("INSERT INTO seen VALUES(?,?)", (event["id"], fingerprint))
            self.db.execute("INSERT OR REPLACE INTO progress VALUES(1,?)", (maximum,))
            if start + 60 <= watermark:
                self.db.execute("INSERT INTO late VALUES(?,?)", (event["id"], encoded))
                return "late"
            self.db.execute("""INSERT INTO totals VALUES(?,?,1,?) ON CONFLICT(region,start)
                            DO UPDATE SET count=count+1,cents=cents+excluded.cents""",
                            (event["region"], start, event["amount_cents"]))
        return "accepted"

    def snapshot(self):
        row = self.db.execute("SELECT max_ts FROM progress WHERE id=1").fetchone()
        watermark = row[0]-30 if row else None
        totals = [{"region": r, "window_start": s, "count": n, "amount_cents": c,
                   "finalized": watermark is not None and s+60 <= watermark}
                  for r,s,n,c in self.db.execute("SELECT region,start,count,cents FROM totals ORDER BY start,region")]
        return {"watermark": watermark, "totals": totals,
                "late_count": self.db.execute("SELECT count(*) FROM late").fetchone()[0]}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True)
    args = parser.parse_args()
    state = Aggregator(args.db)
    try:
        for line in sys.stdin:
            if line.strip():
                outcome = state.apply(json.loads(line))
                print(json.dumps({"outcome": outcome, **state.snapshot()}))
    finally:
        state.close()
