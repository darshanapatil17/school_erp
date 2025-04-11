import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QComboBox,
    QFileDialog, QRadioButton, QButtonGroup, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime
from database import DatabaseHandler

class SalarySlipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Salary Slip Generator")
        self.setFixedSize(700, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(20, 10, 20, 10)
        
        # School Header
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(12)
        
        self.title = QLabel("ABC Public School")
        self.title.setFont(header_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        
        self.address = QLabel("123, Education Street, City Name, State - 123456")
        self.address.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.address)
        
        self.contact = QLabel("Phone: (123) 456-7890 | Email: info@abcpublicschool.com")
        self.contact.setAlignment(Qt.AlignCenter)
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
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
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
            ("House Rent Allowance ...", "", "Income Tax (TDS)", ""),
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
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table.setItem(i, 0, item)
            if d1:
                item = QTableWidgetItem(d1)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
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
        
        # Set layout for central widget
        self.central_widget.setLayout(self.layout)
        
        # Load employee database
        self.load_employee_database()
        
        # Initialize database handler
        self.db = DatabaseHandler()

    def load_employee_database(self):
        try:
            # Get the path to the Excel file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(current_dir, 'database', 'teachers_data.xlsx')
            
            # Load the Excel file
            self.employee_data = pd.read_excel(excel_path)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load employee database: {str(e)}")
            self.employee_data = None
    
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
            self.fields["Employee Name:"].setText(teacher['name'])
            self.fields["Designation:"].setText(teacher['designation'])
            self.fields["Department:"].setText(teacher['department'])
            self.fields["Date of Joining:"].setText(teacher['joining_date'])
            self.fields["Bank Account No:"].setText(teacher['bank_account'])
            self.fields["PF No:"].setText(teacher['pf_no'])

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
            # Get employee details
            emp_id = self.fields["Employee ID:"].text()
            emp_name = self.fields["Employee Name:"].text()
            bank_account = self.fields["Bank Account No:"].text()
            
            if not all([emp_id, emp_name, bank_account]):
                QMessageBox.warning(self, "Missing Information", "Please fill in all employee details.")
                return
            
            # Get net salary from table
            net_salary = float(self.table.item(8, 1).text().replace("₹", ""))
            
            # Create payment dialog
            payment_dialog = QDialog(self)
            payment_dialog.setWindowTitle("Payment Method")
            payment_dialog.setFixedWidth(400)
            
            layout = QVBoxLayout()
            
            # Payment method selection
            method_group = QGroupBox("Select Payment Method")
            method_layout = QVBoxLayout()
            
            payment_methods = {
                "Cash": ["Amount", "Received By"],
                "Cheque": ["Cheque Number", "Bank Name", "Branch"],
                "Card": ["Card Number", "Card Type", "Bank Name"],
                "UPI": ["UPI ID"],
                "Google Pay": ["Mobile Number"],
                "Phone Pay": ["Mobile Number"]
            }
            
            method_combo = QComboBox()
            method_combo.addItems(payment_methods.keys())
            method_layout.addWidget(method_combo)
            method_group.setLayout(method_layout)
            layout.addWidget(method_group)
            
            # Form for payment details
            form_group = QGroupBox("Payment Details")
            form_layout = QFormLayout()
            
            # Dictionary to store input fields
            input_fields = {}
            
            def update_form():
                # Clear existing fields
                while form_layout.rowCount() > 0:
                    form_layout.removeRow(0)
                input_fields.clear()
                
                # Add fields for selected method
                method = method_combo.currentText()
                for field in payment_methods[method]:
                    input_fields[field] = QLineEdit()
                    form_layout.addRow(field + ":", input_fields[field])
                
                # Add common fields
                form_layout.addRow("Amount:", QLabel(f"₹{net_salary:.2f}"))
                form_layout.addRow("Date:", QLabel(datetime.now().strftime("%d/%m/%Y")))
                form_layout.addRow("Employee:", QLabel(f"{emp_name} ({emp_id})"))
            
            method_combo.currentTextChanged.connect(update_form)
            update_form()  # Initialize with first method
            
            form_group.setLayout(form_layout)
            layout.addWidget(form_group)
            
            # Buttons
            button_layout = QHBoxLayout()
            process_btn = QPushButton("Process Payment")
            cancel_btn = QPushButton("Cancel")
            
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
            
            process_btn.setStyleSheet(button_style)
            cancel_btn.setStyleSheet(button_style)
            
            button_layout.addWidget(process_btn)
            button_layout.addWidget(cancel_btn)
            layout.addLayout(button_layout)
            
            payment_dialog.setLayout(layout)
            
            def process_payment():
                # Validate required fields
                method = method_combo.currentText()
                missing_fields = []
                for field in payment_methods[method]:
                    if not input_fields[field].text().strip():
                        missing_fields.append(field)
                
                if missing_fields:
                    QMessageBox.warning(
                        payment_dialog,
                        "Missing Information",
                        f"Please fill in the following fields:\n" + "\n".join(missing_fields)
                    )
                    return
                
                # Show confirmation
                details = [f"Payment Method: {method}"]
                for field in payment_methods[method]:
                    details.append(f"{field}: {input_fields[field].text()}")
                details.extend([
                    f"Amount: ₹{net_salary:.2f}",
                    f"Employee: {emp_name} ({emp_id})",
                    f"Date: {datetime.now().strftime('%d/%m/%Y')}"
                ])
                
                confirm = QMessageBox.question(
                    payment_dialog,
                    "Confirm Payment",
                    "Please confirm the payment details:\n\n" + "\n".join(details),
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if confirm == QMessageBox.Yes:
                    QMessageBox.information(payment_dialog, "Success", "Payment processed successfully!")
                    payment_dialog.accept()
            
            process_btn.clicked.connect(process_payment)
            cancel_btn.clicked.connect(payment_dialog.reject)
            
            payment_dialog.exec_()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Payment failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SalarySlipApp()
    window.show()
    sys.exit(app.exec_())
