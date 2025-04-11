import sqlite3
import pandas as pd
import os
import sys

# Add the screens directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from database.create_excel import create_sample_data

def create_database():
    # Create Excel file with sample data
    create_sample_data()

    # Connect to SQLite Database
    conn = sqlite3.connect("school_data.db")
    cursor = conn.cursor()

    # Create Teachers Table with Salary Information
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id TEXT UNIQUE,
        name TEXT,
        designation TEXT,
        department TEXT,
        joining_date TEXT,
        bank_account TEXT,
        pf_no TEXT,
        basic_salary REAL,
        da_percent REAL,
        hra_percent REAL,
        conveyance REAL,
        medical REAL,
        other_allowances REAL,
        pf_deduction REAL,
        professional_tax REAL,
        income_tax REAL,
        other_deductions REAL
    )
    ''')

    # Load teacher data from Excel
    try:
        excel_path = os.path.join(current_dir, 'database', 'teachers_data.xlsx')
        teachers_df = pd.read_excel(excel_path)
        
        # Insert teacher data into database
        for _, row in teachers_df.iterrows():
            cursor.execute('''
                INSERT OR REPLACE INTO teachers (
                    teacher_id, name, designation, department, joining_date,
                    bank_account, pf_no, basic_salary, da_percent, hra_percent,
                    conveyance, medical, other_allowances, pf_deduction,
                    professional_tax, income_tax, other_deductions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Employee ID'], row['Employee Name'], row['Designation'], row['Department'],
                row['Date of Joining'], row['Bank Account'], row['PF Number'],
                row['Basic Salary'], row['DA Percent'], row['HRA Percent'],
                row['Conveyance'], row['Medical'], row['Other Allowances'],
                row['PF Deduction'], row['Professional Tax'], row['Income Tax'],
                row['Other Deductions']
            ))
        
        print("✅ Teacher data loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading teacher data: {e}")

    # Create Salary Payments Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS salary_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id TEXT,
        payment_date TEXT,
        month_year TEXT,
        total_earnings REAL,
        total_deductions REAL,
        net_salary REAL,
        payment_method TEXT,
        payment_status TEXT,
        FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
    )
    ''')

    # Commit and close
    conn.commit()
    conn.close()
    print("✅ Database setup completed!")

if __name__ == "__main__":
    create_database()


