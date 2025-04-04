import sqlite3
import os
from datetime import datetime

DB_NAME = "messages.db"

def init_db():
    if not os.path.exists(DB_NAME):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # create messages table
            cursor.execute("""
                           CREATE TABLE messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            """)
            # create friends table
            cursor.execute("""
                CREATE TABLE friends (
                    owner TEXT NOT NULL,
                    friend_name TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    PRIMARY KEY (owner, friend_name)
                )
            """)
            # create presence table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS presence (
                    username TEXT PRIMARY KEY,
                    ip TEXT NOT NULL,
                    port INTEGER NOT NULL,
                    last_seen TEXT NOT NULL
                )
            """)
            # create blocking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blocked (
                    blocker TEXT NOT NULL,
                    blocked TEXT NOT NULL,
                    PRIMARY KEY (blocker, blocked)
                )
            """)
        print("[DB] messages.db created with messages, presence, blocking, and friends table")

def save_message(sender, recipient, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender, recipient, timestamp, content) VALUES (?,?,?,?)", (sender, recipient, timestamp, content))
        conn.commit()

def get_conversation(user1, user2):
    with sqlite3.connect("messages.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender, timestamp, content
            FROM messages
            WHERE (sender=? AND recipient=?) OR (sender=? AND recipient=?)
            ORDER BY timestamp
        """, (user1, user2, user2, user1))
        return cursor.fetchall()
