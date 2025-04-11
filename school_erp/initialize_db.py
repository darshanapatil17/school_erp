import sqlite3
import os
from screens.database import Database, DatabaseHandler
from screens.sample_data import SampleData

def initialize_users_db():
    """Initialize the users database with admin and teacher accounts"""
    db_path = os.path.join(os.path.dirname(__file__), "screens", "users.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Add sample users
    sample_users = [
        ('admin', 'admin123', 'admin'),
        ('teacher1', 'teacher123', 'teacher'),
        ('teacher2', 'teacher123', 'teacher')
    ]

    cursor.executemany('INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)', sample_users)
    conn.commit()
    conn.close()

def initialize_salary_db():
    """Initialize the salary database with sample data"""
    # Initialize database
    db = Database()
    db_handler = DatabaseHandler()
    sample_data = SampleData()

    # Load sample teacher data
    teachers = sample_data.get_sample_teachers()
    
    # Save teacher data to both databases
    for teacher in teachers:
        # Save to school_erp.db
        db.cursor.execute('''
        INSERT OR REPLACE INTO teachers 
        (teacher_id, name, designation, department, joining_date, bank_account, pf_no)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            teacher['id'],
            teacher['name'],
            teacher['designation'],
            teacher['department'],
            teacher['joining_date'],
            teacher['bank_account'],
            teacher['pf_number']
        ))

        # Save salary structure
        db.cursor.execute('''
        INSERT OR REPLACE INTO salary_structure 
        (teacher_id, basic_salary, da_amount, hra_amount, conveyance, medical, 
        other_allowances, pf_deduction, professional_tax, income_tax, other_deductions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            teacher['id'],
            teacher['basic_salary'],
            teacher['da'],
            teacher['hra'],
            teacher['conveyance'],
            teacher['medical'],
            teacher['other_allowances'],
            teacher['pf'],
            teacher['professional_tax'],
            teacher['income_tax'],
            teacher['other_deductions']
        ))

        # Save to salary_slip.db
        emp_data = {
            'id': teacher['id'],
            'name': teacher['name'],
            'designation': teacher['designation'],
            'department': teacher['department'],
            'joining_date': teacher['joining_date'],
            'bank_account': teacher['bank_account'],
            'pf_number': teacher['pf_number']
        }
        db_handler.save_employee(emp_data)

    db.conn.commit()
    db.close()

def main():
    print("Initializing databases...")
    try:
        initialize_users_db()
        print("✓ Users database initialized")
        
        initialize_salary_db()
        print("✓ Salary database initialized")
        
        print("\nDatabases initialized successfully!")
        print("\nYou can now run the application with these credentials:")
        print("Admin login:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nTeacher login:")
        print("  Username: teacher1")
        print("  Password: teacher123")
        
    except Exception as e:
        print(f"Error initializing databases: {str(e)}")

if __name__ == "__main__":
    main() 