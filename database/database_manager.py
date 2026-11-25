import sqlite3

from contextlib import closing


from config.database_config import(DATABASE_PATH, DATABASE_TIMEOUT, SCHEMA_PATH)


def get_connection():

    schema = SCHEMA_PATH.read_text(encoding="utf-8")



    conn = sqlite3.connect(DATABASE_PATH, timeout=DATABASE_TIMEOUT)

    conn.execute("PRAGMA foreign_keys = ON;")

    conn.row_factory = sqlite3.Row


    return conn

def init_database():

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with closing(get_connection()) as conn:

        conn.executescript(schema)

        conn.commit()

    print("Database initialized successfully.")
