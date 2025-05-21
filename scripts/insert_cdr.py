import sqlite3
import logging

DB_PATH = "cdr_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cdr_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        call_id TEXT UNIQUE,
        caller TEXT,
        callee TEXT,
        call_start TEXT,
        call_end TEXT,
        duration INTEGER,
        call_type TEXT,
        status TEXT,
        chain TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_cdr_entry(cdr: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO cdr_logs
        (call_id, caller, callee, call_start, call_end, duration, call_type, status, chain)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cdr.get("call_id"),
            cdr.get("caller"),
            cdr.get("callee"),
            cdr.get("call_start"),
            cdr.get("call_end"),
            cdr.get("duration"),
            cdr.get("call_type"),
            cdr.get("status"),
            cdr.get("chain")
        ))
        conn.commit()
    except Exception as e:
        logging.error(f"Erreur insertion base : {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
