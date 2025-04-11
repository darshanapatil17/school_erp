import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
                           QWidget, QLineEdit, QComboBox, QHeaderView, QStackedWidget,
                           QDialog, QFormLayout, QSpinBox, QMessageBox, QDateEdit,
                           QFileDialog)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect, QDate, QDateTime
from datetime import datetime
import sqlite3
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Book")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Simple input fields
        self.title = QLineEdit()
        self.publisher = QLineEdit()
        self.quantity = QSpinBox()
        self.quantity.setRange(1, 1000)
        
        self.condition = QComboBox()
        self.condition.addItems(["Good", "Need Replacement", "Need of Textbook"])
        
        self.grade = QComboBox()
        self.grade.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        
        # Add fields to form
        layout.addRow("Title:", self.title)
        layout.addRow("Grade:", self.grade)
        layout.addRow("Publisher:", self.publisher)
        layout.addRow("Quantity:", self.quantity)
        layout.addRow("Condition:", self.condition)
        
        # Buttons
        buttons = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)
        
        self.setLayout(layout)
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize speaking_data with more classes, sorted by grade
        self.speaking_data = [
            # Nursery Classes
            ("Phonics Practice", "9:00 AM - 10:00 AM", "2024-01-08", "Nursery", "Ms. Emily Parker", "15", "Room 101"),
            ("Story Time", "10:30 AM - 11:30 AM", "2024-01-09", "Nursery", "Ms. Sarah Wilson", "18", "Library"),
            
            # LKG Classes
            ("Vocabulary Building", "9:00 AM - 10:00 AM", "2024-01-08", "LKG", "Ms. Rachel Green", "20", "Room 102"),
            ("Show and Tell", "11:00 AM - 12:00 PM", "2024-01-09", "LKG", "Mr. James Wilson", "22", "Activity Room"),
            
            # UKG Classes
            ("Basic Conversation", "10:00 AM - 11:00 AM", "2024-01-08", "UKG", "Ms. Emma Thompson", "25", "Room 103"),
            ("Rhyme Time", "2:00 PM - 3:00 PM", "2024-01-09", "UKG", "Ms. Lisa Brown", "23", "Music Room"),
            
            # Grade 1-3
            ("Reading Club", "9:00 AM - 10:30 AM", "2024-01-10", "Grade 1", "Mr. Robert Clark", "25", "Library"),
            ("Story Telling", "11:00 AM - 12:30 PM", "2024-01-11", "Grade 2", "Ms. Diana Ross", "28", "Room 201"),
            ("Word Games", "2:00 PM - 3:30 PM", "2024-01-12", "Grade 3", "Mr. Michael Scott", "27", "Activity Room"),
            
            # Grade 4-6
            ("Public Speaking", "10:00 AM - 11:30 AM", "2024-01-10", "Grade 4", "Ms. Jennifer Adams", "30", "Auditorium"),
            ("Debate Club Junior", "1:00 PM - 2:30 PM", "2024-01-11", "Grade 5", "Mr. Thomas Brown", "32", "Room 301"),
            ("Speech Practice", "3:00 PM - 4:30 PM", "2024-01-12", "Grade 6", "Ms. Patricia White", "30", "Conference Room"),
            
            # Grade 7-8
            ("Advanced Debate", "9:00 AM - 11:00 AM", "2024-01-13", "Grade 7", "Mr. David Miller", "35", "Debate Hall"),
            ("Presentation Skills", "1:00 PM - 3:00 PM", "2024-01-14", "Grade 8", "Ms. Sarah Wilson", "33", "Auditorium"),
            
            # Grade 9-10
            ("Model UN Prep", "10:00 AM - 12:00 PM", "2024-01-15", "Grade 9", "Mr. John Smith", "38", "Conference Room"),
            ("Leadership Speaking", "2:00 PM - 4:00 PM", "2024-01-16", "Grade 10", "Mr. William Turner", "36", "Seminar Hall")
        ]
        
        # Sort speaking data by grade and then by date and time
        grade_order = {
            "Nursery": 1, "LKG": 2, "UKG": 3,
            "Grade 1": 4, "Grade 2": 5, "Grade 3": 6,
            "Grade 4": 7, "Grade 5": 8, "Grade 6": 9,
            "Grade 7": 10, "Grade 8": 11, "Grade 9": 12, "Grade 10": 13
        }
        
        self.speaking_data.sort(key=lambda x: (grade_order[x[3]], x[2], x[1]))
        
        # Create database and load data
        self.create_database()
        self.books_data = []
        
        # Main Widget and Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)  # Reduce overall spacing
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("Departments")
        header_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        self.main_layout.addWidget(header_label)
        
        # Tab Buttons
        self.tab_layout = QHBoxLayout()
        self.tab_layout.setSpacing(0)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs = ["Textbooks", "Speaking Skill Classes", "Lesson Plans", "Events"]
        self.tab_buttons = []
        
        for tab in self.tabs:
            tab_button = QPushButton(tab)
            tab_button.clicked.connect(lambda checked, t=tab: self.switch_tab(t))
            self.tab_buttons.append(tab_button)
            self.tab_layout.addWidget(tab_button)
        
        self.update_tab_styles("Textbooks")
        self.main_layout.addLayout(self.tab_layout)
        
        # Content Area
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        
        # Load initial data
        self.load_books_data()
        
        # Create pages
        self.textbooks_page = self.create_textbooks_page()
        self.speaking_page = self.create_speaking_page()
        self.lesson_plans_page = self.create_lesson_plans_page()
        self.stack.addWidget(self.textbooks_page)
        self.stack.addWidget(self.speaking_page)
        self.stack.addWidget(self.lesson_plans_page)
        
        # Add placeholder pages for other tabs
        for _ in range(len(self.tabs) - 3):
            placeholder = QWidget()
            self.stack.addWidget(placeholder)

    def create_textbooks_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 15, 0, 0)
        
        # Title Section
        title_label = QLabel("English Textbooks")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Manage textbooks and reference materials")
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 15px;")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        # Stats Section with clean boxes
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        total_books = sum(book[2] for book in self.books_data)
        available_books = sum(book[2] for book in self.books_data if book[3] == "Good")
        need_books = sum(book[2] for book in self.books_data if book[3] == "Need of Textbook")
        need_replacement = sum(book[2] for book in self.books_data if book[3] == "Need Replacement")
        
        stats = [
            ("Total Textbooks", str(total_books)),
            ("Available Textbooks", str(available_books)),
            ("Need of Textbooks", str(need_books)),
            ("Need Replacement", str(need_replacement))
        ]
        
        for title, value in stats:
            # Create outer container with border
            container = QWidget()
            container.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                }
            """)
            
            # Create inner widget for content without border
            content_widget = QWidget()
            content_widget.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border: none;
                }
            """)
            
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(15, 15, 15, 15)
            content_layout.setSpacing(5)
            
            # Value label without border
            value_label = QLabel(value)
            value_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0d6efd;
                    background: transparent;
                    border: none;
                }
            """)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Title label without border
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 14px;
                    background: transparent;
                    border: none;
                }
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Add labels to content layout
            content_layout.addWidget(value_label)
            content_layout.addWidget(title_label)
            
            # Add content widget to container
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.addWidget(content_widget)
            
            stats_layout.addWidget(container)
        
        layout.addLayout(stats_layout)
        
        # Search and Controls Section
        controls = QHBoxLayout()
        
        # Left side: Search and Grade selector
        left_controls = QHBoxLayout()
        
        search = QLineEdit()
        search.setPlaceholderText("Search textbooks...")
        search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        search.textChanged.connect(self.search_textbooks)
        left_controls.addWidget(search)
        
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["All Grades", "Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        self.grade_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 120px;
            }
        """)
        self.grade_combo.currentTextChanged.connect(self.filter_by_grade)
        left_controls.addWidget(self.grade_combo)
        
        controls.addLayout(left_controls)
        
        # Right side: Action Buttons
        controls.addStretch()
        
        add_btn = QPushButton("Add Book")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
        """)
        add_btn.clicked.connect(self.add_book)
        controls.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete Book")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
        """)
        delete_btn.clicked.connect(self.delete_book)
        controls.addWidget(delete_btn)
        
        order_btn = QPushButton("Order Supplies")
        order_btn.setStyleSheet("""
            QPushButton {
                background-color: #198754;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
        """)
        order_btn.clicked.connect(self.order_supplies)
        controls.addWidget(order_btn)
        
        layout.addLayout(controls)
        
        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        headers = ["Title", "Publisher", "Quantity", "Condition", "Last Inventory", "Actions"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.populate_table(self.books_data)
        layout.addWidget(self.table)
        
        return page

    def create_speaking_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 15, 0, 0)
        
        # Title Section
        title_label = QLabel("Speaking Skills Training")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Activities like debates, public speaking, and elocution contests")
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        # Search and Controls Section
        controls = QHBoxLayout()
        
        # Left side: Search and Grade selector
        left_controls = QHBoxLayout()
        
        search = QLineEdit()
        search.setPlaceholderText("Search activities...")
        search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        search.textChanged.connect(self.search_speaking_classes)
        left_controls.addWidget(search)
        
        self.speaking_grade_combo = QComboBox()
        self.speaking_grade_combo.addItems(["All Grades", "Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        self.speaking_grade_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 120px;
            }
        """)
        self.speaking_grade_combo.currentTextChanged.connect(self.filter_speaking_by_grade)
        left_controls.addWidget(self.speaking_grade_combo)
        
        controls.addLayout(left_controls)
        
        # Right side: Action Buttons
        controls.addStretch()
        
        add_btn = QPushButton("Add Class")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
        """)
        add_btn.clicked.connect(self.add_speaking_class)
        controls.addWidget(add_btn)
        
        delete_btn = QPushButton("Delete Class")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
        """)
        delete_btn.clicked.connect(self.delete_speaking_class)
        controls.addWidget(delete_btn)
        
        layout.addLayout(controls)
        
        # Table
        self.speaking_table = QTableWidget()
        self.speaking_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        # Set up table structure
        headers = ["Activity", "Schedule", "Date", "Grade", "Teacher", "Total Students", "Venue", "Actions"]
        self.speaking_table.setColumnCount(len(headers))
        self.speaking_table.setHorizontalHeaderLabels(headers)
        self.speaking_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.populate_speaking_table(self.speaking_data)
        layout.addWidget(self.speaking_table)
        return page

    def create_lesson_plans_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 15, 0, 0)
        
        # Initialize lesson plan data with comprehensive entries
        self.lesson_data = [
            # Nursery to UKG
            ("Phonics and Letter Recognition", "Early Learning English - NCERT", "Nursery", "Ms. Emily Parker", "2024-01-08 09:30"),
            ("Basic Vocabulary Development", "My First Words - NCERT", "LKG", "Ms. Rachel Green", "2024-01-08 10:15"),
            ("Simple Sentences Formation", "Basic English - NCERT", "UKG", "Ms. Emma Thompson", "2024-01-08 11:00"),
            
            # Grade 1-3
            ("Reading and Comprehension Basics", "English Reader 1 - NCERT", "Grade 1", "Mr. Robert Clark", "2024-01-09 09:00"),
            ("Grammar Fundamentals", "English Grammar 2 - NCERT", "Grade 2", "Ms. Diana Ross", "2024-01-09 10:30"),
            ("Creative Writing Introduction", "English Workbook 3 - NCERT", "Grade 3", "Mr. Michael Scott", "2024-01-09 13:00"),
            
            # Grade 4-6
            ("Advanced Reading Skills", "English Reader 4 - NCERT", "Grade 4", "Ms. Jennifer Adams", "2024-01-10 09:15"),
            ("Intermediate Grammar", "English Grammar 5 - NCERT", "Grade 5", "Mr. Thomas Brown", "2024-01-10 11:00"),
            ("Essay Writing Skills", "English Composition 6 - NCERT", "Grade 6", "Ms. Patricia White", "2024-01-10 14:00"),
            
            # Grade 7-8
            ("Literature Analysis", "English Literature 7 - NCERT", "Grade 7", "Mr. David Miller", "2024-01-11 09:00"),
            ("Advanced Writing Skills", "English Composition 8 - NCERT", "Grade 8", "Ms. Sarah Wilson", "2024-01-11 10:45"),
            
            # Grade 9-10
            ("Advanced Literature Study", "English Literature 9 - NCERT", "Grade 9", "Mr. John Smith", "2024-01-12 09:30"),
            ("Comprehensive English", "English Complete 10 - NCERT", "Grade 10", "Mr. William Turner", "2024-01-12 11:15")
        ]
        
        # Sort lesson data by grade
        grade_order = {
            "Nursery": 1, "LKG": 2, "UKG": 3,
            "Grade 1": 4, "Grade 2": 5, "Grade 3": 6,
            "Grade 4": 7, "Grade 5": 8, "Grade 6": 9,
            "Grade 7": 10, "Grade 8": 11, "Grade 9": 12, "Grade 10": 13
        }
        
        self.lesson_data.sort(key=lambda x: grade_order[x[2]])  # Updated index for grade
        
        # Title Section
        title_label = QLabel("Lesson Plans & Syllabi")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Manage curriculum materials and teaching plans")
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 20px;")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        # Search and Controls Section
        controls = QHBoxLayout()
        
        # Left side: Search and Grade selector
        left_controls = QHBoxLayout()
        
        search = QLineEdit()
        search.setPlaceholderText("Search lesson plans...")
        search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                min-width: 300px;
            }
        """)
        search.textChanged.connect(self.search_lesson_plans)
        left_controls.addWidget(search)
        
        self.lesson_grade_combo = QComboBox()
        self.lesson_grade_combo.addItems(["All Grades", "Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        self.lesson_grade_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 120px;
            }
        """)
        self.lesson_grade_combo.currentTextChanged.connect(self.filter_lesson_plans)
        left_controls.addWidget(self.lesson_grade_combo)
        
        controls.addLayout(left_controls)
        
        # Right side: Action Buttons
        controls.addStretch()
        
        create_btn = QPushButton("Create Lesson Plan")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
        """)
        create_btn.clicked.connect(self.create_lesson_plan)
        controls.addWidget(create_btn)
        
        delete_btn = QPushButton("Delete Lesson Plan")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
            }
        """)
        delete_btn.clicked.connect(self.delete_lesson_plan)
        controls.addWidget(delete_btn)
        
        layout.addLayout(controls)
        
        # Table
        self.lesson_table = QTableWidget()
        self.lesson_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        headers = ["Title", "Resource Book", "Grade", "Teacher", "Last Updated", "Actions"]
        self.lesson_table.setColumnCount(len(headers))
        self.lesson_table.setHorizontalHeaderLabels(headers)
        
        # Set column widths without the serial number column
        self.lesson_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Title
        self.lesson_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Resource Book
        self.lesson_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Grade
        self.lesson_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Teacher
        self.lesson_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Last Updated
        self.lesson_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Actions
        
        self.lesson_table.setColumnWidth(5, 100)  # Actions column
        
        self.populate_lesson_table(self.lesson_data)
        layout.addWidget(self.lesson_table)
        
        return page

    def switch_tab(self, tab_name):
        self.update_tab_styles(tab_name)
        index = self.tabs.index(tab_name)
        self.stack.setCurrentIndex(index)

    def update_tab_styles(self, active_tab):
        for button in self.tab_buttons:
            if button.text() == active_tab:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #0d6efd;
                        color: white;
                        border: none;
                        padding: 15px 32px;
                        font-size: 14px;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        border: none;
                        padding: 15px 32px;
                        font-size: 14px;
                    }
                """)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, book in enumerate(data):
            for col, value in enumerate(book):
                item = QTableWidgetItem(str(value))
                if col == 3 and value == "Good":
                    item.setForeground(Qt.GlobalColor.green)
                self.table.setItem(row, col, item)
            
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 4px;
                }
            """)
            update_btn.clicked.connect(lambda checked, r=row: self.update_book(r))
            self.table.setCellWidget(row, 5, update_btn)

    def filter_by_grade(self, grade):
        if grade == "All Grades":
            self.populate_table(self.books_data)
        else:
            filtered = [book for book in self.books_data if grade in book[0]]
            self.populate_table(filtered)

    def add_book(self):
        dialog = AddBookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            conn = sqlite3.connect('textbooks.db')
            cursor = conn.cursor()
            
            new_book = (
                f"{dialog.grade.currentText()} {dialog.title.text()}",
                dialog.publisher.text(),
                dialog.quantity.value(),
                dialog.condition.currentText(),
                QDate.currentDate().toString("yyyy-MM-dd"),
                500,  # Default cost per book
                dialog.grade.currentText()
            )
            
            cursor.execute('''
                INSERT INTO textbooks (title, publisher, quantity, condition, last_inventory, cost_per_book, grade)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', new_book)
            
            conn.commit()
            conn.close()
            
            self.load_books_data()
            self.populate_table(self.books_data)
            QMessageBox.information(self, "Success", "Book added successfully!")

    def delete_book(self):
        row = self.table.currentRow()
        if row >= 0:
            reply = QMessageBox.question(self, "Confirm Delete", 
                                       "Are you sure you want to delete this book?",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.books_data.pop(row)
                self.populate_table(self.books_data)
                QMessageBox.information(self, "Success", "Book deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a book to delete")

    def update_book(self, row):
        QMessageBox.information(self, "Update Book", f"Updating book at row {row + 1}")

    def order_supplies(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Order Supplies")
        dialog.setModal(True)
        dialog.setMinimumWidth(800)
        
        layout = QVBoxLayout(dialog)
        
        # Add table showing books that need replacement
        table = QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        headers = ["Title", "Current Quantity", "Condition", "Cost per Book (₹)", "Order Quantity", "Total Cost (₹)"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Filter books that need replacement
        needs_replacement = [book for book in self.books_data if book[3] != "Good"]
        table.setRowCount(len(needs_replacement))
        
        order_quantities = []
        total_cost = 0
        
        for row, book in enumerate(needs_replacement):
            table.setItem(row, 0, QTableWidgetItem(book[0]))
            table.setItem(row, 1, QTableWidgetItem(str(book[2])))
            table.setItem(row, 2, QTableWidgetItem(book[3]))
            
            cost_per_book = book[5] if len(book) > 5 else 500
            table.setItem(row, 3, QTableWidgetItem(str(cost_per_book)))
            
            quantity_spin = QSpinBox()
            quantity_spin.setRange(1, 1000)
            quantity_spin.setValue(book[2])
            
            total_item_cost = cost_per_book * quantity_spin.value()
            total_cost += total_item_cost
            
            total_cost_item = QTableWidgetItem(str(total_item_cost))
            table.setItem(row, 5, total_cost_item)
            
            def update_total(value, row=row, cost=cost_per_book):
                new_total = value * cost
                table.setItem(row, 5, QTableWidgetItem(str(new_total)))
                grand_total = sum(int(table.item(r, 5).text()) for r in range(table.rowCount()))
                total_label.setText(f"Total Order Cost: ₹{grand_total:,}")
            
            quantity_spin.valueChanged.connect(update_total)
            order_quantities.append(quantity_spin)
            table.setCellWidget(row, 4, quantity_spin)
        
        layout.addWidget(table)
        
        total_label = QLabel(f"Total Order Cost: ₹{total_cost:,}")
        total_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #198754;
                padding: 10px;
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin: 10px 0;
            }
        """)
        layout.addWidget(total_label)
        
        button_box = QHBoxLayout()
        generate_pdf_btn = QPushButton("Generate PDF")
        generate_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #198754;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #157347;
            }
        """)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5c636a;
            }
        """)
        
        button_box.addWidget(generate_pdf_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        def generate_pdf():
            order_data = []
            total_cost = 0
            for i, book in enumerate(needs_replacement):
                quantity = order_quantities[i].value()
                if quantity > 0:
                    cost_per_book = book[5] if len(book) > 5 else 500
                    item_cost = quantity * cost_per_book
                    total_cost += item_cost
                    order_data.append({
                        'title': book[0],
                        'quantity': quantity,
                        'cost_per_book': cost_per_book
                    })
            
            if order_data:
                self.generate_order_pdf(order_data, total_cost)
                dialog.accept()
            else:
                QMessageBox.warning(dialog, "Error", "No items selected for order")
        
        generate_pdf_btn.clicked.connect(generate_pdf)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()

    def populate_speaking_table(self, data):
        self.speaking_table.setRowCount(len(data))
        for row, item in enumerate(data):
            for col in range(7):  # Populate first 7 columns
                item_text = str(item[col])
                table_item = QTableWidgetItem(item_text)
                self.speaking_table.setItem(row, col, table_item)
            
            # Add update button with improved styling
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 14px;
                    width: 100%;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            update_btn.setFixedHeight(35)
            update_btn.clicked.connect(lambda checked, r=row: self.update_speaking_class(r))
            
            # Create a widget to hold the button with proper spacing
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(4, 4, 4, 4)
            button_layout.addWidget(update_btn)
            
            self.speaking_table.setCellWidget(row, 7, button_widget)
            
        # Adjust column widths
        self.speaking_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Activity
        self.speaking_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Schedule
        self.speaking_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Date
        self.speaking_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Grade
        self.speaking_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Teacher
        self.speaking_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Total Students
        self.speaking_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)  # Venue
        self.speaking_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # Actions
        self.speaking_table.setColumnWidth(7, 120)  # Set fixed width for Actions column

    def filter_speaking_by_grade(self, grade):
        if grade == "All Grades":
            self.populate_speaking_table(self.speaking_data)
        else:
            filtered_data = [item for item in self.speaking_data if item[3] == grade]
            if filtered_data:
                self.populate_speaking_table(filtered_data)
                self.show_weekly_schedule(filtered_data, grade)
            else:
                QMessageBox.information(self, "No Classes", f"No classes found for {grade}")

    def show_weekly_schedule(self, classes, grade):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Weekly Schedule - {grade}")
        dialog.setModal(True)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Title section
        current_date = QDate.currentDate()
        start_of_week = current_date.addDays(-(current_date.dayOfWeek() - 1))
        end_of_week = start_of_week.addDays(6)
        
        title = QLabel(f"Schedule for Week of {start_of_week.toString('MMM d')} - {end_of_week.toString('MMM d, yyyy')}")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Table
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Day", "Activity", "Time", "Teacher", "Total Students", "Venue"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Filter and sort classes for current week
        current_week_classes = []
        for c in classes:
            class_date = QDate.fromString(c[2], "yyyy-MM-dd")
            if start_of_week <= class_date <= end_of_week:
                current_week_classes.append((class_date.toString("dddd"), c[0], c[1], c[4], c[5], c[6]))
        
        current_week_classes.sort(key=lambda x: (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(x[0]), x[2]))
        
        # Populate table
        table.setRowCount(len(current_week_classes))
        for row, data in enumerate(current_week_classes):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)
        
        layout.addWidget(table)
        
        # Generate PDF button
        pdf_btn = QPushButton("Generate Complete Schedule PDF")
        pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #198754;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        pdf_btn.clicked.connect(lambda: self.generate_schedule_pdf(classes, grade))
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(pdf_btn)
        layout.addLayout(button_layout)
        
        dialog.exec()

    def generate_schedule_pdf(self, classes, grade):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Schedule PDF",
            f"speaking_schedule_{grade.lower().replace(' ', '_')}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            try:
                from reportlab.lib import colors
                from reportlab.lib.pagesizes import letter
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                
                doc = SimpleDocTemplate(file_name, pagesize=letter)
                elements = []
                styles = getSampleStyleSheet()
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30
                )
                elements.append(Paragraph(f"Speaking Skills Schedule - {grade}", title_style))
                elements.append(Paragraph(f"Generated on {QDate.currentDate().toString('MMMM d, yyyy')}", styles["Normal"]))
                elements.append(Spacer(1, 20))
                
                # Sort classes by date and time
                sorted_classes = sorted(classes, key=lambda x: (x[2], x[1]))
                
                # Table data
                data = [["Date", "Day", "Activity", "Time", "Teacher", "Venue"]]
                for c in sorted_classes:
                    class_date = QDate.fromString(c[2], "yyyy-MM-dd")
                    data.append([
                        class_date.toString("MMM d, yyyy"),
                        class_date.toString("dddd"),
                        c[0],  # Activity
                        c[1],  # Time
                        c[4],  # Teacher
                        c[6]   # Venue
                    ])
                
                # Create table
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                
                elements.append(table)
                doc.build(elements)
                
                QMessageBox.information(self, "Success", "PDF generated successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to generate PDF: {str(e)}")

    def search_speaking_classes(self, text):
        text = text.lower()
        filtered_data = [
            item for item in self.speaking_data 
            if text in item[0].lower() or  # Activity
               text in item[3].lower() or  # Grade
               text in item[4].lower() or  # Teacher
               text in item[6].lower()     # Venue
        ]
        self.populate_speaking_table(filtered_data)

    def create_database(self):
        conn = sqlite3.connect('textbooks.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS textbooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                publisher TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                condition TEXT NOT NULL,
                last_inventory TEXT NOT NULL,
                cost_per_book INTEGER NOT NULL,
                grade TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def load_books_data(self):
        conn = sqlite3.connect('textbooks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT title, publisher, quantity, condition, last_inventory, cost_per_book, grade FROM textbooks')
        books = cursor.fetchall()
        conn.close()
        
        if not books:  # If no data exists, insert sample data
            self.insert_sample_data()
            return self.load_books_data()
        
        self.books_data = []
        for book in books:
            self.books_data.append((
                book[0],  # title
                book[1],  # publisher
                book[2],  # quantity
                book[3],  # condition
                book[4],  # last_inventory
                book[5],  # cost_per_book
            ))
        return self.books_data

    def insert_sample_data(self):
        conn = sqlite3.connect('textbooks.db')
        cursor = conn.cursor()
        
        sample_data = [
            ("English Nursery", "Oxford University Press", 30, "Good", QDate.currentDate().toString("yyyy-MM-dd"), 500, "Nursery"),
            ("English LKG", "Oxford University Press", 35, "Need Replacement", QDate.currentDate().toString("yyyy-MM-dd"), 550, "LKG"),
            ("English UKG", "Oxford University Press", 40, "Good", QDate.currentDate().toString("yyyy-MM-dd"), 600, "UKG"),
            ("English Grade 1", "Oxford University Press", 42, "Need of Textbook", QDate.currentDate().toString("yyyy-MM-dd"), 650, "Grade 1")
        ]
        
        cursor.executemany('''
            INSERT INTO textbooks (title, publisher, quantity, condition, last_inventory, cost_per_book, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)
        
        conn.commit()
        conn.close()

    def generate_order_pdf(self, order_data, total_cost):
        # Ask user where to save the PDF
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Order PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_name:
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'
            
            # Create the PDF document
            doc = SimpleDocTemplate(
                file_name,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Container for the 'Flowable' objects
            elements = []
            
            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30
            )
            
            # Add the title
            elements.append(Paragraph("Textbook Order Summary", title_style))
            elements.append(Spacer(1, 12))
            
            # Add date
            date_style = styles["Normal"]
            date_style.fontSize = 12
            elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", date_style))
            elements.append(Spacer(1, 12))
            
            # Prepare the table data
            table_data = [["Title", "Quantity", "Cost per Book (₹)", "Total Cost (₹)"]]
            for item in order_data:
                table_data.append([
                    item['title'],
                    str(item['quantity']),
                    str(item['cost_per_book']),
                    str(item['cost_per_book'] * item['quantity'])
                ])
            
            # Create the table
            table = Table(table_data, colWidths=[4*inch, 1*inch, 1.5*inch, 1.5*inch])
            
            # Add style to the table
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))
            
            # Add total cost
            total_paragraph = Paragraph(
                f"<para fontSize=14><b>Total Order Cost: ₹{total_cost:,}</b></para>",
                styles["Normal"]
            )
            elements.append(total_paragraph)
            
            # Build the PDF
            doc.build(elements)
            
            QMessageBox.information(
                self,
                "Success",
                f"PDF has been generated and saved to:\n{file_name}"
            )

    def update_speaking_class(self, row):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Speaking Class")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Get current values
        current_data = [
            self.speaking_table.item(row, i).text() if i != 7 else None
            for i in range(8)
        ]
        
        # Create input fields with current values
        activity = QLineEdit(current_data[0])
        
        time_layout = QHBoxLayout()
        start_time = QComboBox()
        end_time = QComboBox()
        times = [f"{h:02d}:00" for h in range(7, 19)]  # 7 AM to 6 PM
        current_times = current_data[1].split(" - ")
        
        for t in times:
            start_time.addItem(t)
            end_time.addItem(t)
        
        start_time.setCurrentText(current_times[0])
        end_time.setCurrentText(current_times[1])
        
        time_layout.addWidget(start_time)
        time_layout.addWidget(QLabel(" - "))
        time_layout.addWidget(end_time)
        
        date = QDateEdit()
        date.setDisplayFormat("yyyy-MM-dd")
        date.setDate(QDate.fromString(current_data[2], "yyyy-MM-dd"))
        date.setCalendarPopup(True)
        
        grade = QComboBox()
        grade.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        grade.setCurrentText(current_data[3])
        
        teacher = QLineEdit(current_data[4])
        
        total_students = QSpinBox()
        total_students.setRange(1, 100)
        total_students.setValue(int(current_data[5]))
        
        venue = QLineEdit(current_data[6])
        
        # Add fields to form
        form_layout.addRow("Activity:", activity)
        form_layout.addRow("Time:", time_layout)
        form_layout.addRow("Date:", date)
        form_layout.addRow("Grade:", grade)
        form_layout.addRow("Teacher:", teacher)
        form_layout.addRow("Total Students:", total_students)
        form_layout.addRow("Venue:", venue)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        button_box = QHBoxLayout()
        update_btn = QPushButton("Update")
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: black;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        
        button_box.addWidget(update_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        update_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Format time
            start = start_time.currentText()
            end = end_time.currentText()
            time_str = f"{start} - {end}"
            
            # Update class data
            updated_class = (
                activity.text(),
                time_str,
                date.date().toString("yyyy-MM-dd"),
                grade.currentText(),
                teacher.text(),
                str(total_students.value()),
                venue.text()
            )
            
            # Validate data
            if all(updated_class):
                # Update in speaking_data
                self.speaking_data[row] = updated_class
                self.speaking_data.sort(key=lambda x: (x[2], x[1]))  # Sort by date, then time
                
                # Refresh table
                self.populate_speaking_table(self.speaking_data)
                QMessageBox.information(self, "Success", "Class updated successfully!")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields")

    def search_textbooks(self, text):
        text = text.lower()
        filtered_data = [
            book for book in self.books_data 
            if text in book[0].lower() or  # Title
               text in book[1].lower() or  # Publisher
               text in book[3].lower()     # Condition
        ]
        self.populate_table(filtered_data)

    def add_speaking_class(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Class")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Create input fields
        activity = QLineEdit()
        
        time_layout = QHBoxLayout()
        start_time = QComboBox()
        end_time = QComboBox()
        times = [f"{h:02d}:00" for h in range(7, 19)]  # 7 AM to 6 PM
        for t in times:
            start_time.addItem(t)
            end_time.addItem(t)
        time_layout.addWidget(start_time)
        time_layout.addWidget(QLabel(" - "))
        time_layout.addWidget(end_time)
        
        date = QDateEdit()
        date.setDisplayFormat("yyyy-MM-dd")
        date.setDate(QDate.currentDate())
        date.setCalendarPopup(True)
        
        grade = QComboBox()
        grade.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        
        teacher = QLineEdit()
        total_students = QSpinBox()
        total_students.setRange(1, 100)
        venue = QLineEdit()
        
        # Add fields to form
        form_layout.addRow("Activity:", activity)
        form_layout.addRow("Time:", time_layout)
        form_layout.addRow("Date:", date)
        form_layout.addRow("Grade:", grade)
        form_layout.addRow("Teacher:", teacher)
        form_layout.addRow("Total Students:", total_students)
        form_layout.addRow("Venue:", venue)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        save_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Format time
            start = start_time.currentText()
            end = end_time.currentText()
            time_str = f"{start} - {end}"
            
            # Create new class data
            new_class = (
                activity.text(),
                time_str,
                date.date().toString("yyyy-MM-dd"),
                grade.currentText(),
                teacher.text(),
                str(total_students.value()),
                venue.text()
            )
            
            # Validate data
            if all(new_class):
                self.speaking_data.append(new_class)
                self.speaking_data.sort(key=lambda x: (x[2], x[1]))  # Sort by date, then time
                self.populate_speaking_table(self.speaking_data)
                QMessageBox.information(self, "Success", "New class added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields")

    def delete_speaking_class(self):
        row = self.speaking_table.currentRow()
        if row >= 0:
            reply = QMessageBox.question(self, "Confirm Delete", 
                                       "Are you sure you want to delete this class?",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.speaking_data.pop(row)
                self.populate_speaking_table(self.speaking_data)
                QMessageBox.information(self, "Success", "Class deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a class to delete")

    def populate_lesson_table(self, data):
        self.lesson_table.setRowCount(len(data))
        for row, item in enumerate(data):
            for col, value in enumerate(item):
                table_item = QTableWidgetItem(str(value))
                self.lesson_table.setItem(row, col, table_item)
            
            # Add update button with clean, full-width styling
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 14px;
                    width: 100%;
                    height: 35px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            update_btn.clicked.connect(lambda checked, r=row: self.update_lesson_plan(r))
            
            # Create a widget to hold the button without margins
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setSpacing(0)
            button_layout.addWidget(update_btn)
            
            self.lesson_table.setCellWidget(row, len(item), button_widget)
        
        # Set column widths without the serial number column
        self.lesson_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Title
        self.lesson_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Resource Book
        self.lesson_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Grade
        self.lesson_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Teacher
        self.lesson_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Last Updated
        self.lesson_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Actions
        
        self.lesson_table.setColumnWidth(5, 100)  # Actions column

    def filter_lesson_plans(self, grade):
        if grade == "All Grades":
            self.populate_lesson_table(self.lesson_data)
        else:
            filtered_data = [item for item in self.lesson_data if item[2] == grade]
            if filtered_data:
                self.populate_lesson_table(filtered_data)
                self.show_grade_lessons(grade, filtered_data)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("No Lessons")
                msg.setText(f"No lesson plans found for {grade}")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()

    def show_grade_lessons(self, grade, lessons):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Lesson Plans - {grade}")
        dialog.setModal(True)
        dialog.resize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Title section
        title = QLabel(f"Lesson Plans for {grade}")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #0d6efd;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title)
        
        # Stats section
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        # Calculate stats
        total_lessons = len(lessons)
        current_month = QDate.currentDate().toString("MMMM")
        month_lessons = len([l for l in lessons if current_month in l[4]])  # Updated index for last updated
        
        stats = [
            ("Total Lesson Plans", str(total_lessons)),
            ("This Month's Plans", str(month_lessons)),
            ("Teacher Count", str(len(set(l[3] for l in lessons))))  # Updated index for teacher
        ]
        
        for title, value in stats:
        container = QWidget()
            container.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                }
            """)
            
            content_widget = QWidget()
            content_widget.setStyleSheet("background-color: transparent; border: none;")
            
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(15, 15, 15, 15)
            content_layout.setSpacing(5)
            
            value_label = QLabel(value)
            value_label.setStyleSheet("""
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #0d6efd;
                    background: transparent;
                    border: none;
                }
            """)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 14px;
                    background: transparent;
                    border: none;
                }
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            content_layout.addWidget(value_label)
            content_layout.addWidget(title_label)
            
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.addWidget(content_widget)
            
            stats_layout.addWidget(container)
        
        layout.addLayout(stats_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("Search in this grade's lessons...")
        search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                min-width: 300px;
            }
        """)
        search.textChanged.connect(lambda text: self.filter_grade_lessons(text, table, lessons))
        search_layout.addWidget(search)
        search_layout.addStretch()
        layout.addLayout(search_layout)
        
        # Table
        table = QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        headers = ["Title", "Resource Book", "Teacher", "Last Updated", "Actions"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Title
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Resource Book
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Teacher
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Last Updated
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Actions
        
        table.setColumnWidth(4, 100)  # Actions column
        
        # Populate table
        table.setRowCount(len(lessons))
        for row, lesson in enumerate(lessons):
            # Display data excluding grade
            display_data = [lesson[0], lesson[1], lesson[3], lesson[4]]  # Updated indices
            
            for col, value in enumerate(display_data):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)
            
            # Add update button with clean, full-width styling
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 14px;
                    width: 100%;
                    height: 35px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            
            lesson_row = row
            update_btn.clicked.connect(
                lambda checked, r=lesson_row, l=lessons: 
                self.update_lesson_plan_from_dialog(r, l, table, table.parent())
            )
            
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setSpacing(0)
            button_layout.addWidget(update_btn)
            
            table.setCellWidget(row, len(display_data), button_widget)
        
        layout.addWidget(table)
        
        # Add close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5c636a;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        dialog.exec()

    def filter_grade_lessons(self, text, table, lessons):
        text = text.lower()
        filtered_data = [
            lesson for lesson in lessons 
            if text in lesson[0].lower() or  # Title
               text in lesson[1].lower() or  # Resource Book
               text in lesson[3].lower()     # Teacher
        ]
        
        table.setRowCount(len(filtered_data))
        for row, lesson in enumerate(filtered_data):
            display_data = [lesson[0], lesson[1], lesson[3], lesson[4]]  # Updated indices
            
            for col, value in enumerate(display_data):
                item = QTableWidgetItem(str(value))
                table.setItem(row, col, item)
            
            # Add update button with clean, full-width styling
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 14px;
                    width: 100%;
                    height: 35px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            
            lesson_row = row
            update_btn.clicked.connect(
                lambda checked, r=lesson_row, l=filtered_data: 
                self.update_lesson_plan_from_dialog(r, l, table, table.parent())
            )
            
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setSpacing(0)
            button_layout.addWidget(update_btn)
            
            table.setCellWidget(row, len(display_data), button_widget)

    def update_lesson_plan_from_dialog(self, row, lessons, table, parent_dialog):
        dialog = QDialog(parent_dialog)
        dialog.setWindowTitle("Update Lesson Plan")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        
        # Title
        title_label = QLabel("Update Lesson Plan")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #0d6efd;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        
        # Get current values
        current_data = lessons[row]
        
        # Create input fields with current values
        title = QLineEdit(current_data[0])  # Updated index
        title.setStyleSheet("padding: 8px;")
        
        resource_book = QLineEdit(current_data[1])  # Updated index
        resource_book.setStyleSheet("padding: 8px;")
        
        teacher = QLineEdit(current_data[3])  # Updated index
        teacher.setStyleSheet("padding: 8px;")
        
        # Add fields to form
        form_layout.addRow("Title:", title)
        form_layout.addRow("Resource Book:", resource_book)
        form_layout.addRow("Teacher:", teacher)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        button_box = QHBoxLayout()
        update_btn = QPushButton("Update")
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 100px;
            }
        """)
        
        button_box.addStretch()
        button_box.addWidget(update_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        update_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update lesson plan data
            updated_lesson = (
                title.text(),
                resource_book.text(),
                current_data[2],  # Keep original grade
                teacher.text(),
                QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
            )
            
            # Validate data
            if all(updated_lesson):
                # Update in main data
                main_index = next(i for i, item in enumerate(self.lesson_data) 
                                if item[0] == current_data[0] and item[2] == current_data[2])
                self.lesson_data[main_index] = updated_lesson
                
                # Update in filtered data and table
                lessons[row] = updated_lesson
                
                # Update table display
                display_data = [updated_lesson[0], updated_lesson[1], updated_lesson[3], updated_lesson[4]]
                for col, value in enumerate(display_data):
                    table.setItem(row, col, QTableWidgetItem(str(value)))
                
                QMessageBox.information(dialog, "Success", "Lesson plan updated successfully!")
            else:
                QMessageBox.warning(dialog, "Error", "Please fill in all fields")

    def update_lesson_plan(self, row):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Lesson Plan")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        
        # Title
        title_label = QLabel("Update Lesson Plan")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #0d6efd;
                padding: 10px 0;
            }
        """)
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        
        # Get current values
        current_data = self.lesson_data[row]
        
        # Create input fields with current values
        title = QLineEdit(current_data[0])  # Updated index
        title.setStyleSheet("padding: 8px;")
        
        resource_book = QLineEdit(current_data[1])  # Updated index
        resource_book.setStyleSheet("padding: 8px;")
        
        grade = QComboBox()
        grade.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        grade.setCurrentText(current_data[2])  # Updated index
        grade.setStyleSheet("padding: 8px;")
        
        teacher = QLineEdit(current_data[3])  # Updated index
        teacher.setStyleSheet("padding: 8px;")
        
        # Add fields to form
        form_layout.addRow("Title:", title)
        form_layout.addRow("Resource Book:", resource_book)
        form_layout.addRow("Grade:", grade)
        form_layout.addRow("Teacher:", teacher)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        button_box = QHBoxLayout()
        update_btn = QPushButton("Update")
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-size: 14px;
                min-width: 100px;
            }
        """)
        
        button_box.addStretch()
        button_box.addWidget(update_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        update_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update lesson plan data
            updated_lesson = (
                title.text(),
                resource_book.text(),
                grade.currentText(),
                teacher.text(),
                QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
            )
            
            # Validate data
            if all(updated_lesson):
                self.lesson_data[row] = updated_lesson
                self.populate_lesson_table(self.lesson_data)
                QMessageBox.information(self, "Success", "Lesson plan updated successfully!")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields")

    def create_lesson_plan(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Lesson Plan")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        form_layout = QFormLayout()
        
        # Create input fields
        title = QLineEdit()
        resource_book = QLineEdit()
        
        grade = QComboBox()
        grade.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        
        teacher = QLineEdit()
        
        # Add fields to form
        form_layout.addRow("Title:", title)
        form_layout.addRow("Resource Book:", resource_book)
        form_layout.addRow("Grade:", grade)
        form_layout.addRow("Teacher:", teacher)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
            }
        """)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)
        
        save_btn.clicked.connect(dialog.accept)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Create new lesson plan data without serial number
            new_lesson = (
                title.text(),
                resource_book.text(),
                grade.currentText(),
                teacher.text(),
                QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")
            )
            
            # Validate data
            if all(new_lesson):
                self.lesson_data.append(new_lesson)
                self.populate_lesson_table(self.lesson_data)
                QMessageBox.information(self, "Success", "Lesson plan created successfully!")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields")

    def delete_lesson_plan(self):
        row = self.lesson_table.currentRow()
        if row >= 0:
            reply = QMessageBox.question(self, "Confirm Delete", 
                                       "Are you sure you want to delete this lesson plan?",
                                       QMessageBox.StandardButton.Yes | 
                                       QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.lesson_data.pop(row)
                # Update serial numbers
                self.lesson_data = [(str(i+1),) + tuple(data[1:]) for i, data in enumerate(self.lesson_data)]
                self.populate_lesson_table(self.lesson_data)
                QMessageBox.information(self, "Success", "Lesson plan deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a lesson plan to delete")

    def search_lesson_plans(self, text):
        text = text.lower()
        filtered_data = [
            item for item in self.lesson_data 
            if text in item[1].lower() or  # Title
               text in item[2].lower() or  # Resource Book
               text in item[4].lower()     # Teacher
        ]
        self.populate_lesson_table(filtered_data)

if __name__ == "__main__":
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
