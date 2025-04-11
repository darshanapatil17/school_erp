import sqlite3
import os

class DatabaseHandler:
    def __init__(self):
        # Get the path to the database file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(current_dir, 'school_data.db')
        
        # Connect to the database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def get_teacher_details(self, teacher_id):
        """Get teacher details by ID"""
        self.cursor.execute('''
            SELECT * FROM teachers 
            WHERE teacher_id = ?
        ''', (teacher_id,))
        return self.cursor.fetchone()
    
    def insert_salary_payment(self, teacher_id, payment_date, month_year, 
                            total_earnings, total_deductions, net_salary,
                            payment_method, payment_status):
        """Insert a new salary payment record"""
        self.cursor.execute('''
            INSERT INTO salary_payments 
            (teacher_id, payment_date, month_year, total_earnings, 
             total_deductions, net_salary, payment_method, payment_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (teacher_id, payment_date, month_year, total_earnings,
              total_deductions, net_salary, payment_method, payment_status))
        self.conn.commit()
    
    def close(self):
        """Close the database connection"""
        self.conn.close() 