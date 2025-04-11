import sys
import os
import pandas as pd
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QFrame, QStackedLayout, QTextEdit,
    QListWidget, QListWidgetItem, QDateTimeEdit, QLineEdit,
    QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QFileDialog, QDialog, QGroupBox, QComboBox,
    QMainWindow, QRadioButton, QButtonGroup
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import Qt, QTimer, QTime, QDateTime, QMargins
from PyQt6.QtGui import QFont, QTextDocument
from datetime import datetime

class SalaryDatabase:
    def __init__(self):
        self.setup_database()

    def setup_database(self):
        """Initialize the salary database with required tables"""
        try:
            self.conn = sqlite3.connect("school_data.db")
            self.cursor = self.conn.cursor()

            # Create teachers table if not exists
            self.cursor.execute('''
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

            # Create salary_payments table if not exists
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salary_payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

            self.conn.commit()
            print("Salary database initialized successfully!")

        except Exception as e:
            print(f"Error setting up database: {e}")

    def get_teacher_details(self, teacher_id):
        """Get teacher details including salary structure"""
        try:
            self.cursor.execute('''
                SELECT * FROM teachers WHERE teacher_id = ?
            ''', (teacher_id,))
            
            teacher = self.cursor.fetchone()
            if teacher:
                # Convert to dictionary with column names
                columns = [description[0] for description in self.cursor.description]
                teacher_dict = dict(zip(columns, teacher))
                
                # Calculate derived values
                basic_salary = teacher_dict['basic_salary']
                da_amount = basic_salary * (teacher_dict['da_percent'] / 100)
                hra_amount = basic_salary * (teacher_dict['hra_percent'] / 100)
                
                # Return complete teacher details
                return {
                    'name': teacher_dict['name'],
                    'designation': teacher_dict['designation'],
                    'department': teacher_dict['department'],
                    'joining_date': teacher_dict['joining_date'],
                    'bank_account': teacher_dict['bank_account'],
                    'pf_no': teacher_dict['pf_no'],
                    'salary_structure': {
                        'basic_salary': basic_salary,
                        'da_amount': da_amount,
                        'hra_amount': hra_amount,
                        'conveyance': teacher_dict['conveyance'],
                        'medical': teacher_dict['medical'],
                        'other_allowances': teacher_dict['other_allowances'],
                        'pf_deduction': teacher_dict['pf_deduction'],
                        'professional_tax': teacher_dict['professional_tax'],
                        'income_tax': teacher_dict['income_tax'],
                        'other_deductions': teacher_dict['other_deductions']
                    }
                }
            return None
        except Exception as e:
            print(f"Error getting teacher details: {e}")
            return None

    def record_salary_payment(self, payment_data):
        """Record a salary payment in the database"""
        try:
            self.cursor.execute('''
                INSERT INTO salary_payments (
                    teacher_id, payment_date, month_year,
                    total_earnings, total_deductions, net_salary,
                    payment_method, payment_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                payment_data['teacher_id'],
                payment_data['payment_date'],
                payment_data['month_year'],
                payment_data['total_earnings'],
                payment_data['total_deductions'],
                payment_data['net_salary'],
                payment_data['payment_method'],
                payment_data['payment_status']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error recording salary payment: {e}")
            return False

    def close(self):
        """Close the database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

class SalarySlipWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = SalaryDatabase()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(20, 10, 20, 10)
        
        # School Header
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(12)
        
        self.title = QLabel("ABC Public School")
        self.title.setFont(header_font)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        
        self.address = QLabel("123, Education Street, City Name, State - 123456")
        self.address.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.address)
        
        self.contact = QLabel("Phone: (123) 456-7890 | Email: info@abcpublicschool.com")
        self.contact.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.contact)
        
        # Employee Details Form
        form_font = QFont()
        form_font.setPointSize(10)
        
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(8)
        self.form_layout.setContentsMargins(0, 15, 0, 15)
        
        labels = ["Employee Name:", "Employee ID:", "Designation:", "Department:",
                 "Date of Joining:", "Bank Account No:", "PF No:", "Pay Period:"]
        
        self.fields = {}
        for label in labels:
            field_label = QLabel(label)
            field_label.setFont(form_font)
            field = QLineEdit()
            field.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 1px solid black;
                    background: transparent;
                    padding: 2px 0px;
                }
            """)
            self.fields[label] = field
            self.form_layout.addRow(field_label, field)
        
        # Set current month/year as pay period
        self.fields["Pay Period:"].setText(datetime.now().strftime("%m/%Y"))
        
        # Connect employee ID field to auto-fill function
        self.fields["Employee ID:"].returnPressed.connect(self.auto_fill_details)
        
        self.layout.addLayout(self.form_layout)
        
        # Salary Table
        self.table = QTableWidget(9, 4)
        self.table.setHorizontalHeaderLabels(["Earnings", "Amount (INR)", "Deductions", "Amount (INR)"])
        
        # Table styling
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(30)
        
        # Set column widths
        total_width = 660
        col_widths = [int(total_width * 0.3), int(total_width * 0.2),
                     int(total_width * 0.3), int(total_width * 0.2)]
        for i, width in enumerate(col_widths):
            self.table.setColumnWidth(i, width)
        
        # Initialize table rows
        rows = [
            ("Basic Salary", "", "Provident Fund (PF)", ""),
            ("Dearness Allowance (DA)", "", "Professional Tax", ""),
            ("House Rent Allowance", "", "Income Tax (TDS)", ""),
            ("Conveyance Allowance", "", "Other Deductions", ""),
            ("Medical Allowance", "", "Total Deductions", ""),
            ("Other Allowances", "", "", ""),
            ("Gross Salary", "", "", ""),
            ("", "", "", ""),
            ("Net Salary", "", "", "")
        ]
        
        for i, (e1, e2, d1, d2) in enumerate(rows):
            if e1:
                item = QTableWidgetItem(e1)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, 0, item)
            if d1:
                item = QTableWidgetItem(d1)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(i, 2, item)
        
        self.layout.addWidget(self.table)
        
        # Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        
        self.export_btn = QPushButton("Generate PDF")
        self.pay_btn = QPushButton("Make Payment")
        
        button_style = """
            QPushButton {
                background-color: white;
                border: 1px solid black;
                border-radius: 3px;
                padding: 5px 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """
        
        for btn in [self.export_btn, self.pay_btn]:
            btn.setStyleSheet(button_style)
            btn.setFixedHeight(30)
        
        self.export_btn.clicked.connect(self.generate_pdf)
        self.pay_btn.clicked.connect(self.make_payment)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.pay_btn)
        btn_layout.addStretch()
        
        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)

    def auto_fill_details(self):
        try:
            emp_id = self.fields["Employee ID:"].text().strip()
            if not emp_id:
                return
            
            # Get teacher details from database
            teacher = self.db.get_teacher_details(emp_id)
            if not teacher:
                QMessageBox.warning(self, "Not Found", f"No employee found with ID: {emp_id}")
                return
            
            # Fill employee details
            self.fields["Employee Name:"].setText(str(teacher['name']))
            self.fields["Designation:"].setText(str(teacher['designation']))
            self.fields["Department:"].setText(str(teacher['department']))
            self.fields["Date of Joining:"].setText(str(teacher['joining_date']))
            self.fields["Bank Account No:"].setText(str(teacher['bank_account']))
            self.fields["PF No:"].setText(str(teacher['pf_no']))
            
            # Get salary structure
            salary = teacher['salary_structure']
            
            # Fill salary table
            self.table.setItem(0, 1, QTableWidgetItem(f"{salary['basic_salary']:.2f}"))
            self.table.setItem(1, 1, QTableWidgetItem(f"{salary['da_amount']:.2f}"))
            self.table.setItem(2, 1, QTableWidgetItem(f"{salary['hra_amount']:.2f}"))
            self.table.setItem(3, 1, QTableWidgetItem(f"{salary['conveyance']:.2f}"))
            self.table.setItem(4, 1, QTableWidgetItem(f"{salary['medical']:.2f}"))
            self.table.setItem(5, 1, QTableWidgetItem(f"{salary['other_allowances']:.2f}"))
            
            # Fill deductions
            self.table.setItem(0, 3, QTableWidgetItem(f"{salary['pf_deduction']:.2f}"))
            self.table.setItem(1, 3, QTableWidgetItem(f"{salary['professional_tax']:.2f}"))
            self.table.setItem(2, 3, QTableWidgetItem(f"{salary['income_tax']:.2f}"))
            self.table.setItem(3, 3, QTableWidgetItem(f"{salary['other_deductions']:.2f}"))
            
            # Calculate totals
            total_earnings = (
                salary['basic_salary'] +
                salary['da_amount'] +
                salary['hra_amount'] +
                salary['conveyance'] +
                salary['medical'] +
                salary['other_allowances']
            )
            
            total_deductions = (
                salary['pf_deduction'] +
                salary['professional_tax'] +
                salary['income_tax'] +
                salary['other_deductions']
            )
            
            net_salary = total_earnings - total_deductions
            
            # Show totals
            self.table.setItem(6, 0, QTableWidgetItem("Gross Salary"))
            self.table.setItem(6, 1, QTableWidgetItem(f"{total_earnings:.2f}"))
            self.table.setItem(4, 2, QTableWidgetItem("Total Deductions"))
            self.table.setItem(4, 3, QTableWidgetItem(f"{total_deductions:.2f}"))
            self.table.setItem(8, 0, QTableWidgetItem("Net Salary"))
            self.table.setItem(8, 1, QTableWidgetItem(f"{net_salary:.2f}"))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to auto-fill details: {str(e)}")
            import traceback
            traceback.print_exc()

    def calculate_totals(self):
        try:
            # Calculate gross salary
            gross = 0
            for row in range(6):  # First 6 rows are earnings
                amount = self.table.item(row, 1)
                if amount and amount.text():
                    gross += float(amount.text())
            
            # Set gross salary
            self.table.setItem(6, 1, QTableWidgetItem(str(gross)))
            
            # Calculate total deductions
            total_deductions = 0
            for row in range(4):  # First 4 rows are deductions
                amount = self.table.item(row, 3)
                if amount and amount.text():
                    total_deductions += float(amount.text())
            
            # Set total deductions
            self.table.setItem(4, 3, QTableWidgetItem(str(total_deductions)))
            
            # Calculate and set net salary
            net = gross - total_deductions
            self.table.setItem(8, 1, QTableWidgetItem(str(net)))
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate totals: {str(e)}")

    def generate_pdf(self):
        try:
            if not self.fields["Employee ID:"].text():
                QMessageBox.warning(self, "Missing Data", "Please enter an Employee ID and generate salary details first.")
                return

            # Ask user where to save the PDF
            emp_id = self.fields["Employee ID:"].text()
            pay_period = self.fields["Pay Period:"].text().replace('/', '_')
            suggested_name = f"salary_slip_{emp_id}_{pay_period}.pdf"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Salary Slip PDF",
                suggested_name,
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return  # User cancelled

            # Create PDF
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            
            # Set page size to match form (700x800)
            doc = SimpleDocTemplate(file_path, pagesize=(700, 800), rightMargin=20, leftMargin=20, topMargin=10, bottomMargin=10)
            
            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=14,
                textColor=colors.HexColor('#0000FF'),  # Blue color for title
                spaceAfter=10,
                alignment=1
            )
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=5,
                alignment=1
            )
            bold_style = ParagraphStyle(
                'CustomBold',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=5,
                alignment=0,
                fontName='Helvetica-Bold'
            )
            
            content = []
            
            # Add header
            content.append(Paragraph("ABC Public School", title_style))
            content.append(Paragraph("123, Education Street, City Name, State - 123456", normal_style))
            content.append(Paragraph("Phone: (123) 456-7890 | Email: info@abcpublicschool.com", normal_style))
            content.append(Spacer(1, 10))
            content.append(Paragraph("SALARY SLIP", title_style))
            content.append(Paragraph(f"For the Month of: {self.fields['Pay Period:'].text()}", normal_style))
            content.append(Spacer(1, 10))
            
            # Add employee details
            emp_details = [
                ["Employee Name:", self.fields["Employee Name:"].text(), "Employee ID:", self.fields["Employee ID:"].text()],
                ["Designation:", self.fields["Designation:"].text(), "Department:", self.fields["Department:"].text()],
                ["Date of Joining:", self.fields["Date of Joining:"].text(), "Bank Account No:", self.fields["Bank Account No:"].text()],
                ["PF No:", self.fields["PF No:"].text(), "Pay Period:", self.fields["Pay Period:"].text()]
            ]
            
            emp_table = Table(emp_details, colWidths=[100, 200, 100, 200])
            emp_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            content.append(emp_table)
            content.append(Spacer(1, 10))
            
            # Helper function to safely get table cell text
            def get_cell_text(row, col):
                item = self.table.item(row, col)
                if item:
                    text = item.text()
                    # Remove any remaining ■ characters and clean up the text
                    text = text.replace('■', '').strip()
                    return text
                return ""
            
            # Prepare salary data
            salary_data = [["Earnings", "Amount (INR)", "Deductions", "Amount (INR)"]]
            
            # Add regular rows
            for i in range(6):
                row = [
                    get_cell_text(i, 0),  # Earnings description
                    get_cell_text(i, 1),  # Earnings amount
                    get_cell_text(i, 2),  # Deductions description
                    get_cell_text(i, 3)   # Deductions amount
                ]
                salary_data.append(row)
            
            # Add Gross Salary and Total Deductions
            salary_data.append([
                get_cell_text(6, 0),  # Gross Salary
                get_cell_text(6, 1),  # Gross Amount
                get_cell_text(6, 2),  # Total Deductions
                get_cell_text(6, 3)   # Deductions Amount
            ])
            
            # Add empty row
            salary_data.append(["", "", "", ""])
            
            # Add Net Salary
            salary_data.append([
                get_cell_text(8, 0),  # Net Salary
                get_cell_text(8, 1),  # Net Amount
                "", ""
            ])
            
            # Create salary table
            salary_table = Table(salary_data, colWidths=[150, 100, 150, 100])  # Adjusted column widths
            salary_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Header alignment
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),    # First column left align
                ('ALIGN', (1, 1), (1, -1), 'RIGHT'),   # Second column right align
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # Third column left align
                ('ALIGN', (3, 1), (3, -1), 'RIGHT'),   # Fourth column right align
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),  # Make totals bold
            ]))
            content.append(salary_table)
            content.append(Spacer(1, 10))
            
            # Footer details
            footer_details = [
                ["Payment Mode:", "Bank Transfer / Cheque"],  # Filled payment mode field
                ["Salary Disbursed on:", "[DD/MM/YYYY]"],
                ["Authorized Signatory", "(Principal / Administrator)"]
            ]
            footer_table = Table(footer_details, colWidths=[150, 350])
            footer_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            content.append(footer_table)
            
            # Build PDF
            doc.build(content)
            
            QMessageBox.information(self, "Success", f"PDF saved successfully at:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF: {str(e)}")
            import traceback
            traceback.print_exc()

    def make_payment(self):
        try:
            # Create payment dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("Make Payment")
            dialog.setFixedSize(400, 300)
            
            layout = QVBoxLayout()
            
            # Payment method selection
            method_group = QGroupBox("Payment Method")
            method_layout = QVBoxLayout()
            
            methods = ["Cash", "Cheque", "Bank Transfer", "UPI"]
            method_buttons = QButtonGroup()
            
            for method in methods:
                radio = QRadioButton(method)
                method_layout.addWidget(radio)
                method_buttons.addButton(radio)
            
            method_group.setLayout(method_layout)
            layout.addWidget(method_group)
            
            # Payment details
            details_group = QGroupBox("Payment Details")
            details_layout = QFormLayout()
            
            amount_label = QLabel("Amount:")
            amount_value = QLabel(self.table.item(8, 1).text())
            
            date_label = QLabel("Payment Date:")
            date_input = QDateTimeEdit()
            date_input.setDateTime(QDateTime.currentDateTime())
            
            details_layout.addRow(amount_label, amount_value)
            details_layout.addRow(date_label, date_input)
            
            details_group.setLayout(details_layout)
            layout.addWidget(details_group)
            
            # Buttons
            button_layout = QHBoxLayout()
            confirm_btn = QPushButton("Confirm Payment")
            cancel_btn = QPushButton("Cancel")
            
            button_layout.addWidget(confirm_btn)
            button_layout.addWidget(cancel_btn)
            layout.addLayout(button_layout)
            
            dialog.setLayout(layout)
            
            # Connect signals
            confirm_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Record payment in database
                payment_data = {
                    'teacher_id': self.fields["Employee ID:"].text(),
                    'payment_date': date_input.dateTime().toString("yyyy-MM-dd"),
                    'month_year': self.fields["Pay Period:"].text(),
                    'total_earnings': float(self.table.item(6, 1).text()),
                    'total_deductions': float(self.table.item(4, 3).text()),
                    'net_salary': float(self.table.item(8, 1).text()),
                    'payment_method': [m for m in methods if method_buttons.checkedButton().text() == m][0],
                    'payment_status': "Completed"
                }
                
                if self.db.record_salary_payment(payment_data):
                    QMessageBox.information(self, "Success", "Payment processed successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to record payment.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process payment: {str(e)}")

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard - School ERP")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #eef9fd;")

        self.initDatabase()
        self.initUI()
        self.loadDashboardData()

    def initDatabase(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect("school_data.db")
        self.cursor = self.conn.cursor()
        # Create notices table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def initUI(self):
        """Initialize User Interface"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === Left Sidebar ===
        left_menu = QFrame()
        left_menu.setFixedWidth(230)
        left_menu.setStyleSheet("background-color: #0f1b2d;")
        left_layout = QVBoxLayout(left_menu)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setSpacing(10)

        title = QLabel("Dashboard Menu")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title)

        # Sidebar Buttons with Signals
        buttons = {
            "Auto Reply Email Assistant": None,
            "Digital Notice Board": self.showNoticeBoard,
            "Fee Payment": None,
            "Lost & Found / AI Complaint Tracker": None,
            "Teacher Attendance": None,
            "Salary Slip - Teacher Payment": self.showSalarySlip,
            "Student Record Finder": None,
            "Auto-Generated Certificates": None,
            "Staff Meeting Scheduler": None,
            "Student Admission Process": None,
            "Teacher Admission Process": None,
        }

        for text, handler in buttons.items():
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1f2c3c;
                    color: white;
                    padding: 8px;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2e3f54;
                }
            """)
            if handler:
                btn.clicked.connect(handler)
            left_layout.addWidget(btn)

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4d;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff1a1a;
            }
        """)
        left_layout.addWidget(logout_btn)

        # === Right Side (Main Content Area using QStackedLayout) ===
        self.stack = QStackedLayout()
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.stack)
        self.stack.setContentsMargins(0, 0, 0, 0)

        # Main Dashboard Screen
        self.dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(self.dashboard_widget)
        dashboard_layout.setContentsMargins(30, 30, 30, 30)

        top_bar_layout = QHBoxLayout()
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.clock_label)
        dashboard_layout.addLayout(top_bar_layout)

        timer = QTimer(self)
        timer.timeout.connect(self.updateClock)
        timer.start(1000)
        self.updateClock()

        center_content = QVBoxLayout()
        center_content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_label = QLabel("Welcome, Admin!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        center_content.addWidget(welcome_label)

        cards_layout = QHBoxLayout()
        self.total_students_card = QLabel("Total Students: Loading...")
        self.pending_fees_card = QLabel("Pending Fees: Loading...")
        self.total_teachers_card = QLabel("Total Teachers: Loading...")

        for card in [self.total_students_card, self.pending_fees_card, self.total_teachers_card]:
            card.setFixedSize(180, 60)
            card.setStyleSheet("background-color: #6d78f6; color: white; font-weight: bold; border-radius: 10px;")
            card.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cards_layout.addWidget(card)

        center_content.addLayout(cards_layout)
        dashboard_layout.addLayout(center_content)

        # Add Dashboard to Stacked Layout
        self.stack.addWidget(self.dashboard_widget)

        # Add Layouts to Main Window
        main_layout.addWidget(left_menu)
        main_layout.addWidget(self.right_widget, stretch=1)

    def updateClock(self):
        """Update real-time clock"""
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.clock_label.setText(f"🕒 {current_time}")

    def loadDashboardData(self):
        """Fetch student, pending fees, and teacher data from the database"""
        try:
            df = pd.read_excel("screens/students.xlsx", skiprows=3)
            df.columns = df.columns.str.strip().str.lower()
            df.rename(columns={
                "babalad vakratunda shrishail": "student_name",
                "joyti": "roll_no",
                "akurdi": "dob"
            }, inplace=True)

            total_students = df.shape[0] if "student_name" in df.columns else 0
            self.total_students_card.setText(f"Total Students: {total_students}")

            self.cursor.execute("SELECT COUNT(*) FROM pending_fees")
            pending_fees = self.cursor.fetchone()[0]
            self.pending_fees_card.setText(f"Pending Fees: {pending_fees}")

            self.cursor.execute("SELECT COUNT(*) FROM teachers")
            total_teachers = self.cursor.fetchone()[0]
            self.total_teachers_card.setText(f"Total Teachers: {total_teachers}")

        except Exception as e:
            print(f"❌ Error fetching dashboard data: {e}")

    def showNoticeBoard(self):
        """Create and show Digital Notice Board"""
        notice_board_widget = QWidget()
        notice_layout = QHBoxLayout(notice_board_widget)
        notice_layout.setContentsMargins(20, 20, 20, 20)

        # Left side - Notice List
        notice_list_widget = QWidget()
        notice_list_layout = QVBoxLayout(notice_list_widget)
        
        notice_list = QListWidget()
        notice_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e6f3ff;
            }
        """)
        
        # Load existing notices
        self.cursor.execute("SELECT title, timestamp FROM notices ORDER BY timestamp DESC")
        notices = self.cursor.fetchall()
        for title, timestamp in notices:
            item = QListWidgetItem(f"📢 {title}\n🕒 {timestamp}")
            notice_list.addItem(item)

        notice_list_layout.addWidget(notice_list)
        notice_layout.addWidget(notice_list_widget, stretch=1)

        # Right side - Create Notice
        create_notice_widget = QWidget()
        create_notice_layout = QVBoxLayout(create_notice_widget)
        create_notice_layout.setSpacing(15)

        title_label = QLabel("Notice Title:")
        title_label.setStyleSheet("font-weight: bold;")
        title_input = QTextEdit()
        title_input.setMaximumHeight(40)
        title_input.setPlaceholderText("Enter notice title...")

        content_label = QLabel("Notice Content:")
        content_label.setStyleSheet("font-weight: bold;")
        content_input = QTextEdit()
        content_input.setPlaceholderText("Enter notice content...")

        post_button = QPushButton("Post Notice")
        post_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        def post_notice():
            title = title_input.toPlainText().strip()
            content = content_input.toPlainText().strip()
            if title and content:
                timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                self.cursor.execute(
                    "INSERT INTO notices (title, content, timestamp) VALUES (?, ?, ?)",
                    (title, content, timestamp)
                )
                self.conn.commit()
                
                # Add to list
                item = QListWidgetItem(f"📢 {title}\n🕒 {timestamp}")
                notice_list.insertItem(0, item)
                
                # Clear inputs
                title_input.clear()
                content_input.clear()

        post_button.clicked.connect(post_notice)

        create_notice_layout.addWidget(title_label)
        create_notice_layout.addWidget(title_input)
        create_notice_layout.addWidget(content_label)
        create_notice_layout.addWidget(content_input)
        create_notice_layout.addWidget(post_button)
        create_notice_layout.addStretch()

        notice_layout.addWidget(create_notice_widget, stretch=1)

        # Add to stack and show
        self.stack.addWidget(notice_board_widget)
        self.stack.setCurrentWidget(notice_board_widget)

    def showSalarySlip(self):
        """Load and show Salary Slip Generator"""
        try:
            self.salary_slip_widget = SalarySlipWidget()
            self.stack.addWidget(self.salary_slip_widget)
            self.stack.setCurrentWidget(self.salary_slip_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load salary slip: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec())