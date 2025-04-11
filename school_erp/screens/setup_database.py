import os
import sqlite3

def setup_database():
    # Get the absolute path to the database
    db_path = os.path.join(os.path.dirname(__file__), "school_erp.db")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create teachers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id TEXT PRIMARY KEY,
        name TEXT,
        mother_name TEXT,
        dob TEXT,
        age INTEGER,
        cast_category TEXT,
        place TEXT,
        tal TEXT,
        dist TEXT,
        state TEXT,
        adar_no TEXT,
        contact_no TEXT,
        designation TEXT,
        department TEXT,
        joining_date TEXT,
        bank_account TEXT,
        pf_no TEXT
    )
    ''')
    
    # Create salary_structure table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS salary_structure (
        teacher_id TEXT,
        basic_salary REAL,
        da_amount REAL,
        hra_amount REAL,
        conveyance REAL,
        medical REAL,
        other_allowances REAL,
        pf_deduction REAL,
        professional_tax REAL,
        income_tax REAL,
        other_deductions REAL,
        FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
    )
    ''')
    
    # Create salary_payments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS salary_payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id TEXT,
        payment_date TEXT,
        month_year TEXT,
        working_days INTEGER,
        holidays INTEGER,
        total_earnings REAL,
        total_deductions REAL,
        net_salary REAL,
        payment_method TEXT,
        payment_status TEXT,
        FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
    )
    ''')
    
    # Insert some sample data
    sample_teacher = (
        'T001', 'John Doe', 'Jane Doe', '1990-01-01', 33, 'General',
        'Mumbai', 'Mumbai', 'Mumbai', 'Maharashtra', '123456789012',
        '9876543210', 'Senior Teacher', 'Mathematics', '2020-01-01',
        '1234567890', 'PF001'
    )
    
    cursor.execute('''
    INSERT OR IGNORE INTO teachers 
    (teacher_id, name, mother_name, dob, age, cast_category, place, tal, dist, state, adar_no, contact_no, designation, department, joining_date, bank_account, pf_no)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_teacher)
    
    # Insert sample salary structure
    sample_salary = (
        'T001', 50000.0, 10000.0, 5000.0, 2000.0, 1000.0, 2000.0,
        5000.0, 500.0, 1000.0, 500.0
    )
    
    cursor.execute('''
    INSERT OR IGNORE INTO salary_structure 
    (teacher_id, basic_salary, da_amount, hra_amount, conveyance, medical, other_allowances, pf_deduction, professional_tax, income_tax, other_deductions)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_salary)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database setup completed successfully!")

if __name__ == "__main__":
    setup_database() 