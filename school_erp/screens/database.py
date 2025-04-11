import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        # Get the absolute path to the database
        db_path = os.path.join(os.path.dirname(__file__), "school_erp.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create teachers table
        self.cursor.execute('''
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
        self.cursor.execute('''
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
        self.cursor.execute('''
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

        self.conn.commit()

    def close(self):
        self.conn.close()

class DatabaseHandler:
    def __init__(self):
        self.db_name = os.path.join(os.path.dirname(__file__), "salary_slip.db")
        self.setup_database()

    def setup_database(self):
        """Create necessary tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Create employees table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    designation TEXT,
                    department TEXT,
                    joining_date TEXT,
                    bank_account TEXT,
                    pf_number TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create salary_slips table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS salary_slips (
                    slip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT,
                    pay_period TEXT,
                    basic_salary REAL,
                    da REAL,
                    hra REAL,
                    conveyance REAL,
                    medical REAL,
                    other_allowances REAL,
                    pf REAL,
                    professional_tax REAL,
                    income_tax REAL,
                    other_deductions REAL,
                    gross_salary REAL,
                    total_deductions REAL,
                    net_salary REAL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            ''')

            # Create payments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slip_id INTEGER,
                    amount REAL,
                    payment_method TEXT,
                    transaction_id TEXT,
                    payment_details TEXT,
                    status TEXT,
                    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (slip_id) REFERENCES salary_slips (slip_id)
                )
            ''')

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Database setup error: {str(e)}")
            raise

    def save_employee(self, emp_data):
        """Save or update employee information"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO employees 
                (id, name, designation, department, joining_date, bank_account, pf_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                emp_data['id'],
                emp_data['name'],
                emp_data['designation'],
                emp_data['department'],
                emp_data['joining_date'],
                emp_data['bank_account'],
                emp_data['pf_number']
            ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Save employee error: {str(e)}")
            return False

    def get_employee(self, emp_id):
        """Retrieve employee information"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'designation': result[2],
                    'department': result[3],
                    'joining_date': result[4],
                    'bank_account': result[5],
                    'pf_number': result[6]
                }
            return None

        except Exception as e:
            print(f"Get employee error: {str(e)}")
            return None

    def save_salary_slip(self, emp_id, pay_period, earnings, deductions, totals):
        """Save salary slip information"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO salary_slips 
                (employee_id, pay_period, basic_salary, da, hra, conveyance, medical, 
                other_allowances, pf, professional_tax, income_tax, other_deductions,
                gross_salary, total_deductions, net_salary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                emp_id,
                pay_period,
                float(earnings.get('Basic Salary', 0)),
                float(earnings.get('Dearness Allowance (DA)', 0)),
                float(earnings.get('House Rent Allowance (HRA)', 0)),
                float(earnings.get('Conveyance Allowance', 0)),
                float(earnings.get('Medical Allowance', 0)),
                float(earnings.get('Other Allowances', 0)),
                float(deductions.get('Provident Fund (PF)', 0)),
                float(deductions.get('Professional Tax', 0)),
                float(deductions.get('Income Tax (TDS)', 0)),
                float(deductions.get('Other Deductions', 0)),
                float(totals['gross_salary']),
                float(totals['total_deductions']),
                float(totals['net_salary'])
            ))

            slip_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return slip_id

        except Exception as e:
            print(f"Save salary slip error: {str(e)}")
            return None

    def save_payment(self, slip_id, amount, payment_method, payment_details):
        """Save payment information"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            transaction_id = datetime.now().strftime('%Y%m%d%H%M%S')
            
            cursor.execute('''
                INSERT INTO payments 
                (slip_id, amount, payment_method, transaction_id, payment_details, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                slip_id,
                amount,
                payment_method,
                transaction_id,
                payment_details,
                'COMPLETED'
            ))

            conn.commit()
            conn.close()
            return transaction_id

        except Exception as e:
            print(f"Save payment error: {str(e)}")
            return None

    def get_salary_history(self, emp_id):
        """Retrieve salary history for an employee"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT s.*, p.payment_method, p.transaction_id, p.status
                FROM salary_slips s
                LEFT JOIN payments p ON s.slip_id = p.slip_id
                WHERE s.employee_id = ?
                ORDER BY s.generated_at DESC
            ''', (emp_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            history = []
            for row in results:
                history.append({
                    'slip_id': row[0],
                    'pay_period': row[2],
                    'gross_salary': row[12],
                    'net_salary': row[14],
                    'generated_at': row[15],
                    'payment_method': row[16] if row[16] else 'Pending',
                    'transaction_id': row[17] if row[17] else '',
                    'payment_status': row[18] if row[18] else 'Pending'
                })
            
            return history

        except Exception as e:
            print(f"Get salary history error: {str(e)}")
            return []

    def get_payment_details(self, slip_id):
        """Retrieve payment details for a salary slip"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM payments WHERE slip_id = ?
            ''', (slip_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'payment_id': result[0],
                    'amount': result[2],
                    'payment_method': result[3],
                    'transaction_id': result[4],
                    'payment_details': result[5],
                    'status': result[6],
                    'paid_at': result[7]
                }
            return None

        except Exception as e:
            print(f"Get payment details error: {str(e)}")
            return None

# Create an instance of the database
db = Database()

# Create an instance of the database handler
db_handler = DatabaseHandler() 