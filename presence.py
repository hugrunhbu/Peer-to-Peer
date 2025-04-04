import sqlite3
from datetime import datetime

DB_NAME = "messages.db"

def register_active_user(username, port, ip="127.0.0.1"):
    timestamp = datetime.now().isoformat()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO presence (username, ip, port, last_seen)
            VALUES (?, ?, ?, ?)
        """, (username, ip, port, timestamp))
        conn.commit()

def load_users():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, ip, port FROM presence")
        return {row[0]: {"ip": row[1], "port": row[2]} for row in cursor.fetchall()}

def remove_active_user(username):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM presence WHERE username = ?", (username,))
        conn.commit()
