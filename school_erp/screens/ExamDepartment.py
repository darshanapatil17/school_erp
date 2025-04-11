import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar,
                           QMenu, QTableWidget, QTableWidgetItem, QHeaderView,
                           QStackedWidget, QFileDialog, QMessageBox, QDialog,
                           QFormLayout, QDateEdit, QTimeEdit, QComboBox, QSpinBox,
                           QFrame, QDoubleSpinBox, QTabWidget, QGroupBox, QGridLayout,
                           QProgressBar, QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QAction, QColor
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from datetime import datetime

class AddExamDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Exam")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.exam_name = QLineEdit()
        self.grade = QComboBox()
        self.grade.addItems([f"{i}th" for i in range(6, 13)])
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.time = QTimeEdit()
        self.time.setTime(QTime(9, 0))
        self.venue = QLineEdit()
        self.room_capacity = QSpinBox()
        self.room_capacity.setRange(1, 200)
        self.total_students = QSpinBox()
        self.total_students.setRange(1, 200)
        self.supervisor = QLineEdit()

        # Add fields to form
        layout.addRow("Exam Name:", self.exam_name)
        layout.addRow("Grade:", self.grade)
        layout.addRow("Date:", self.date)
        layout.addRow("Time:", self.time)
        layout.addRow("Venue:", self.venue)
        layout.addRow("Room Capacity:", self.room_capacity)
        layout.addRow("Total Students:", self.total_students)
        layout.addRow("Supervisor:", self.supervisor)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_exam_data(self):
        return [
            self.exam_name.text(),
            self.grade.currentText(),
            self.date.date().toString("yyyy-MM-dd"),
            self.time.time().toString("HH:mm"),
            self.venue.text(),
            str(self.room_capacity.value()),
            str(self.total_students.value()),
            self.supervisor.text()
        ]

class AddInventoryDialog(QDialog):
    def __init__(self, parent=None, item_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Inventory Item")
        self.setModal(True)
        self.item_data = item_data
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.item_name = QLineEdit()
        self.department = QComboBox()
        self.department.addItems(["Mathematics", "Science", "English", "General"])
        self.available = QSpinBox()
        self.available.setRange(0, 10000)
        self.required = QSpinBox()
        self.required.setRange(0, 10000)
        self.cost_per_item = QDoubleSpinBox()
        self.cost_per_item.setRange(0, 10000)
        self.cost_per_item.setPrefix("$")
        self.cost_per_item.setDecimals(2)

        # Add fields to form
        layout.addRow("Item Name:", self.item_name)
        layout.addRow("Department:", self.department)
        layout.addRow("Available Quantity:", self.available)
        layout.addRow("Required Quantity:", self.required)
        layout.addRow("Cost per Item:", self.cost_per_item)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

        # If editing, populate fields
        if self.item_data:
            self.item_name.setText(self.item_data[0])
            self.department.setCurrentText(self.item_data[1])
            self.available.setValue(int(self.item_data[2]))
            self.required.setValue(int(self.item_data[3]))
            self.cost_per_item.setValue(float(self.item_data[5]))

    def get_inventory_data(self):
        available = self.available.value()
        required = self.required.value()
        cost_per_item = self.cost_per_item.value()
        total_cost = cost_per_item * required
        
        status = "Sufficient" if available >= required else "Need more"
        stock_level = min(100, int((available / required) * 100)) if required > 0 else 100
        
        return [
            self.item_name.text(),
            self.department.currentText(),
            str(available),
            str(required),
            status,
            f"{cost_per_item:.2f}",
            f"{total_cost:.2f}",
            stock_level
        ]

class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Student")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.student_name = QLineEdit()
        self.grade = QComboBox()
        self.grade.addItems(["10th", "11th", "12th"])
        self.roll_no = QLineEdit()
        self.last_exam_score = QSpinBox()
        self.last_exam_score.setRange(0, 100)
        self.attendance = QSpinBox()
        self.attendance.setRange(0, 100)

        # Add fields to form
        layout.addRow("Student Name:", self.student_name)
        layout.addRow("Grade:", self.grade)
        layout.addRow("Roll No:", self.roll_no)
        layout.addRow("Last Exam Score (%):", self.last_exam_score)
        layout.addRow("Attendance (%):", self.attendance)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_student_data(self):
        return [
            self.student_name.text(),
            self.grade.currentText(),
            self.roll_no.text(),
            f"{self.last_exam_score.value()}%",
            f"{self.attendance.value()}%"
        ]

class PreviousPapersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Previous Year Papers")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Access and manage previous exam papers")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Upload section
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search papers...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_papers)

        upload_btn = QPushButton("Upload Paper")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        upload_btn.clicked.connect(self.upload_paper)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(upload_btn)
        layout.addLayout(search_layout)

        # Papers table
        self.papers_table = QTableWidget()
        self.papers_table.setColumnCount(5)
        self.papers_table.setHorizontalHeaderLabels([
            "Paper Name", "Grade", "Uploaded By", "Date", "Actions"
        ])
        self.papers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data
        self.sample_data = [
            ["Mathematics Final 2022", "10th", "Ms. Johnson", "2022-12-10"],
            ["Science Midterm 2022", "9th", "Mr. Peterson", "2022-10-15"],
            ["English Final 2022", "11th", "Ms. Williams", "2022-12-05"],
            ["History Midterm 2022", "8th", "Dr. Miller", "2022-10-12"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.papers_table)

    def populate_table(self, data):
        self.papers_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.papers_table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Add Download button
            download_btn = QPushButton("Download")
            download_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f2f5;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #e4e6e9;
                }
            """)
            download_btn.clicked.connect(lambda checked, row=row: self.download_paper(row))
            self.papers_table.setCellWidget(row, 4, download_btn)

    def search_papers(self):
        search_text = self.search_box.text().lower()
        if not search_text:
            self.populate_table(self.sample_data)
            return
        
        filtered_data = [
            row for row in self.sample_data
            if any(search_text in str(cell).lower() for cell in row)
        ]
        self.populate_table(filtered_data)

    def upload_paper(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Upload Paper",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_name:
            QMessageBox.information(
                self,
                "Success",
                "Paper uploaded successfully!",
                QMessageBox.StandardButton.Ok
            )
            
            # Add the new paper to the table
            base_name = os.path.basename(file_name)
            new_paper = [
                base_name,
                "10th",  # Default grade
                "Current User",
                datetime.now().strftime("%Y-%m-%d")
            ]
            self.sample_data.insert(0, new_paper)
            self.populate_table(self.sample_data)

    def download_paper(self, row):
        paper_name = self.papers_table.item(row, 0).text()
        QMessageBox.information(
            self,
            "Download",
            f"Downloading {paper_name}...",
            QMessageBox.StandardButton.Ok
        )

class UpcomingExamsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Upcoming Examinations")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Schedule and manage upcoming school exams")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Add Exam section
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search exams...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_exams)

        add_exam_btn = QPushButton("Add Exam")
        add_exam_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        add_exam_btn.clicked.connect(self.add_exam)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(add_exam_btn)
        layout.addLayout(search_layout)

        # Exams table
        self.exams_table = QTableWidget()
        self.exams_table.setColumnCount(8)
        self.exams_table.setHorizontalHeaderLabels([
            "Exam Name", "Grade", "Date", "Time", "Venue",
            "Room Capacity", "Total Students", "Supervisor Name"
        ])
        self.exams_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data
        self.sample_data = [
            ["Mathematics Final Exam", "10th", "2023-10-15", "09:00", "Hall A", "50", "45", "Dr. Smith"],
            ["Science Midterm Exam", "9th", "2023-10-18", "10:30", "Lab Complex", "40", "38", "Prof. Johnson"],
            ["English Essay Test", "11th", "2023-10-20", "11:00", "Hall B", "60", "55", "Mrs. Williams"],
            ["History Quiz", "8th", "2023-10-22", "09:30", "Room 105", "35", "30", "Mr. Davis"],
            ["Computer Practical Test", "12th", "2023-10-25", "13:00", "Computer Lab", "30", "28", "Dr. Wilson"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.exams_table)

        # Generate PDF button
        button_layout = QHBoxLayout()
        generate_pdf_btn = QPushButton("Generate PDF")
        generate_pdf_btn.clicked.connect(self.generate_pdf)
        generate_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(generate_pdf_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def populate_table(self, data):
        self.exams_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.exams_table.setItem(row, col, QTableWidgetItem(str(value)))

    def search_exams(self):
        search_text = self.search_box.text().lower()
        if not search_text:
            self.populate_table(self.sample_data)
            return
        
        filtered_data = [
            row for row in self.sample_data
            if any(search_text in str(cell).lower() for cell in row)
        ]
        self.populate_table(filtered_data)

    def add_exam(self):
        dialog = AddExamDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_exam = dialog.get_exam_data()
            self.sample_data.append(new_exam)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Exam added successfully!")

    def generate_pdf(self):
        try:
            doc = SimpleDocTemplate("exam_schedule.pdf", pagesize=landscape(letter))
            elements = []

            data = [["Exam Name", "Grade", "Date", "Time", "Venue", 
                    "Room Capacity", "Total Students", "Supervisor Name"]]
            
            for row in range(self.exams_table.rowCount()):
                row_data = []
                for col in range(8):
                    item = self.exams_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            col_widths = [120, 50, 70, 50, 80, 70, 70, 100]
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWHEIGHT', (0, 0), (-1, -1), 30)
            ]))
            
            elements.append(table)
            doc.build(elements)
            QMessageBox.information(self, "Success", "PDF generated successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating PDF: {str(e)}")

class ExamInventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Exam Inventory")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Track and manage exam materials and supplies")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Sufficient Items Card
        sufficient_card = QFrame()
        sufficient_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        sufficient_layout = QVBoxLayout(sufficient_card)
        self.sufficient_value = QLabel("3")
        self.sufficient_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        sufficient_label = QLabel("Sufficient Items")
        sufficient_label.setStyleSheet("color: gray;")
        sufficient_layout.addWidget(self.sufficient_value)
        sufficient_layout.addWidget(sufficient_label)
        stats_layout.addWidget(sufficient_card)
        
        # Items Needing Restock Card
        restock_card = QFrame()
        restock_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        restock_layout = QVBoxLayout(restock_card)
        self.restock_value = QLabel("2")
        self.restock_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        restock_label = QLabel("Items Needing Restock")
        restock_label.setStyleSheet("color: gray;")
        restock_layout.addWidget(self.restock_value)
        restock_layout.addWidget(restock_label)
        stats_layout.addWidget(restock_card)

        # Current Date and Time Card
        datetime_card = QFrame()
        datetime_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        datetime_layout = QVBoxLayout(datetime_card)
        self.datetime_value = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.datetime_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        datetime_label = QLabel("Last Updated")
        datetime_label.setStyleSheet("color: gray;")
        datetime_layout.addWidget(self.datetime_value)
        datetime_layout.addWidget(datetime_label)
        stats_layout.addWidget(datetime_card)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        add_inventory_btn = QPushButton("Add Inventory")
        add_inventory_btn.clicked.connect(self.add_inventory)
        update_inventory_btn = QPushButton("Update Inventory")
        update_inventory_btn.clicked.connect(self.update_selected_item)
        
        for btn in [add_inventory_btn, update_inventory_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
        
        buttons_layout.addWidget(add_inventory_btn)
        buttons_layout.addWidget(update_inventory_btn)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

        # Inventory table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels([
            "Item", "Department", "Available", "Required", "Status", "Cost per Item (₹)", "Total Cost (₹)"
        ])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data
        self.sample_data = [
            ["Answer Booklets A4", "General", "1200", "1500", "Need more", "₹40.00", "₹60,000.00"],
            ["Question Papers (Mathematics)", "Mathematics", "520", "500", "Sufficient", "₹80.00", "₹40,000.00"],
            ["Question Papers (Science)", "Science", "480", "500", "Need more", "₹80.00", "₹40,000.00"],
            ["Exam Hall Seating Cards", "General", "1500", "1500", "Sufficient", "₹20.00", "₹30,000.00"],
            ["Spare Stationery Kits", "General", "100", "150", "Need more", "₹400.00", "₹60,000.00"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.inventory_table)

    def populate_table(self, data):
        self.inventory_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col in [2, 3, 5, 6]:  # Right-align numbers
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.inventory_table.setItem(row, col, item)
            
            # Set status color
            status_item = self.inventory_table.item(row, 4)
            if status_item.text() == "Sufficient":
                status_item.setForeground(QColor("#34A853"))
            else:
                status_item.setForeground(QColor("#FBBC05"))

        # Update stats
        self.update_stats()

    def update_stats(self):
        # Calculate items needing restock
        items_needing_restock = sum(1 for row in self.sample_data if row[4] == "Need more")
        self.restock_value.setText(str(items_needing_restock))
        
        # Calculate sufficient items
        sufficient_items = sum(1 for row in self.sample_data if row[4] == "Sufficient")
        self.sufficient_value.setText(str(sufficient_items))
        
        # Update datetime
        self.datetime_value.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))

    def add_inventory(self):
        dialog = AddInventoryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_item = dialog.get_inventory_data()
            self.sample_data.append(new_item[:7])  # Exclude stock level
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Inventory item added successfully!")

    def update_selected_item(self):
        current_row = self.inventory_table.currentRow()
        if current_row >= 0:
            item_data = [
                self.inventory_table.item(current_row, col).text()
                for col in range(self.inventory_table.columnCount())
            ]
            dialog = AddInventoryDialog(self, item_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                updated_item = dialog.get_inventory_data()
                self.sample_data[current_row] = updated_item[:7]  # Exclude stock level
                self.populate_table(self.sample_data)
                QMessageBox.information(self, "Success", "Inventory item updated successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select an item to update.")

class StudentDetailsDialog(QDialog):
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        self.setWindowTitle("Student Report Card")
        self.setModal(True)
        self.student_data = student_data
        self.setMinimumWidth(700)
        self.setMinimumHeight(750)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Create scroll area for the form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(8)
        form_layout.setContentsMargins(10, 10, 10, 10)

        # Basic Information (pre-filled)
        self.name_edit = QLineEdit(self.student_data[0])
        self.name_edit.setReadOnly(True)
        self.grade_edit = QComboBox()
        self.grade_edit.addItems(["10th", "11th", "12th"])
        self.grade_edit.setCurrentText(self.student_data[1])
        self.grade_edit.setEnabled(False)
        self.roll_no_edit = QLineEdit(self.student_data[2])
        self.roll_no_edit.setReadOnly(True)
        self.exam_score_edit = QSpinBox()
        self.exam_score_edit.setRange(0, 100)
        self.exam_score_edit.setValue(int(self.student_data[3].strip('%')))
        self.exam_score_edit.setEnabled(False)
        self.attendance_edit = QSpinBox()
        self.attendance_edit.setRange(0, 100)
        self.attendance_edit.setValue(int(self.student_data[4].strip('%')))
        self.attendance_edit.setEnabled(False)

        # Additional Information
        self.admission_no = QLineEdit()
        self.academic_year = QLineEdit()
        self.academic_term = QComboBox()
        self.academic_term.addItems(["First Term", "Second Term", "Final Term"])

        # Subject Marks
        subjects_group = QGroupBox("Subject Marks")
        subjects_layout = QFormLayout()
        subjects_layout.setSpacing(5)
        self.subject_marks = {}
        subjects = ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Additional Subject"]
        for subject in subjects:
            spin_box = QSpinBox()
            spin_box.setRange(0, 100)
            spin_box.setValue(0)
            spin_box.valueChanged.connect(self.update_percentage)
            self.subject_marks[subject] = spin_box
            subjects_layout.addRow(f"{subject}:", spin_box)
        subjects_group.setLayout(subjects_layout)

        # Percentage Display
        self.percentage_label = QLabel("Total Percentage: 0%")
        self.percentage_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #1a73e8;")
        subjects_layout.addRow("", self.percentage_label)

        # Extracurricular Activities
        activities_group = QGroupBox("Extracurricular Activities")
        activities_layout = QVBoxLayout()
        activities_layout.setSpacing(5)
        
        # Add Activity Section
        add_activity_layout = QHBoxLayout()
        add_activity_layout.setSpacing(5)
        self.new_activity = QLineEdit()
        self.new_activity.setPlaceholderText("Enter activity name")
        add_btn = QPushButton("Add Activity")
        add_btn.clicked.connect(self.add_activity)
        add_activity_layout.addWidget(self.new_activity)
        add_activity_layout.addWidget(add_btn)
        activities_layout.addLayout(add_activity_layout)
        
        # Activities List
        self.activities_list = QVBoxLayout()
        self.activities_list.setSpacing(5)
        self.activities = {}  # Dictionary to store activity widgets
        activities_layout.addLayout(self.activities_list)
        
        activities_group.setLayout(activities_layout)

        # Achievements
        self.achievements = QTextEdit()
        self.achievements.setPlaceholderText("Enter student's achievements...")
        self.achievements.setMaximumHeight(80)

        # Teacher's Remarks
        self.teacher_remarks = QTextEdit()
        self.teacher_remarks.setPlaceholderText("Enter teacher's remarks...")
        self.teacher_remarks.setMaximumHeight(80)

        # Add all fields to form
        form_layout.addRow("Student Name:", self.name_edit)
        form_layout.addRow("Grade:", self.grade_edit)
        form_layout.addRow("Roll No:", self.roll_no_edit)
        form_layout.addRow("Admission No:", self.admission_no)
        form_layout.addRow("Academic Year:", self.academic_year)
        form_layout.addRow("Academic Term:", self.academic_term)
        form_layout.addRow("Last Exam Score (%):", self.exam_score_edit)
        form_layout.addRow("Attendance (%):", self.attendance_edit)
        form_layout.addRow(subjects_group)
        form_layout.addRow(activities_group)
        form_layout.addRow("Achievements:", self.achievements)
        form_layout.addRow("Teacher's Remarks:", self.teacher_remarks)

        scroll.setWidget(form_widget)
        layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Submit Button
        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        submit_btn.clicked.connect(self.submit_report)
        
        # Generate PDF Button
        generate_pdf_btn = QPushButton("Generate PDF")
        generate_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        generate_pdf_btn.clicked.connect(self.generate_pdf)
        
        # Cancel Button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        cancel_btn.clicked.connect(self.reject)

        # Add buttons to layout with spacing
        button_layout.addStretch()
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(generate_pdf_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)

    def add_activity(self):
        activity_name = self.new_activity.text().strip()
        if activity_name and activity_name not in self.activities:
            activity_layout = QHBoxLayout()
            activity_label = QLabel(activity_name)
            activity_details = QLineEdit()
            activity_details.setPlaceholderText("Enter details")
            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda: self.remove_activity(activity_name))
            
            activity_layout.addWidget(activity_label)
            activity_layout.addWidget(activity_details)
            activity_layout.addWidget(remove_btn)
            
            self.activities[activity_name] = {
                'layout': activity_layout,
                'details': activity_details
            }
            self.activities_list.addLayout(activity_layout)
            self.new_activity.clear()

    def remove_activity(self, activity_name):
        if activity_name in self.activities:
            # Remove the widgets from the layout
            while self.activities[activity_name]['layout'].count():
                item = self.activities[activity_name]['layout'].takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            # Remove the layout itself
            self.activities_list.removeItem(self.activities[activity_name]['layout'])
            # Remove from dictionary
            del self.activities[activity_name]

    def update_percentage(self):
        total_marks = sum(spin.value() for spin in self.subject_marks.values())
        total_subjects = len(self.subject_marks)
        percentage = (total_marks / (total_subjects * 100)) * 100 if total_subjects > 0 else 0
        self.percentage_label.setText(f"Total Percentage: {percentage:.2f}%")

    def submit_report(self):
        # Validate required fields
        if not self.admission_no.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter Admission Number")
            return
        if not self.academic_year.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter Academic Year")
            return
            
        # Check if any subject marks are entered
        if all(spin.value() == 0 for spin in self.subject_marks.values()):
            QMessageBox.warning(self, "Validation Error", "Please enter marks for at least one subject")
            return

        # Collect all data
        data = {
            "name": self.name_edit.text(),
            "grade": self.grade_edit.currentText(),
            "roll_no": self.roll_no_edit.text(),
            "admission_no": self.admission_no.text(),
            "academic_year": self.academic_year.text(),
            "academic_term": self.academic_term.currentText(),
            "exam_score": self.exam_score_edit.value(),
            "attendance": self.attendance_edit.value(),
            "subjects": {subject: spin.value() for subject, spin in self.subject_marks.items()},
            "activities": {name: details['details'].text() for name, details in self.activities.items()},
            "achievements": self.achievements.toPlainText(),
            "teacher_remarks": self.teacher_remarks.toPlainText()
        }
        
        # Calculate total marks and percentage
        total_marks = sum(data["subjects"].values())
        total_subjects = len(data["subjects"])
        percentage = (total_marks / (total_subjects * 100)) * 100 if total_subjects > 0 else 0
        
        # Determine overall grade
        grade = "A+" if percentage >= 90 else "A" if percentage >= 80 else "B+" if percentage >= 70 else "B" if percentage >= 60 else "C+" if percentage >= 50 else "C" if percentage >= 40 else "D" if percentage >= 33 else "F"
        
        data["total_marks"] = total_marks
        data["percentage"] = percentage
        data["overall_grade"] = grade
        
        # Show success message with grade information
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Success")
        msg.setText("Report card submitted successfully!")
        msg.setInformativeText(f"Total Marks: {total_marks}\nPercentage: {percentage:.2f}%\nOverall Grade: {grade}")
        msg.exec()
        
        self.accept()

    def generate_pdf(self):
        try:
            # Validate required fields
            if not self.admission_no.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter Admission Number")
                return
            if not self.academic_year.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter Academic Year")
                return
                
            # Check if any subject marks are entered
            if all(spin.value() == 0 for spin in self.subject_marks.values()):
                QMessageBox.warning(self, "Validation Error", "Please enter marks for at least one subject")
                return

            # Create PDF document with larger size
            doc = SimpleDocTemplate("student_report_card.pdf", pagesize=landscape(letter))
            elements = []
            
            # Add title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=28,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            elements.append(Paragraph("Student Report Card", title_style))
            
            # Add student information
            data = [
                ["Student Name:", self.name_edit.text()],
                ["Grade:", self.grade_edit.currentText()],
                ["Roll No:", self.roll_no_edit.text()],
                ["Admission No:", self.admission_no.text()],
                ["Academic Year:", self.academic_year.text()],
                ["Academic Term:", self.academic_term.currentText()],
                ["Last Exam Score:", f"{self.exam_score_edit.value()}%"],
                ["Attendance:", f"{self.attendance_edit.value()}%"]
            ]
            
            # Create table for student info
            t = Table(data, colWidths=[200, 400])
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 20))
            
            # Add subject marks
            elements.append(Paragraph("Subject Marks", styles['Heading2']))
            subject_data = [["Subject", "Marks"]]
            for subject, spin in self.subject_marks.items():
                subject_data.append([subject, str(spin.value())])
            
            # Add total and percentage row
            total_marks = sum(spin.value() for spin in self.subject_marks.values())
            percentage = (total_marks / (len(self.subject_marks) * 100)) * 100
            subject_data.append(["Total", str(total_marks)])
            subject_data.append(["Percentage", f"{percentage:.2f}%"])
            
            t = Table(subject_data, colWidths=[300, 150])
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (-2, -2), (-1, -1), colors.lightgrey),
                ('FONTNAME', (-2, -2), (-1, -1), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 20))
            
            # Add extracurricular activities
            if self.activities:
                elements.append(Paragraph("Extracurricular Activities", styles['Heading2']))
                activity_data = [["Activity", "Details"]]
                for name, details in self.activities.items():
                    activity_data.append([name, details['details'].text()])
                
                t = Table(activity_data, colWidths=[300, 400])
                t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(t)
                elements.append(Spacer(1, 20))
            
            # Add achievements
            elements.append(Paragraph("Achievements", styles['Heading2']))
            elements.append(Paragraph(self.achievements.toPlainText(), styles['Normal']))
            elements.append(Spacer(1, 20))
            
            # Add teacher's remarks
            elements.append(Paragraph("Teacher's Remarks", styles['Heading2']))
            elements.append(Paragraph(self.teacher_remarks.toPlainText(), styles['Normal']))
            elements.append(Spacer(1, 40))
            
            # Add signature lines
            signature_data = [
                ["Class Teacher's Signature", "Principal's Signature"],
                ["_________________", "_________________"],
                ["Date: _____________", "Date: _____________"]
            ]
            
            t = Table(signature_data, colWidths=[350, 350])
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 14),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(t)
            
            # Build PDF
            doc.build(elements)
            
            # Show success message with file location
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("PDF generated successfully!")
            msg.setInformativeText(f"File saved as: {os.path.abspath('student_report_card.pdf')}")
            msg.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating PDF: {str(e)}")

class StudentExamRecordsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.students_data = []  # Store student data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Student Exam Records")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title)
        
        # Search and Action Buttons Layout
        top_layout = QHBoxLayout()
        
        # Search bar with icon
        search_container = QFrame()
        search_container.setStyleSheet("QFrame { background-color: white; border-radius: 5px; border: 1px solid #ddd; }")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 5, 10, 5)
        
        search_icon = QLabel("🔍")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or roll number...")
        self.search_input.setStyleSheet("QLineEdit { border: none; padding: 5px; }")
        self.search_input.textChanged.connect(self.searchStudents)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)
        
        # Action Buttons
        add_student_btn = QPushButton("Add Student")
        add_student_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_student_btn.clicked.connect(self.showAddStudentDialog)
        
        delete_student_btn = QPushButton("Delete Student")
        delete_student_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        delete_student_btn.clicked.connect(self.deleteStudent)
        
        top_layout.addWidget(search_container, stretch=2)
        top_layout.addWidget(add_student_btn)
        top_layout.addWidget(delete_student_btn)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Changed from 7 to 6 (removed Actions column)
        self.table.setHorizontalHeaderLabels([
            "Student Name", "Grade", "Roll No", "Last Exam Score", "Attendance", "View Details"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Add sample data
        self.loadSampleData()
        
        layout.addLayout(header_layout)
        layout.addLayout(top_layout)
        layout.addWidget(self.table)

    def viewStudentDetails(self, row):
            student_data = [
            self.table.item(row, col).text()
            for col in range(self.table.columnCount() - 1)  # Exclude "View Details" column
            ]
            dialog = StudentDetailsDialog(self, student_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Update the table with the edited details
                for col, value in enumerate(student_data):
                    self.table.setItem(row, col, QTableWidgetItem(value))
                QMessageBox.information(self, "Success", "Student details updated successfully!")

    def searchStudents(self, text):
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text().lower()
            roll_no = self.table.item(row, 2).text().lower()
            should_show = text.lower() in name or text.lower() in roll_no
            self.table.setRowHidden(row, not should_show)

    def showAddStudentDialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.loadSampleData()  # Refresh table

    def deleteStudent(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            student_name = self.table.item(current_row, 0).text()
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete {student_name}'s record?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                self.table.removeRow(current_row)
                QMessageBox.information(self, "Success", "Student record deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a student to delete.")

    def loadSampleData(self):
        # Sample data for the student records table
        self.sample_data = [
            ["Alice Johnson", "10th", "101", "85%", "95%"],
            ["Bob Smith", "9th", "102", "78%", "90%"],
            ["Charlie Brown", "11th", "103", "92%", "98%"],
            ["Daisy Miller", "8th", "104", "88%", "93%"]
        ]
        self.populate_table(self.sample_data)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            # Add student data
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Add View Details button
            view_details_btn = QPushButton("View Details")
            view_details_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            view_details_btn.clicked.connect(lambda checked, row=row: self.viewStudentDetails(row))
            self.table.setCellWidget(row, 5, view_details_btn)

class ExamDepartment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menubar
        menubar = self.menuBar()
        departments_menu = menubar.addMenu("Departments")
        
        # Add Exam Department action
        exam_action = QAction("Exam Department", self)
        departments_menu.addAction(exam_action)
        
        # Add separator and exit action
        departments_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        departments_menu.addAction(exit_action)

        # Create tab buttons
        tab_layout = QHBoxLayout()
        self.tab_buttons = []
        tabs = ["Upcoming Exams", "Previous Papers", "Exam Inventory", "Student Records"]
        
        for i, tab in enumerate(tabs):
            btn = QPushButton(tab)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f2f5;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e4e6e9;
                }
                QPushButton:checked {
                    background-color: #1a73e8;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, index=i: self.switch_tab(index))
            self.tab_buttons.append(btn)
            tab_layout.addWidget(btn)
        
        self.tab_buttons[0].setChecked(True)
        main_layout.addLayout(tab_layout)
        
        # Create stacked widget for pages
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # Create and add pages
        self.upcoming_exams_page = UpcomingExamsPage()
        self.previous_papers_page = PreviousPapersPage()
        self.exam_inventory_page = ExamInventoryPage()
        self.student_exam_records_page = StudentExamRecordsPage()
        
        self.stack.addWidget(self.upcoming_exams_page)
        self.stack.addWidget(self.previous_papers_page)
        self.stack.addWidget(self.exam_inventory_page)
        self.stack.addWidget(self.student_exam_records_page)

    def switch_tab(self, index):
        # Update button states
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)
        
        # Switch page
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExamDepartment()
    window.show()
    sys.exit(app.exec())