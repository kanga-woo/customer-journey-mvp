import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "../data/events.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    event_type TEXT,
    properties TEXT,
    timestamp TEXT
    )
    """
    )
    conn.commit()
    conn.close()


def insert_event(customer_id, event_type, properties, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO events (customer_id, event_type, properties, timestamp) VALUES (?,?,?,?)",
        (customer_id, event_type, str(properties), timestamp.isoformat()),
    )
    conn.commit()
    conn.close()


def get_customer_events(customer_id, limit=500):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT event_type, properties, timestamp FROM events WHERE customer_id=? ORDER BY timestamp DESC LIMIT ?",
        (customer_id, limit),
    )
    rows = c.fetchall()
    conn.close()
    return [{"event_type": r[0], "properties": r[1], "timestamp": r[2]} for r in rows]


# Placeholder feature builder
def get_customer_features(customer_id):
    # For MVP, compute simple recency & frequency
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT timestamp FROM events WHERE customer_id=? ORDER BY timestamp DESC", (customer_id,)
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        return {"recency_days": None, "frequency_30d": 0}
    last = datetime.fromisoformat(rows[0][0])
    recency = (datetime.utcnow() - last).days
    # naive frequency in last 30 days
    freq_30d = 0
    for r in rows:
        t = datetime.fromisoformat(r[0])
        if (datetime.utcnow() - t).days <= 30:
            freq_30d += 1
    return {"recency_days": recency, "frequency_30d": freq_30d}
