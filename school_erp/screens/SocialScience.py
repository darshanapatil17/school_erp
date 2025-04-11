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

        # Initialize speaking_data with sample social science activities
        self.interactive_data = [
            # Nursery to UKG
            ("Community Helpers Talk", "9:00 AM - 10:00 AM", "2024-01-08", "Nursery", "Ms. Emily Parker", "15", "Room 101"),
            ("My Family Presentation", "10:30 AM - 11:30 AM", "2024-01-09", "LKG", "Ms. Sarah Wilson", "18", "Activity Room"),
            ("Neighborhood Walk", "9:00 AM - 10:00 AM", "2024-01-08", "UKG", "Ms. Rachel Green", "20", "Outdoor"),
            
            # Grade 1-3
            ("Local History Project", "10:00 AM - 11:00 AM", "2024-01-08", "Grade 1", "Mr. Robert Clark", "25", "Room 201"),
            ("Cultural Show & Tell", "2:00 PM - 3:00 PM", "2024-01-09", "Grade 2", "Ms. Diana Ross", "23", "Assembly Hall"),
            ("Community Service Day", "9:00 AM - 10:30 AM", "2024-01-10", "Grade 3", "Mr. Michael Scott", "25", "Community Center"),
            
            # Grade 4-6
            ("History Debate", "11:00 AM - 12:30 PM", "2024-01-11", "Grade 4", "Ms. Jennifer Adams", "28", "Room 301"),
            ("Geography Quiz", "2:00 PM - 3:30 PM", "2024-01-12", "Grade 5", "Mr. Thomas Brown", "27", "Geography Lab"),
            ("Civics Mock Parliament", "10:00 AM - 11:30 AM", "2024-01-10", "Grade 6", "Ms. Patricia White", "30", "Auditorium"),
            
            # Grade 7-10
            ("Model United Nations", "1:00 PM - 2:30 PM", "2024-01-11", "Grade 7", "Mr. David Miller", "32", "Conference Room"),
            ("Economics Fair", "3:00 PM - 4:30 PM", "2024-01-12", "Grade 8", "Ms. Sarah Wilson", "30", "Exhibition Hall"),
            ("Political Science Debate", "9:00 AM - 11:00 AM", "2024-01-13", "Grade 9", "Mr. John Smith", "35", "Debate Hall"),
            ("Social Research Symposium", "1:00 PM - 3:00 PM", "2024-01-14", "Grade 10", "Mr. William Turner", "33", "Seminar Room")
        ]
        
        # Sort interactive data by grade
        grade_order = {
            "Nursery": 1, "LKG": 2, "UKG": 3,
            "Grade 1": 4, "Grade 2": 5, "Grade 3": 6,
            "Grade 4": 7, "Grade 5": 8, "Grade 6": 9,
            "Grade 7": 10, "Grade 8": 11, "Grade 9": 12, "Grade 10": 13
        }
        
        self.interactive_data.sort(key=lambda x: (grade_order[x[3]], x[2], x[1]))
        
        # Initialize lesson plan data
        self.lesson_data = [
            # Nursery to UKG
            ("My Family", "Social World - NCERT", "Nursery", "Ms. Emily Parker", "2024-01-08 09:30"),
            ("Community Helpers", "Our Society - NCERT", "LKG", "Ms. Rachel Green", "2024-01-08 10:15"),
            ("My Neighborhood", "Our World - NCERT", "UKG", "Ms. Emma Thompson", "2024-01-08 11:00"),
            
            # Grade 1-3
            ("Local History", "Social Studies 1 - NCERT", "Grade 1", "Mr. Robert Clark", "2024-01-09 09:00"),
            ("Our Culture", "Social Studies 2 - NCERT", "Grade 2", "Ms. Diana Ross", "2024-01-09 10:30"),
            ("Community Life", "Social Studies 3 - NCERT", "Grade 3", "Mr. Michael Scott", "2024-01-09 13:00"),
            
            # Grade 4-6
            ("Indian History", "History 4 - NCERT", "Grade 4", "Ms. Jennifer Adams", "2024-01-10 09:15"),
            ("Geography of India", "Geography 5 - NCERT", "Grade 5", "Mr. Thomas Brown", "2024-01-10 11:00"),
            ("Civics Introduction", "Civics 6 - NCERT", "Grade 6", "Ms. Patricia White", "2024-01-10 14:00"),
            
            # Grade 7-10
            ("Medieval India", "History 7 - NCERT", "Grade 7", "Mr. David Miller", "2024-01-11 09:00"),
            ("World Geography", "Geography 8 - NCERT", "Grade 8", "Ms. Sarah Wilson", "2024-01-11 10:45"),
            ("Democratic Politics", "Civics 9 - NCERT", "Grade 9", "Mr. John Smith", "2024-01-12 09:30"),
            ("Contemporary India", "Social Science 10 - NCERT", "Grade 10", "Mr. William Turner", "2024-01-12 11:15")
        ]
        
        # Sort lesson data by grade
        self.lesson_data.sort(key=lambda x: grade_order[x[2]])
        
        # Create database and load data
        self.create_database()
        self.books_data = []
        
        # Main Widget and Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("Departments")
        header_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        self.main_layout.addWidget(header_label)
        
        # Tab Buttons
        self.tab_layout = QHBoxLayout()
        self.tab_layout.setSpacing(0)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs = ["Textbooks", "Inventory", "Lesson Plans", "Events"]
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
        self.interactive_page = self.create_interactive_page()
        self.lesson_plans_page = self.create_lesson_plans_page()
        self.stack.addWidget(self.textbooks_page)
        self.stack.addWidget(self.interactive_page)
        self.stack.addWidget(self.lesson_plans_page)
        
        # Add placeholder pages for other tabs
        for _ in range(len(self.tabs) - 3):
            placeholder = QWidget()
            self.stack.addWidget(placeholder)

    def create_database(self):
        conn = sqlite3.connect('social_science_textbooks.db')
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
        conn = sqlite3.connect('social_science_textbooks.db')
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
        conn = sqlite3.connect('social_science_textbooks.db')
        cursor = conn.cursor()
        
        sample_data = [
            ("Social Studies Nursery", "NCERT", 30, "Good", QDate.currentDate().toString("yyyy-MM-dd"), 500, "Nursery"),
            ("Environmental Studies LKG", "NCERT", 35, "Need Replacement", QDate.currentDate().toString("yyyy-MM-dd"), 550, "LKG"),
            ("Our World UKG", "NCERT", 40, "Good", QDate.currentDate().toString("yyyy-MM-dd"), 600, "UKG"),
            ("History Grade 1", "NCERT", 42, "Need of Textbook", QDate.currentDate().toString("yyyy-MM-dd"), 650, "Grade 1"),
            ("Geography Grade 2", "NCERT", 38, "Good", QDate.currentDate().toString("yyyy-MM-dd"), 700, "Grade 2"),
            ("Civics Grade 3", "NCERT", 45, "Good", QDate.currentDate().toString("yyyy-MM-dd"), 750, "Grade 3")
        ]
        
        cursor.executemany('''
            INSERT INTO textbooks (title, publisher, quantity, condition, last_inventory, cost_per_book, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)
        
        conn.commit()
        conn.close()

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
            update_btn.clicked.connect(lambda checked, r=row: self.update_book(r))
            
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(4, 4, 4, 4)
            button_layout.addWidget(update_btn)
            
            self.table.setCellWidget(row, len(book), button_widget)

    def search_textbooks(self, text):
        text = text.lower()
        filtered_data = [
            book for book in self.books_data 
            if text in book[0].lower() or  # Title
               text in book[1].lower() or  # Publisher
               text in book[3].lower()     # Condition
        ]
        self.populate_table(filtered_data)

    def filter_by_grade(self, grade):
        if grade == "All Grades":
            self.populate_table(self.books_data)
        else:
            filtered = [book for book in self.books_data if grade in book[0]]
            self.populate_table(filtered)

    def update_book(self, row):
        QMessageBox.information(self, "Update Book", f"Updating book at row {row + 1}")

    def create_textbooks_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 15, 0, 0)
        
        # Title Section
        title_label = QLabel("Social Science Textbooks")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Manage textbooks and reference materials")
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 15px;")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        # Stats Section
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
            container = QWidget()
            container.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                }
            """)
            
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

    def create_interactive_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(5)  # Restored previous spacing
        layout.setContentsMargins(0, 15, 0, 0)  # Restored previous margin
        
        # Title Section
        title_label = QLabel("Inventory")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle_label = QLabel("Maps, models, and physical resources for teaching social sciences")
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 10px;")  # Restored previous margin
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)

        # Sample physical resources data with grades
        physical_data = [
            ("World Maps Collection", "Maps", "Grade 6-8", "25", "2023-08-15", "Available"),
            ("Historical Timeline Charts", "Charts", "Grade 9-10", "15", "2023-07-22", "Available"),
            ("Globe Models", "3D Models", "Grade 4-5", "10", "2023-09-05", "Low Stock"),
            ("Historical Artifacts Replicas", "Educational Models", "Grade 7-8", "8", "2023-06-30", "Low Stock")
        ]

        # Stats Section
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)  # Restored previous spacing
        
        # Calculate real statistics from physical_data
        total_items = sum(int(item[3]) for item in physical_data)
        available_items = sum(int(item[3]) for item in physical_data if item[5] == "Available")
        low_stock_items = sum(int(item[3]) for item in physical_data if item[5] == "Low Stock")
        
        stats = [
            ("Total Items", str(total_items)),
            ("Available Items", str(available_items)),
            ("Low Stock Items", str(low_stock_items))
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
            content_widget.setStyleSheet("""
                QWidget {
                    background-color: transparent;
                    border: none;
                }
            """)
            
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(15, 15, 15, 15)  # Restored previous padding
            content_layout.setSpacing(5)  # Restored previous spacing
            
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
        layout.addSpacing(5)  # Restored previous spacing

        # Top Controls Section
        controls = QHBoxLayout()
        controls.setContentsMargins(0, 0, 0, 0)
        controls.setSpacing(0)  # Removed spacing between controls
        
        # Left side: Search and Grade selector
        left_controls = QHBoxLayout()
        left_controls.setSpacing(0)  # Removed spacing between search and grade
        left_controls.setContentsMargins(0, 0, 0, 0)
        
        # Search Bar
        search = QLineEdit()
        search.setPlaceholderText("Search inventory...")
        search.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        search.textChanged.connect(self.search_inventory)
        left_controls.addWidget(search)
        
        # Grade Filter
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["All Grades", "Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        self.grade_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                min-width: 120px;
                font-size: 14px;
            }
        """)
        self.grade_combo.currentTextChanged.connect(self.filter_inventory_by_grade)
        left_controls.addWidget(self.grade_combo)
        
        controls.addLayout(left_controls)
        
        # Right side: Action Buttons
        controls.addStretch()
        
        # Button container with minimal spacing
        button_container = QHBoxLayout()
        button_container.setSpacing(5)  # Restored previous spacing
        
        # Order Supplies Button
        order_btn = QPushButton("Order Supplies")
        order_btn.setStyleSheet("""
            QPushButton {
                background-color: #198754;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #157347;
            }
        """)
        order_btn.clicked.connect(self.order_inventory_supplies)
        button_container.addWidget(order_btn)
        
        # Delete Inventory Button
        delete_btn = QPushButton("Delete Inventory")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #bb2d3b;
            }
        """)
        delete_btn.clicked.connect(self.delete_inventory)
        button_container.addWidget(delete_btn)
        
        # Add Inventory Button
        add_btn = QPushButton("Add Inventory")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
        """)
        add_btn.clicked.connect(self.add_inventory)
        button_container.addWidget(add_btn)
        
        controls.addLayout(button_container)
        layout.addLayout(controls)
        layout.addSpacing(5)  # Restored previous spacing

        # Physical Resources Section
        physical_label = QLabel("Physical Resources")
        physical_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 5px;")
        layout.addWidget(physical_label)

        # Physical Resources Table
        self.physical_table = QTableWidget()
        self.physical_table.setStyleSheet("""
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
        
        physical_headers = ["Resource Name", "Type", "Grade", "Quantity", "Last Ordered", "Status", "Actions"]
        self.physical_table.setColumnCount(len(physical_headers))
        self.physical_table.setHorizontalHeaderLabels(physical_headers)
        
        self.physical_table.setRowCount(len(physical_data))
        for row, item in enumerate(physical_data):
            for col, value in enumerate(item):
                table_item = QTableWidgetItem(str(value))
                if col == 5:  # Status column
                    if value == "Available":
                        table_item.setForeground(Qt.GlobalColor.darkGreen)
                    elif value == "Low Stock":
                        table_item.setForeground(Qt.GlobalColor.darkRed)
                self.physical_table.setItem(row, col, table_item)
            
            # Add Update button
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
            update_btn.clicked.connect(lambda checked, r=row: self.update_inventory_item(r))
            
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(4, 4, 4, 4)
            button_layout.addWidget(update_btn)
            
            self.physical_table.setCellWidget(row, len(physical_headers) - 1, button_widget)
        
        # Set column widths
        self.physical_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Resource Name
        self.physical_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        self.physical_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Grade
        self.physical_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Quantity
        self.physical_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Last Ordered
        self.physical_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Status
        self.physical_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Actions
        self.physical_table.setColumnWidth(6, 120)  # Set Actions column width
        
        layout.addWidget(self.physical_table)
        
        return page

    def update_inventory_item(self, row):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Inventory Item")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout(dialog)
        
        # Get current values
        name = self.physical_table.item(row, 0).text()
        type_ = self.physical_table.item(row, 1).text()
        grade = self.physical_table.item(row, 2).text()
        quantity = self.physical_table.item(row, 3).text()
        status = self.physical_table.item(row, 5).text()
        
        # Create input fields
        name_input = QLineEdit(name)
        type_input = QLineEdit(type_)
        grade_input = QComboBox()
        grade_input.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        grade_input.setCurrentText(grade)
        quantity_input = QSpinBox()
        quantity_input.setRange(0, 1000)
        quantity_input.setValue(int(quantity))
        status_input = QComboBox()
        status_input.addItems(["Available", "Low Stock"])
        status_input.setCurrentText(status)
        
        # Add fields to form
        layout.addRow("Resource Name:", name_input)
        layout.addRow("Type:", type_input)
        layout.addRow("Grade:", grade_input)
        layout.addRow("Quantity:", quantity_input)
        layout.addRow("Status:", status_input)
        
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
        
        def save_changes():
            self.physical_table.item(row, 0).setText(name_input.text())
            self.physical_table.item(row, 1).setText(type_input.text())
            self.physical_table.item(row, 2).setText(grade_input.currentText())
            self.physical_table.item(row, 3).setText(str(quantity_input.value()))
            self.physical_table.item(row, 5).setText(status_input.currentText())
            
            # Update status color
            status_item = self.physical_table.item(row, 5)
            if status_input.currentText() == "Available":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            else:
                status_item.setForeground(Qt.GlobalColor.darkRed)
            
            dialog.accept()
            QMessageBox.information(self, "Success", "Inventory item updated successfully!")
        
        save_btn.clicked.connect(save_changes)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()

    def create_lesson_plans_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 15, 0, 0)
        
        # Title Section
        title_label = QLabel("Social Science Lesson Plans")
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
        
        # Set column widths
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

    def add_book(self):
        dialog = AddBookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            conn = sqlite3.connect('social_science_textbooks.db')
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

    def generate_order_pdf(self, order_data, total_cost):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Order PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_name:
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'
            
            doc = SimpleDocTemplate(
                file_name,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            elements = []
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30
            )
            
            elements.append(Paragraph("Social Science Textbook Order Summary", title_style))
            elements.append(Spacer(1, 12))
            
            date_style = styles["Normal"]
            date_style.fontSize = 12
            elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", date_style))
            elements.append(Spacer(1, 12))
            
            table_data = [["Title", "Quantity", "Cost per Book (₹)", "Total Cost (₹)"]]
            for item in order_data:
                table_data.append([
                    item['title'],
                    str(item['quantity']),
                    str(item['cost_per_book']),
                    str(item['cost_per_book'] * item['quantity'])
                ])
            
            table = Table(table_data, colWidths=[4*inch, 1*inch, 1.5*inch, 1.5*inch])
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
            
            total_paragraph = Paragraph(
                f"<para fontSize=14><b>Total Order Cost: ₹{total_cost:,}</b></para>",
                styles["Normal"]
            )
            elements.append(total_paragraph)
            
            doc.build(elements)
            
            QMessageBox.information(
                self,
                "Success",
                f"PDF has been generated and saved to:\n{file_name}"
            )

    def populate_lesson_table(self, data):
        self.lesson_table.setRowCount(len(data))
        for row, lesson in enumerate(data):
            for col, value in enumerate(lesson):
                item = QTableWidgetItem(str(value))
                self.lesson_table.setItem(row, col, item)
            
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
            
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(4, 4, 4, 4)
            button_layout.addWidget(update_btn)
            
            self.lesson_table.setCellWidget(row, len(lesson), button_widget)

    def search_lesson_plans(self, text):
        text = text.lower()
        filtered_data = [
            lesson for lesson in self.lesson_data 
            if text in lesson[0].lower() or  # Title
               text in lesson[1].lower() or  # Resource Book
               text in lesson[3].lower()     # Teacher
        ]
        self.populate_lesson_table(filtered_data)

    def filter_lesson_plans(self, grade):
        if grade == "All Grades":
            self.populate_lesson_table(self.lesson_data)
        else:
            filtered = [lesson for lesson in self.lesson_data if lesson[2] == grade]
            self.populate_lesson_table(filtered)

    def create_lesson_plan(self):
        QMessageBox.information(self, "Create Lesson Plan", "Create new lesson plan functionality will be implemented soon.")

    def delete_lesson_plan(self):
        row = self.lesson_table.currentRow()
        if row >= 0:
            reply = QMessageBox.question(
                self, 
                "Confirm Delete",
                "Are you sure you want to delete this lesson plan?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.lesson_data.pop(row)
                self.populate_lesson_table(self.lesson_data)
                QMessageBox.information(self, "Success", "Lesson plan deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a lesson plan to delete")

    def update_lesson_plan(self, row):
        QMessageBox.information(self, "Update Lesson Plan", f"Updating lesson plan at row {row + 1}")

    def search_inventory(self, text):
        text = text.lower()
        for row in range(self.physical_table.rowCount()):
            should_show = False
            for col in range(self.physical_table.columnCount()):
                item = self.physical_table.item(row, col)
                if item and text in item.text().lower():
                    should_show = True
                    break
            self.physical_table.setRowHidden(row, not should_show)

    def filter_inventory_by_grade(self, grade):
        if grade == "All Grades":
            for row in range(self.physical_table.rowCount()):
                self.physical_table.setRowHidden(row, False)
        else:
            for row in range(self.physical_table.rowCount()):
                item = self.physical_table.item(row, 2)  # Grade column
                if item:
                    # Show row if grade matches exactly or is part of the grade range
                    grade_text = item.text()
                    should_show = False
                    
                    # Check for exact match
                    if grade == grade_text:
                        should_show = True
                    # Check for grade ranges (e.g., "Grade 6-8")
                    elif "-" in grade_text:
                        start_grade, end_grade = grade_text.split("-")
                        if "Grade" in grade:
                            current_grade = int(grade.replace("Grade ", ""))
                            start_num = int(start_grade.replace("Grade ", ""))
                            end_num = int(end_grade)
                            should_show = start_num <= current_grade <= end_num
                    
                    self.physical_table.setRowHidden(row, not should_show)
            
            # Update statistics based on filtered data
            visible_items = sum(1 for row in range(self.physical_table.rowCount()) 
                              if not self.physical_table.isRowHidden(row))
            visible_available = sum(1 for row in range(self.physical_table.rowCount())
                                  if not self.physical_table.isRowHidden(row) and 
                                  self.physical_table.item(row, 5).text() == "Available")
            visible_low_stock = sum(1 for row in range(self.physical_table.rowCount())
                                  if not self.physical_table.isRowHidden(row) and 
                                  self.physical_table.item(row, 5).text() == "Low Stock")

    def delete_inventory(self):
        selected_rows = set(item.row() for item in self.physical_table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select items to delete")
            return
            
        reply = QMessageBox.question(
            self, 
            "Confirm Delete",
            f"Are you sure you want to delete {len(selected_rows)} selected items?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for row in sorted(selected_rows, reverse=True):
                self.physical_table.removeRow(row)
            QMessageBox.information(self, "Success", "Selected items deleted successfully!")

    def add_inventory(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Inventory Item")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout(dialog)
        
        # Create input fields
        name_input = QLineEdit()
        type_input = QLineEdit()
        grade_input = QComboBox()
        grade_input.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        quantity_input = QSpinBox()
        quantity_input.setRange(1, 1000)
        status_input = QComboBox()
        status_input.addItems(["Available", "Low Stock"])
        
        # Add fields to form
        layout.addRow("Resource Name:", name_input)
        layout.addRow("Type:", type_input)
        layout.addRow("Grade:", grade_input)
        layout.addRow("Quantity:", quantity_input)
        layout.addRow("Status:", status_input)
        
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
        
        def save_new_item():
            if not name_input.text() or not type_input.text():
                QMessageBox.warning(dialog, "Warning", "Please fill in all fields")
                return
            
            row = self.physical_table.rowCount()
            self.physical_table.insertRow(row)
            
            # Add the new item to the table
            self.physical_table.setItem(row, 0, QTableWidgetItem(name_input.text()))
            self.physical_table.setItem(row, 1, QTableWidgetItem(type_input.text()))
            self.physical_table.setItem(row, 2, QTableWidgetItem(grade_input.currentText()))
            self.physical_table.setItem(row, 3, QTableWidgetItem(str(quantity_input.value())))
            self.physical_table.setItem(row, 4, QTableWidgetItem(QDate.currentDate().toString("yyyy-MM-dd")))
            
            status_item = QTableWidgetItem(status_input.currentText())
            if status_input.currentText() == "Available":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            else:
                status_item.setForeground(Qt.GlobalColor.darkRed)
            self.physical_table.setItem(row, 5, status_item)
            
            # Add Update button
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
            update_btn.clicked.connect(lambda checked, r=row: self.update_inventory_item(r))
            
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(4, 4, 4, 4)
            button_layout.addWidget(update_btn)
            
            self.physical_table.setCellWidget(row, 6, button_widget)
            
            dialog.accept()
            QMessageBox.information(self, "Success", "New inventory item added successfully!")
        
        save_btn.clicked.connect(save_new_item)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()

    def order_inventory_supplies(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Order Supplies")
        dialog.setModal(True)
        dialog.setMinimumWidth(800)
        
        layout = QVBoxLayout(dialog)
        
        # Add table showing items that need ordering
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
        
        headers = ["Resource Name", "Current Quantity", "Status", "Order Quantity", "Unit Cost (₹)", "Total Cost (₹)"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        # Get items that need ordering (Low Stock)
        low_stock_items = []
        for row in range(self.physical_table.rowCount()):
            status = self.physical_table.item(row, 5).text()
            if status == "Low Stock":
                name = self.physical_table.item(row, 0).text()
                quantity = int(self.physical_table.item(row, 3).text())
                low_stock_items.append((name, quantity))
        
        table.setRowCount(len(low_stock_items))
        order_quantities = []
        unit_costs = []
        total_cost = 0
        
        for row, (name, quantity) in enumerate(low_stock_items):
            # Resource Name
            table.setItem(row, 0, QTableWidgetItem(name))
            # Current Quantity
            table.setItem(row, 1, QTableWidgetItem(str(quantity)))
            # Status
            status_item = QTableWidgetItem("Low Stock")
            status_item.setForeground(Qt.GlobalColor.darkRed)
            table.setItem(row, 2, status_item)
            
            # Order Quantity SpinBox
            quantity_spin = QSpinBox()
            quantity_spin.setRange(1, 1000)
            quantity_spin.setValue(max(20 - quantity, 1))  # Suggest order quantity
            order_quantities.append(quantity_spin)
            
            # Unit Cost SpinBox
            cost_spin = QSpinBox()
            cost_spin.setRange(1, 100000)
            cost_spin.setValue(500)  # Default unit cost
            cost_spin.setPrefix("₹")
            unit_costs.append(cost_spin)
            
            def update_total(row):
                quantity = order_quantities[row].value()
                cost = unit_costs[row].value()
                total = quantity * cost
                table.setItem(row, 5, QTableWidgetItem(f"₹{total:,}"))
                
                # Update grand total
                grand_total = sum(
                    order_quantities[r].value() * unit_costs[r].value()
                    for r in range(len(low_stock_items))
                )
                total_label.setText(f"Total Order Cost: ₹{grand_total:,}")
            
            quantity_spin.valueChanged.connect(lambda _, r=row: update_total(r))
            cost_spin.valueChanged.connect(lambda _, r=row: update_total(r))
            
            # Add SpinBoxes to table
            table.setCellWidget(row, 3, quantity_spin)
            table.setCellWidget(row, 4, cost_spin)
            
            # Initial total for this item
            total = quantity_spin.value() * cost_spin.value()
            table.setItem(row, 5, QTableWidgetItem(f"₹{total:,}"))
            total_cost += total
        
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, 6):
            table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(table)
        
        # Total cost label
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
        
        # Buttons
        button_box = QHBoxLayout()
        
        generate_pdf_btn = QPushButton("Generate Order PDF")
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
            file_name, _ = QFileDialog.getSaveFileName(
                dialog,
                "Save Order PDF",
                "",
                "PDF Files (*.pdf);;All Files (*)"
            )
            
            if file_name:
                if not file_name.endswith('.pdf'):
                    file_name += '.pdf'
                
                doc = SimpleDocTemplate(
                    file_name,
                    pagesize=letter,
                    rightMargin=72,
                    leftMargin=72,
                    topMargin=72,
                    bottomMargin=72
                )
                
                elements = []
                styles = getSampleStyleSheet()
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30
                )
                elements.append(Paragraph("Social Science Department - Supply Order", title_style))
                elements.append(Spacer(1, 12))
                
                # Date
                date_style = styles["Normal"]
                date_style.fontSize = 12
                elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", date_style))
                elements.append(Spacer(1, 12))
                
                # Order details table
                table_data = [["Resource Name", "Order Quantity", "Unit Cost (₹)", "Total Cost (₹)"]]
                
                grand_total = 0
                for row in range(table.rowCount()):
                    name = table.item(row, 0).text()
                    quantity = order_quantities[row].value()
                    unit_cost = unit_costs[row].value()
                    total = quantity * unit_cost
                    grand_total += total
                    
                    table_data.append([
                        name,
                        str(quantity),
                        f"₹{unit_cost:,}",
                        f"₹{total:,}"
                    ])
                
                pdf_table = Table(table_data, colWidths=[4*inch, 1.2*inch, 1.2*inch, 1.2*inch])
                pdf_table.setStyle(TableStyle([
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
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                elements.append(pdf_table)
                elements.append(Spacer(1, 20))
                
                # Grand Total
                elements.append(Paragraph(
                    f"<para fontSize=14><b>Grand Total: ₹{grand_total:,}</b></para>",
                    styles["Normal"]
                ))
                
                doc.build(elements)
                
                QMessageBox.information(
                    dialog,
                    "Success",
                    f"Order PDF has been generated and saved to:\n{file_name}"
                )
                dialog.accept()
        
        generate_pdf_btn.clicked.connect(generate_pdf)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
