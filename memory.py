import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/jarvis.db")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT,
            tool_name TEXT,
            tool_calls TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_message(role, content=None, tool_name=None, tool_calls=None):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO messages (role, content, tool_name, tool_calls) VALUES (?, ?, ?, ?)",
        (role, content, tool_name, json.dumps(tool_calls) if tool_calls else None),
    )
    conn.commit()
    conn.close()


def load_recent(limit=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT role, content, tool_name, tool_calls FROM messages ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    rows.reverse()
    messages = []
    for role, content, tool_name, tool_calls in rows:
        msg = {'role': role, 'content': content or ''}
        if tool_name:
            msg['tool_name'] = tool_name
        if tool_calls:
            msg['tool_calls'] = json.loads(tool_calls)
        messages.append(msg)
    return messages


def clear_history():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()