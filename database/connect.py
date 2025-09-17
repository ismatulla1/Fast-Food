import sqlite3

def get_connect():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        username TEXT,
        chat_id INTEGER UNIQUE,
        phone TEXT,
        long REAL,
        lat REAL,
        is_admin Integer default 0
    )
    """)

   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        image TEXT,
        price REAL,
        quantity INTEGER,
        description TEXT
    )
    """)

    # Buyurtmalar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_id INTEGER,
        user_id INTEGER,
        quantity INTEGER,
        price REAL,
        status TEXT,
        create_at TEXT DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (food_id) REFERENCES food(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
  
    return conn