import streamlit as st
import sqlite3
import hashlib
from pathlib import Path

class AuthHandler:
    def __init__(self):
        self.db_path = Path(__file__).parent / "users.db"
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password TEXT, email TEXT)''')
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, email):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        hashed_pw = self.hash_password(password)
        try:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", 
                     (username, hashed_pw, email))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def login_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        hashed_pw = self.hash_password(password)
        c.execute("SELECT * FROM users WHERE username=? AND password=?", 
                 (username, hashed_pw))
        result = c.fetchone()
        conn.close()
        return result is not None