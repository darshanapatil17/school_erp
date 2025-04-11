"""
Discipline Department Module
This module implements the Discipline Department interface for the School ERP system.
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
                           QWidget, QLineEdit, QComboBox, QHeaderView, QStackedWidget,
                           QDialog, QFormLayout, QSpinBox, QMessageBox, QDateEdit,
                           QFileDialog, QFrame, QGroupBox, QScrollArea)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect, QDate, QDateTime
import matplotlib
matplotlib.use('qtagg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

class MplCanvas(FigureCanvasQTAgg):
    """Custom matplotlib canvas for embedding plots in PyQt6"""
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class DisciplineDepartmentPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discipline Department")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QWidget {
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background: white;
                font-size: 14px;
            }
            QTableWidget {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 14px;
            }
            QLabel {
                color: #212529;
                font-size: 14px;
            }
            QStackedWidget {
                background: transparent;
                border: none;
                margin: 20px;
            }
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title
        title = QLabel("Discipline Department")
        title.setFont(QFont("Segoe UI", 40, QFont.Weight.Bold))
        title.setStyleSheet("color: #212529; margin: 20px;")
        main_layout.addWidget(title)

        # Create navigation bar
        nav_bar = QHBoxLayout()
        nav_bar.setSpacing(0)
        nav_bar.setContentsMargins(0, 0, 0, 0)
        nav_buttons = [
            ("Behavior Records", 0),
            ("Attendance Reports", 1),
            ("Incident Reports", 2),
            ("Student Records", 3)
        ]

        for text, index in nav_buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #6c757d;
                    border: none;
                    border-radius: 0;
                    padding: 8px 16px;
                    font-size: 14px;
                    border-right: 1px solid #dee2e6;
                    margin: 0;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                }
            """)
            btn.clicked.connect(lambda checked, idx=index: self.switch_tab(idx))
            nav_bar.addWidget(btn)

        # Add the last button without right border
        nav_bar.itemAt(nav_bar.count() - 1).widget().setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6c757d;
                border: none;
                border-radius: 0;
                padding: 8px 16px;
                font-size: 14px;
                margin: 0;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)

        # Create a container for the navigation bar
        nav_container = QWidget()
        nav_container.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
                margin: 0 20px;
            }
        """)
        nav_container.setLayout(nav_bar)
        main_layout.addWidget(nav_container)

        # Create stacked widget for content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_behavior_policy_tab())
        self.stacked_widget.addWidget(self.create_attendance_tab())
        self.stacked_widget.addWidget(self.create_conflict_resolution_tab())
        self.stacked_widget.addWidget(self.create_human_resource_tab())

        # Connect tab change to update navigation buttons
        self.stacked_widget.currentChanged.connect(self.update_nav_buttons)
        main_layout.addWidget(self.stacked_widget)

    def switch_tab(self, index):
        """Smoothly switch between tabs"""
        # Create animation
        animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        animation.setDuration(300)  # 300ms animation
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Get current and target geometries
        current_rect = self.stacked_widget.geometry()
        target_rect = current_rect
        
        # Set up animation
        animation.setStartValue(current_rect)
        animation.setEndValue(target_rect)
        
        # Start animation and switch tab
        animation.start()
        self.stacked_widget.setCurrentIndex(index)

    def update_nav_buttons(self, index):
        """Update navigation buttons style based on current tab"""
        nav_buttons = self.findChildren(QPushButton)
        for i, btn in enumerate(nav_buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0d6efd;
                        color: white;
                        border: none;
                        border-radius: 0;
                        padding: 8px 16px;
                        font-size: 14px;
                        border-right: 1px solid #dee2e6;
                        margin: 0;
                    }
                    QPushButton:hover {
                        background-color: #0b5ed7;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #6c757d;
                        border: none;
                        border-radius: 0;
                        padding: 8px 16px;
                        font-size: 14px;
                        border-right: 1px solid #dee2e6;
                        margin: 0;
                    }
                    QPushButton:hover {
                        background-color: #e9ecef;
                    }
                """)
        # Update the last button without right border
        nav_buttons[-1].setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6c757d;
                border: none;
                border-radius: 0;
                padding: 8px 16px;
                font-size: 14px;
                margin: 0;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)

    def create_behavior_policy_tab(self):
        """Create the Behavior Policy tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Search and Action Buttons Section
        action_section = QHBoxLayout()
        
        # Search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search policies...")
        search_box.setMinimumWidth(400)  # Increased width

        # Create Policy button
        create_btn = QPushButton("Create Policy")
        create_btn.setIcon(QIcon("assets/icons/add.png"))

        action_section.addWidget(search_box)
        action_section.addStretch()
        action_section.addWidget(create_btn)
        layout.addLayout(action_section)

        # Policy Cards
        policies = [
            ("General Conduct Policy", "Guidelines for appropriate behavior in classrooms, corridors, and common areas"),
            ("Academic Integrity Policy", "Rules regarding plagiarism, cheating, and other forms of academic dishonesty"),
            ("Uniform Code", "Requirements for proper school uniform and appearance standards"),
            ("Anti-Bullying Policy", "Zero-tolerance approach to bullying in any form including cyberbullying"),
            ("Digital Device Usage Policy", "Regulations for using smartphones and other devices on campus")
        ]

        for title, description in policies:
            card = self.create_policy_card(title, description)
            layout.addWidget(card)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_policy_card(self, title, description):
        """Create a policy card widget"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                margin: 5px 0;
            }
            QFrame:hover {
                border-color: #0d6efd;
            }
        """)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #212529;")

        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #6c757d;")
        desc_label.setWordWrap(True)

        # View Details button
        view_btn = QPushButton("View Details")
        view_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #0d6efd;
                border: none;
                text-align: left;
                padding: 5px 0;
            }
            QPushButton:hover {
                color: #0b5ed7;
            }
        """)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(view_btn)
        card.setLayout(layout)
        return card

    def create_attendance_tab(self):
        """Create the Attendance Issues tab"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Search and Filter Section
        search_section = QHBoxLayout()
        
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search students...")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 300px;
            }
        """)

        grade_filter = QComboBox()
        grade_filter.addItems(["All Grades", "Grade 8", "Grade 9", "Grade 10"])
        grade_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 150px;
            }
        """)

        search_section.addWidget(search_box)
        search_section.addWidget(grade_filter)
        search_section.addStretch()
        layout.addLayout(search_section)

        # Table
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Grade", "Total Lectures", "Absent Lectures", 
            "Attendance %", "Status", "Update", "View"
        ])
        table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        # Sample data
        data = [
            ["Grade 9A", "50", "5", "90%", "Good"],
            ["Grade 8B", "50", "12", "76%", "Warning"],
            ["Grade 10C", "50", "8", "84%", "Average"],
        ]

        table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)
            
            # Add buttons
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background: #2196F3;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background: #1976D2;
                }
            """)
            
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background: #388E3C;
                }
            """)
            view_btn.clicked.connect(lambda checked, r=row: self.show_attendance_details(r))

            table.setCellWidget(row, 5, update_btn)
            table.setCellWidget(row, 6, view_btn)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)

        tab.setLayout(layout)
        return tab

    def show_attendance_details(self, row):
        """Show detailed attendance information in a dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Student Attendance Details")
        dialog.setMinimumWidth(800)
        dialog.setMinimumHeight(600)
        dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 24px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Student Info Section
        info_group = QGroupBox("Student Information")
        info_layout = QFormLayout()
        info_layout.setSpacing(10)
        
        info_layout.addRow("Grade:", QLabel(f"Grade {9+row}A"))
        info_layout.addRow("Total Lectures:", QLabel("50"))
        info_layout.addRow("Absent Lectures:", QLabel("5"))
        info_layout.addRow("Attendance Percentage:", QLabel("90%"))
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Attendance Graph
        graph_group = QGroupBox("Attendance Distribution")
        graph_layout = QVBoxLayout()
        graph_layout.setContentsMargins(10, 20, 10, 10)
        
        canvas = MplCanvas(self, width=8, height=4, dpi=100)
        
        # Sample data for pie chart
        labels = ['Class Lectures', 'Guest Lectures', 'Events', 'Present']
        sizes = [2, 1, 2, 45]
        colors = ['#ff9f43', '#ee5253', '#0abde3', '#2ed573']
        
        canvas.axes.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        canvas.axes.axis('equal')
        
        graph_layout.addWidget(canvas)
        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        
        report_btn = QPushButton("Generate Report")
        report_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #388E3C;
            }
        """)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(report_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec()

    def create_conflict_resolution_tab(self):
        """Create the Conflict Resolution tab"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Title and Description
        desc = QLabel("Mediation services to resolve disputes and maintain harmony among students.")
        desc.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        layout.addWidget(desc)

        # New Case Button
        new_case_btn = QPushButton("New Case")
        new_case_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                align-self: flex-end;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(new_case_btn)
        layout.addLayout(button_layout)

        # Cases List
        cases = [
            {
                "title": "Student Dispute",
                "case_id": "CR-2023-042",
                "parties": "Class 9A Students",
                "mediator": "Ms. Johnson",
                "date": "Oct 18, 2023",
                "status": "Resolved"
            },
            {
                "title": "Bullying Incident",
                "case_id": "CR-2023-041",
                "parties": "Students from Class 8B & 8C",
                "mediator": "Mr. Roberts",
                "date": "Oct 15, 2023",
                "status": "In Progress"
            },
            {
                "title": "Property Damage",
                "case_id": "CR-2023-040",
                "parties": "Class 10A Student",
                "mediator": "Ms. Thompson",
                "date": "Oct 12, 2023",
                "status": "Scheduled"
            }
        ]

        for case in cases:
            case_card = self.create_case_card(case)
            layout.addWidget(case_card)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_case_card(self, case):
        """Create a case card widget"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 15px;
                margin: 5px 0;
            }
        """)

        layout = QVBoxLayout()

        # Header with title and status
        header = QHBoxLayout()
        
        title = QLabel(case["title"])
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        
        case_id = QLabel(f"Case ID: {case['case_id']}")
        case_id.setStyleSheet("color: #7f8c8d;")
        
        status = QLabel(case["status"])
        status_color = {
            "Resolved": "#27ae60",
            "In Progress": "#f39c12",
            "Scheduled": "#3498db"
        }
        status.setStyleSheet(f"""
            color: white;
            background: {status_color.get(case['status'], '#95a5a6')};
            padding: 5px 10px;
            border-radius: 3px;
        """)

        header.addWidget(title)
        header.addWidget(case_id)
        header.addStretch()
        header.addWidget(status)

        # Details
        details = QHBoxLayout()
        
        parties = QLabel(f"Parties Involved:\n{case['parties']}")
        parties.setStyleSheet("color: #7f8c8d;")
        
        mediator = QLabel(f"Mediator:\n{case['mediator']}")
        mediator.setStyleSheet("color: #7f8c8d;")
        
        date = QLabel(f"📅 {case['date']}")
        date.setStyleSheet("color: #7f8c8d;")

        details.addWidget(parties)
        details.addStretch()
        details.addWidget(mediator)
        details.addStretch()
        details.addWidget(date)

        # View Details button
        view_btn = QPushButton("View Details")
        view_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2196F3;
                border: none;
                text-align: left;
                padding: 5px 0;
            }
            QPushButton:hover {
                color: #1976D2;
            }
        """)

        layout.addLayout(header)
        layout.addLayout(details)
        layout.addWidget(view_btn)
        card.setLayout(layout)
        return card

    def create_human_resource_tab(self):
        """Create the Human Resource tab"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Search and Filter Section
        search_section = QHBoxLayout()
        
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search lectures...")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 300px;
            }
        """)

        search_section.addWidget(search_box)
        search_section.addStretch()
        layout.addLayout(search_section)

        # Table
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            "Teacher Name", "Grade", "Time", "Duration", 
            "Date", "Venue", "Update", "View"
        ])
        table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        # Sample data
        data = [
            ["Mr. Smith", "Grade 9", "10:00 AM", "1 hour", "2023-10-20", "Room 101"],
            ["Mrs. Johnson", "Grade 8", "11:30 AM", "45 min", "2023-10-20", "Lab 2"],
            ["Dr. Brown", "Grade 10", "2:00 PM", "1.5 hours", "2023-10-20", "Auditorium"],
        ]

        table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)
            
            # Add buttons
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background: #2196F3;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background: #1976D2;
                }
            """)
            
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background: #388E3C;
                }
            """)
            view_btn.clicked.connect(lambda checked, r=row: self.show_lecture_details(r))

            table.setCellWidget(row, 6, update_btn)
            table.setCellWidget(row, 7, view_btn)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(table)

        tab.setLayout(layout)
        return tab

    def show_lecture_details(self, row):
        """Show detailed lecture information in a dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Lecture Details")
        dialog.setMinimumWidth(600)
        dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)

        layout = QVBoxLayout()

        # Lecturer Info
        info_group = QGroupBox("Lecturer Information")
        info_layout = QFormLayout()
        
        info_layout.addRow("Name:", QLabel("Mr. Smith"))
        info_layout.addRow("Qualification:", QLabel("Ph.D. in Physics"))
        info_layout.addRow("Experience:", QLabel("10 years"))
        info_layout.addRow("Specialization:", QLabel("Quantum Mechanics"))
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Lecture Materials
        materials_group = QGroupBox("Lecture Materials")
        materials_layout = QVBoxLayout()
        
        ppt_label = QLabel("Presentation: Quantum_Physics_Intro.ppt")
        ppt_label.setStyleSheet("color: #2196F3;")
        
        materials_layout.addWidget(ppt_label)
        materials_group.setLayout(materials_layout)
        layout.addWidget(materials_group)

        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec()

def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = DisciplineDepartmentPage()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
