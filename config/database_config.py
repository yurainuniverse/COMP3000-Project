from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "data" / "memories.db"

SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

DATABASE_TIMEOUT=10

