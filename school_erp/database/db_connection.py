import sqlite3

# Connect to SQLite and create table
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

# Insert a sample user (username: admin, password: 1234)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)")

conn.commit()
conn.close()

print("Database and table created successfully! User added.")
