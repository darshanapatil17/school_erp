from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QFormLayout, QTextEdit, QHBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox,
                             QDialog, QComboBox, QStackedWidget)
from PyQt6.QtGui import QTextDocument
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtCore import Qt, QMargins
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screens.database import Database

# Create database instance
db = Database()

class PaymentDialog(QDialog):
    def __init__(self, amount, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Payment")
        self.setFixedWidth(400)
        layout = QVBoxLayout()
        
        # Amount to pay
        amount_label = QLabel(f"Amount Due: ₹{amount:.2f}")
        amount_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(amount_label)
        
        # Payment method selection
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Credit/Debit Card", "Check", "Bank Transfer", "UPI"])
        layout.addWidget(QLabel("Select Payment Method:"))
        layout.addWidget(self.method_combo)
        
        self.setLayout(layout)
        
        # Pay button
        self.pay_button = QPushButton("Pay Now")
        self.pay_button.clicked.connect(self.accept)
        layout.addWidget(self.pay_button)

class SalarySlipGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Salary Slip Generator")
        self.setGeometry(100, 100, 700, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        
        # Search Section
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Teacher ID")
        self.search_btn = QPushButton("Search")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        self.layout.addLayout(search_layout)
        
        # Title
        self.title = QLabel("ABC Public School")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        
        self.address = QLabel("123, Education Street, City Name, State - 123456")
        self.address.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.address)
        
        self.contact = QLabel("Phone: (123) 456-7890 | Email: info@abcpublicschool.com")
        self.contact.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.contact)
        
        self.salary_slip_label = QLabel("SALARY SLIP - " + datetime.now().strftime("%m/%Y"))
        self.salary_slip_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.salary_slip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.salary_slip_label)
        
        # Employee Details Form
        self.form_layout = QFormLayout()
        
        self.emp_name = QLineEdit()
        self.emp_id = QLineEdit()
        self.designation = QLineEdit()
        self.department = QLineEdit()
        self.joining_date = QLineEdit()
        self.bank_acc = QLineEdit()
        self.pf_no = QLineEdit()
        
        # Make fields read-only
        for field in [self.emp_name, self.emp_id, self.designation, self.department,
                      self.joining_date, self.bank_acc, self.pf_no]:
            field.setReadOnly(True)
        
        self.form_layout.addRow("Employee Name:", self.emp_name)
        self.form_layout.addRow("Employee ID:", self.emp_id)
        self.form_layout.addRow("Designation:", self.designation)
        self.form_layout.addRow("Department:", self.department)
        self.form_layout.addRow("Date of Joining:", self.joining_date)
        self.form_layout.addRow("Bank Account No:", self.bank_acc)
        self.form_layout.addRow("PF No:", self.pf_no)
        
        self.layout.addLayout(self.form_layout)
        
        # Salary Table
        self.table = QTableWidget(6, 4)
        self.table.setHorizontalHeaderLabels(["Earnings", "Amount (INR)", "Deductions", "Amount (INR)"])
        self.layout.addWidget(self.table)
        
        # Buttons Layout
        btn_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate Salary Slip")
        self.export_btn = QPushButton("Export to PDF")
        self.pay_btn = QPushButton("Pay Now")

        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.pay_btn)

        self.layout.addLayout(btn_layout)

        # Output Area
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)
        
        # Set layout for central widget
        self.central_widget.setLayout(self.layout)
        
        # Connect buttons to functions
        self.generate_btn.clicked.connect(self.generate_salary_slip)
        self.export_btn.clicked.connect(self.export_to_pdf)
        self.pay_btn.clicked.connect(self.show_payment_dialog)

    def generate_salary_slip(self):
        self.text_output.setPlainText("Salary Slip Generated Successfully!")

    def export_to_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Salary Slip", "", "PDF Files (*.pdf)")
        if file_path:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageMargins(QMargins(20, 20, 20, 20))
            
            doc = QTextDocument()
            doc.setPlainText(self.text_output.toPlainText())
            doc.print_(printer)
            QMessageBox.information(self, "Success", "PDF exported successfully!")

    def show_payment_dialog(self):
        dialog = PaymentDialog(10000, self)  # Assume 10000 is the amount for testing
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Success", "Payment processed successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SalarySlipGenerator()
    window.show()
    sys.exit(app.exec())
