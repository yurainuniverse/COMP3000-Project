from contextlib import closing
from database.database_manager import get_connection
from config.database_config import DATABASE_PATH

def test_connection():

    with closing(get_connection())as conn:

        print("Connection established successfully.")


        print("Database path:", DATABASE_PATH)

        rows=conn.execute("select * from memories").fetchall()

        for row in rows:
            print(dict(row))

if __name__ == "__main__":
    test_connection()