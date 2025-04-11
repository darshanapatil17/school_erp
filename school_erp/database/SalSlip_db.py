import sqlite3
import pandas as pd
import os

# Set file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, 'teachers_data.xlsx')
DB_FILE = os.path.join(BASE_DIR, 'SalSlip.db')

def setup_database():
    # Read Excel file
    df = pd.read_excel(EXCEL_FILE)

    # Rename columns for consistency with expected schema
    df = df.rename(columns={
        "Employee ID": "employee_id",
        "Employee Name": "name",
        "Designation": "designation",
        "Department": "department",
        "Date of Joining": "joining_date",
        "Bank Account No": "bank_account",
        "PF No": "pf_number",
        "Pay Period": "pay_period",
        "Basic Pay": "basic_pay",
        "HRA": "hra",
        "Other Allowances": "other_allowances",
        "Tax Deductions": "tax_deductions"
    })

    # Create and connect to SQLite DB
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the employees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        name TEXT,
        designation TEXT,
        department TEXT,
        joining_date TEXT,
        bank_account TEXT,
        pf_number TEXT,
        pay_period TEXT,
        basic_pay REAL,
        hra REAL,
        other_allowances REAL,
        tax_deductions REAL
    );
    """)

    # Insert data from Excel into table
    df.to_sql('employees', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
    print("Database setup completed. Data inserted into SalSlip.db.")

if __name__ == "__main__":
    setup_database()
