import sqlite3

from contextlib import closing


from config.database_config import(DATABASE_PATH, DATABASE_TIMEOUT, SCHEMA_PATH)


def get_connection():

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)



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


def add_memory(content,category,source="manual",source_message_id=None):
    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO memories (content, category, source, source_message_id) VALUES (?, ?, ?, ?)",
            (content, category, source, source_message_id),
        )


        conn.commit()

        return cursor.lastrowid


def get_memories():
        with closing(get_connection()) as conn:
            rows=conn.execute("SELECT * FROM memories ORDER BY created_at DESC").fetchall()

            return [dict(row) for row in rows]



def get_memory_by_id(memory_id):
    with closing(get_connection()) as conn:
        row=conn.execute("SELECT * FROM memories WHERE id=?", (memory_id,)).fetchone()

        return dict(row) if row else None



def update_memory(memory_id,content,category):
    
    with closing(get_connection()) as conn:
        cursor=conn.execute(
            "UPDATE memories SET content=?, category=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (content, category, memory_id),
        )

        if cursor.rowcount>0:
            conn.execute("DELETE FROM memory_embeddings WHERE memory_id=?", (memory_id,))
            conn.commit()
            return True
        return False



def delete_memory(memory_id):
        with closing(get_connection()) as conn:
            
            with conn:
                
                cursor=conn.execute("DELETE FROM memories WHERE id=?", (memory_id,) )

                return cursor.rowcount>0


def create_session(title=None):
     
     
     with closing(get_connection()) as conn:
         cursor=conn.execute("INSERT INTO conversation_sessions(title) VALUES (?)", (title,))

         conn.commit()

         return cursor.lastrowid


def get_sessions():

     with closing(get_connection()) as conn:
            rows=conn.execute("SELECT * FROM conversation_sessions ORDER BY started_at DESC,id DESC").fetchall()
    
            return [dict(row) for row in rows]


def update_session_title(session_id,title):
    with closing(get_connection()) as conn:
        cursor=conn.execute("UPDATE conversation_sessions SET title=? WHERE id=?", (title,session_id))

        conn.commit()

        return cursor.rowcount>0





def delete_session(session_id):

     with closing(get_connection()) as conn:
         cursor=conn.execute("DELETE FROM conversation_sessions WHERE id=?", (session_id,))

         conn.commit()

         return cursor.rowcount>0



