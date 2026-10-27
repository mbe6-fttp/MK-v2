from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "knowledge.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_notes_updated_at
        ON notes (updated_at DESC, created_at DESC)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_notes_category_updated_at
        ON notes (category_id, updated_at DESC, created_at DESC)
    """)

    connection.commit()
    connection.close()