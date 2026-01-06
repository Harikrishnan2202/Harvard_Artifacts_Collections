import sqlite3
import os

DB_PATH = "harvard_artifacts.db"

def init_db(force=False):
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artifact_metadata (
        id INTEGER PRIMARY KEY,
        title TEXT,
        culture TEXT,
        period TEXT,
        century TEXT,
        medium TEXT,
        dimensions TEXT,
        description TEXT,
        department TEXT,
        classification TEXT,
        accessionyear INTEGER,
        accessionmethod TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artifact_media (
        objectid INTEGER,
        imagecount INTEGER,
        mediacount INTEGER,
        colorcount INTEGER,
        rank INTEGER,
        datebegin INTEGER,
        dateend INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artifact_colors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        objectid INTEGER,
        color TEXT,
        spectrum TEXT,
        hue TEXT,
        percent REAL,
        css3 TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db(force=True)
