import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / "termcopilot" / "history.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS diagnostics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            bundle TEXT,
            result TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            command TEXT,
            outcome TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_diagnostic(bundle, result):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO diagnostics (timestamp, bundle, result) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), json.dumps(bundle, default=str), json.dumps(result)),
    )
    conn.commit()
    conn.close()


def save_action(command, outcome):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO actions (timestamp, command, outcome) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), command, json.dumps(outcome)),
    )
    conn.commit()
    conn.close()


def get_diagnostic_history(limit=20):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM diagnostics ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_action_history(limit=20):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM actions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
