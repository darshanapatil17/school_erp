import sqlite3

def create_database():
    """✅ Create the school management database and tables if they don't exist."""
    conn = sqlite3.connect("school_management.db")
    cursor = conn.cursor()

    # Example: Creating a 'users' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database setup completed!")

# ✅ Run the function when the script is executed directly
if __name__ == "__main__":
    create_database()
