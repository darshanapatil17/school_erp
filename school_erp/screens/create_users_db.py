import sqlite3
import os

def create_users_database():
    # Get the absolute path to the database
    db_path = os.path.join(os.path.dirname(__file__), "users.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT
    )
    ''')
    
    # Insert some test users
    test_users = [
        ('admin', 'admin123', 'admin', 'admin@school.com'),
        ('teacher', 'teacher123', 'teacher', 'teacher@school.com')
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO users (username, password, role, email)
    VALUES (?, ?, ?, ?)
    ''', test_users)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Users database created successfully!")

if __name__ == "__main__":
    create_users_database() 