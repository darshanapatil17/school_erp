from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QTableWidget, QTableWidgetItem, QLabel, QPushButton,
                             QComboBox, QHeaderView)
from PyQt6.QtCore import Qt
import sys
import os
import sqlite3

# Database connection
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('school_erp.db')
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

# Create database instance
db = Database()

class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School ERP Database Viewer")
        self.setGeometry(100, 100, 1200, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Teachers Tab
        teachers_tab = QWidget()
        teachers_layout = QVBoxLayout(teachers_tab)
        
        # Teachers Table
        self.teachers_table = QTableWidget()
        self.teachers_table.setColumnCount(12)
        self.teachers_table.setHorizontalHeaderLabels([
            "ID", "Name", "Mother's Name", "DOB", "Age", "Category",
            "Place", "District", "State", "Aadhar", "Contact", "Department"
        ])
        self.teachers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        teachers_layout.addWidget(self.teachers_table)
        
        # Salary Structure Tab
        salary_tab = QWidget()
        salary_layout = QVBoxLayout(salary_tab)
        
        # Teacher selector for salary
        salary_select_layout = QHBoxLayout()
        salary_select_layout.addWidget(QLabel("Select Teacher:"))
        self.salary_teacher_combo = QComboBox()
        self.salary_teacher_combo.currentIndexChanged.connect(self.load_salary_data)
        salary_select_layout.addWidget(self.salary_teacher_combo)
        salary_layout.addLayout(salary_select_layout)
        
        # Salary Table
        self.salary_table = QTableWidget()
        self.salary_table.setColumnCount(5)
        self.salary_table.setRowCount(6)
        self.salary_table.setHorizontalHeaderLabels([
            "Component", "Amount", "Deduction Type", "Amount", "Net"
        ])
        self.salary_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        salary_layout.addWidget(self.salary_table)
        
        # Payment History Tab
        payments_tab = QWidget()
        payments_layout = QVBoxLayout(payments_tab)
        
        # Teacher selector for payments
        payment_select_layout = QHBoxLayout()
        payment_select_layout.addWidget(QLabel("Select Teacher:"))
        self.payment_teacher_combo = QComboBox()
        self.payment_teacher_combo.currentIndexChanged.connect(self.load_payment_data)
        payment_select_layout.addWidget(self.payment_teacher_combo)
        payments_layout.addLayout(payment_select_layout)
        
        # Payments Table
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(8)
        self.payments_table.setHorizontalHeaderLabels([
            "Date", "Month/Year", "Working Days", "Holidays",
            "Total Earnings", "Total Deductions", "Net Salary", "Status"
        ])
        self.payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        payments_layout.addWidget(self.payments_table)
        
        # Add tabs to tab widget
        tabs.addTab(teachers_tab, "Teachers")
        tabs.addTab(salary_tab, "Salary Structure")
        tabs.addTab(payments_tab, "Payment History")
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.load_all_data)
        layout.addWidget(refresh_btn)
        
        # Load initial data
        self.load_all_data()
    
    def load_all_data(self):
        self.load_teachers_data()
        self.update_teacher_combos()
        self.load_salary_data()
        self.load_payment_data()
    
    def load_teachers_data(self):
        db.cursor.execute("SELECT * FROM teachers")
        teachers = db.cursor.fetchall()
        
        self.teachers_table.setRowCount(len(teachers))
        for row, teacher in enumerate(teachers):
            for col in range(12):
                item = QTableWidgetItem(str(teacher[col]))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make read-only
                self.teachers_table.setItem(row, col, item)
    
    def update_teacher_combos(self):
        db.cursor.execute("SELECT teacher_id, name FROM teachers")
        teachers = db.cursor.fetchall()
        
        self.salary_teacher_combo.clear()
        self.payment_teacher_combo.clear()
        
        for teacher_id, name in teachers:
            display_text = f"{name} (ID: {teacher_id})"
            self.salary_teacher_combo.addItem(display_text, teacher_id)
            self.payment_teacher_combo.addItem(display_text, teacher_id)
    
    def load_salary_data(self):
        if self.salary_teacher_combo.currentData():
            teacher_id = self.salary_teacher_combo.currentData()
            
            db.cursor.execute("SELECT * FROM salary_structure WHERE teacher_id = ?", (teacher_id,))
            salary = db.cursor.fetchone()
            
            if salary:
                # Earnings
                earnings = [
                    ("Basic Salary", salary[1]),
                    ("DA", salary[2]),
                    ("HRA", salary[3]),
                    ("Conveyance", salary[4]),
                    ("Medical", salary[5]),
                    ("Other Allowances", salary[6])
                ]
                
                # Deductions
                deductions = [
                    ("PF", salary[7]),
                    ("Professional Tax", salary[8]),
                    ("Income Tax", salary[9]),
                    ("Other Deductions", salary[10])
                ]
                
                # Clear previous data
                self.salary_table.clearContents()
                
                # Fill data
                total_earnings = 0
                total_deductions = 0
                
                for row, (name, amount) in enumerate(earnings):
                    self.salary_table.setItem(row, 0, QTableWidgetItem(name))
                    self.salary_table.setItem(row, 1, QTableWidgetItem(f"₹{amount}"))
                    total_earnings += float(amount or 0)
                
                for row, (name, amount) in enumerate(deductions):
                    self.salary_table.setItem(row, 2, QTableWidgetItem(name))
                    self.salary_table.setItem(row, 3, QTableWidgetItem(f"₹{amount}"))
                    total_deductions += float(amount or 0)
                
                # Add totals
                self.salary_table.setItem(4, 0, QTableWidgetItem("Total Earnings"))
                self.salary_table.setItem(4, 1, QTableWidgetItem(f"₹{total_earnings}"))
                self.salary_table.setItem(4, 2, QTableWidgetItem("Total Deductions"))
                self.salary_table.setItem(4, 3, QTableWidgetItem(f"₹{total_deductions}"))
                
                # Add net salary
                net_salary = total_earnings - total_deductions
                self.salary_table.setItem(5, 0, QTableWidgetItem("NET SALARY"))
                self.salary_table.setItem(5, 4, QTableWidgetItem(f"₹{net_salary}"))
    
    def load_payment_data(self):
        if self.payment_teacher_combo.currentData():
            teacher_id = self.payment_teacher_combo.currentData()
            
            db.cursor.execute("SELECT * FROM salary_payments WHERE teacher_id = ? ORDER BY payment_date DESC", (teacher_id,))
            payments = db.cursor.fetchall()
            
            self.payments_table.setRowCount(len(payments))
            for row, payment in enumerate(payments):
                items = [
                    payment[2],  # payment_date
                    payment[3],  # month_year
                    str(payment[4]),  # working_days
                    str(payment[5]),  # holidays
                    f"₹{payment[6]}",  # total_earnings
                    f"₹{payment[7]}",  # total_deductions
                    f"₹{payment[8]}",  # net_salary
                    payment[10]  # status
                ]
                
                for col, item_text in enumerate(items):
                    item = QTableWidgetItem(item_text)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make read-only
                    self.payments_table.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseViewer()
    window.show()
    sys.exit(app.exec()) 