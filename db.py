<<<<<<< HEAD
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't already exist and apply safe migrations."""
    conn = get_db_connection()
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.commit()

    cursor = conn.cursor()

    # Migration for users table: wallet_balance, is_pro, subscription_expiry
    user_cols = [c[1] for c in cursor.execute("PRAGMA table_info('users')").fetchall()]
    if 'wallet_balance' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN wallet_balance REAL DEFAULT 0.00")
    if 'is_pro' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN is_pro INTEGER DEFAULT 0")
    if 'subscription_expiry' not in user_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN subscription_expiry DATETIME")

    # Migration for mcp table: created_at
    mcp_cols = [c[1] for c in cursor.execute("PRAGMA table_info('mcp')").fetchall()]
    if 'created_at' not in mcp_cols:
        cursor.execute("ALTER TABLE mcp ADD COLUMN created_at DATETIME")
        cursor.execute("UPDATE mcp SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print(f"Database initialised at: {DB_PATH}")
=======
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
>>>>>>> 70348e341f47bba4657b70688d9be21d0fa5d075
