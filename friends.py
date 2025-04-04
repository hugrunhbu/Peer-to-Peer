import sqlite3

DB_NAME = "messages.db"

def add_friend(owner, friend_name, ip, port):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO friends (owner, friend_name, ip, port)
            VALUES (?, ?, ?, ?)
        """, (owner, friend_name, ip, port))
        conn.commit()

def get_friends(owner):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT friend_name, ip, port
            FROM friends
            WHERE owner = ?
        """, (owner,))
        return {row[0]: {"ip": row[1], "port": row[2]} for row in cursor.fetchall()}

def is_friend(owner, friend_name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM friends WHERE owner = ? AND friend_name = ?
        """, (owner, friend_name))
        return cursor.fetchone() is not None

def get_friend_info(owner, friend_name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ip, port FROM friends WHERE owner = ? AND friend_name = ?
        """, (owner, friend_name))
        result = cursor.fetchone()
        return {"ip": result[0], "port": result[1]} if result else None
