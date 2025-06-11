import mariadb
import sys
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from config.db_config import DB_CONFIG

class DatabaseHandler:
    def __init__(self):
        try:
            self.__conn = mariadb.connect(**DB_CONFIG)
            self.__conn.autocommit = False
        except mariadb.Error as e:
            logging.error("Database connection error")
            raise

    def verify_user(self, username: str, password: str) -> bool:
        try:
            cursor = self.__conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute(
                "SELECT username FROM users WHERE username=? AND password=?",
                (username, hashed_password)
            )
            result = cursor.fetchone()
            
            if result:
                cursor.execute(
                    "UPDATE users SET last_login=? WHERE username=?",
                    (datetime.now(), username)
                )
                self.__conn.commit()
                return True
            return False
        except mariadb.Error as e:
            logging.error(f"Error verifying user: {e}")
            return False

    def create_user(self, username: str, password: str) -> bool:
        try:
            cursor = self.__conn.cursor()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            self.__conn.commit()
            return True
        except mariadb.Error:
            return False

    def __del__(self):
        try:
            if hasattr(self, '_DatabaseHandler__conn'):
                self.__conn.close()
        except:
            pass