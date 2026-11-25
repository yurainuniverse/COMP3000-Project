import sqlite3

from config.database_config import(DATABASE_PATH, DATABASE_TIMEOUT)


def get_connection():

    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(f"Database file not found at {DATABASE_PATH}")



    conn = sqlite3.connect(DATABASE_PATH, timeout=DATABASE_TIMEOUT)

    conn.execute("PRAGMA foreign_keys = ON;")

    conn.row_factory = sqlite3.Row


    return conn