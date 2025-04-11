from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QStackedWidget, QLineEdit, QComboBox,
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                            QApplication, QMainWindow, QFrame, QFileDialog, QDialog, QFormLayout)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import json
import os
import sys
import shutil
from datetime import datetime

class SportsRecreationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System - Sports & Recreation Department")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menubar
        menubar = self.menuBar()
        departments_menu = menubar.addMenu("Departments")
        
        # Add Sports & Recreation Department action
        sports_action = QAction("Sports & Recreation Department", self)
        departments_menu.addAction(sports_action)
        
        # Add separator and exit action
        departments_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        departments_menu.addAction(exit_action)

        # Create tab buttons
        tab_layout = QHBoxLayout()
        self.tab_buttons = []
        tabs = ["Coach Data", "Facilities", "Fitness Classes", 
                "Recreation Activities", "Competitions", "Gallery"]
        
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
        self.coach_data_page = CoachDataPage()
        self.facilities_page = FacilitiesPage()
        self.fitness_classes_page = FitnessClassesPage()
        self.recreation_activities_page = RecreationActivitiesPage()
        self.competitions_page = CompetitionsPage()
        self.gallery_page = GalleryPage()
        
        self.stack.addWidget(self.coach_data_page)
        self.stack.addWidget(self.facilities_page)
        self.stack.addWidget(self.fitness_classes_page)
        self.stack.addWidget(self.recreation_activities_page)
        self.stack.addWidget(self.competitions_page)
        self.stack.addWidget(self.gallery_page)

    def switch_tab(self, index):
        # Update button states
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)
        
        # Switch page
        self.stack.setCurrentIndex(index)

class CoachDataPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_sample_data()
        self.documents_dir = "coach_documents"
        self.create_documents_directory()

    def create_documents_directory(self):
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Coach Data")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage coach information and schedules")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Coaches Card
        total_card = QFrame()
        total_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        total_layout = QVBoxLayout(total_card)
        self.total_value = QLabel("12")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_label = QLabel("Total Coaches")
        total_label.setStyleSheet("color: gray;")
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        stats_layout.addWidget(total_card)
        
        # Active Coaches Card
        active_card = QFrame()
        active_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        active_layout = QVBoxLayout(active_card)
        self.active_value = QLabel("10")
        self.active_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        active_label = QLabel("Active Coaches")
        active_label.setStyleSheet("color: gray;")
        active_layout.addWidget(self.active_value)
        active_layout.addWidget(active_label)
        stats_layout.addWidget(active_card)

        # Available Slots Card
        slots_card = QFrame()
        slots_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        slots_layout = QVBoxLayout(slots_card)
        self.slots_value = QLabel("5")
        self.slots_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        slots_label = QLabel("Available Slots")
        slots_label.setStyleSheet("color: gray;")
        slots_layout.addWidget(self.slots_value)
        slots_layout.addWidget(slots_label)
        stats_layout.addWidget(slots_card)

        layout.addLayout(stats_layout)

        # Search and Add section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search coaches...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)

        # Sport filter
        self.sport_filter = QComboBox()
        self.sport_filter.addItems(["All Sports", "Football", "Basketball", "Cricket", "Tennis", "Swimming"])
        
        # Add Coach button
        add_btn = QPushButton("Add Coach")
        add_btn.setStyleSheet("""
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

        # Delete Coach button
        delete_btn = QPushButton("Delete Coach")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(self.show_delete_form)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.sport_filter)
        search_layout.addWidget(add_btn)
        search_layout.addWidget(delete_btn)
        layout.addLayout(search_layout)

        # Coaches table
        self.coaches_table = QTableWidget()
        self.coaches_table.setColumnCount(6)
        self.coaches_table.setHorizontalHeaderLabels([
            "Name", "Sport", "Experience", "Contact", "Status", "Actions"
        ])
        self.coaches_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.coaches_table)

    def load_sample_data(self):
        # Sample coach data
        coaches = [
            {"name": "John Smith", "sport": "Football", "experience": "5 years", "contact": "john@example.com", "status": "Active"},
            {"name": "Sarah Johnson", "sport": "Basketball", "experience": "3 years", "contact": "sarah@example.com", "status": "Active"},
            {"name": "Mike Brown", "sport": "Cricket", "experience": "7 years", "contact": "mike@example.com", "status": "Active"},
            {"name": "Emma Wilson", "sport": "Tennis", "experience": "4 years", "contact": "emma@example.com", "status": "Active"},
            {"name": "David Lee", "sport": "Swimming", "experience": "6 years", "contact": "david@example.com", "status": "Active"}
        ]

        self.coaches_table.setRowCount(len(coaches))
        for row, coach in enumerate(coaches):
            self.coaches_table.setItem(row, 0, QTableWidgetItem(coach["name"]))
            self.coaches_table.setItem(row, 1, QTableWidgetItem(coach["sport"]))
            self.coaches_table.setItem(row, 2, QTableWidgetItem(coach["experience"]))
            self.coaches_table.setItem(row, 3, QTableWidgetItem(coach["contact"]))
            self.coaches_table.setItem(row, 4, QTableWidgetItem(coach["status"]))
            
            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            view_btn.clicked.connect(lambda checked, r=row: self.show_view_form(r))
            
            actions_layout.addWidget(update_btn)
            actions_layout.addWidget(view_btn)
            self.coaches_table.setCellWidget(row, 5, actions_widget)

    def show_view_form(self, row=None):
        # Create view form dialog
        dialog = QWidget()
        dialog.setWindowTitle("View Coach Details")
        dialog.setGeometry(300, 300, 500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Coach information
        info_label = QLabel("Coach Information:")
        info_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(info_label)
        
        if row is not None:
            self.current_coach_row = row
            name = self.coaches_table.item(row, 0).text()
            sport = self.coaches_table.item(row, 1).text()
            experience = self.coaches_table.item(row, 2).text()
            contact = self.coaches_table.item(row, 3).text()
            status = self.coaches_table.item(row, 4).text()
            
            # Create a frame for coach info
            info_frame = QFrame()
            info_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 5px;
                    padding: 10px;
                }
            """)
            info_layout = QVBoxLayout(info_frame)
            
            info_text = f"""
            Name: {name}
            Sport: {sport}
            Experience: {experience}
            Contact: {contact}
            Status: {status}
            """
            info_display = QLabel(info_text)
            info_layout.addWidget(info_display)
            layout.addWidget(info_frame)
        
        # Documents section
        docs_label = QLabel("Documents:")
        docs_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        layout.addWidget(docs_label)
        
        # Create a frame for documents
        docs_frame = QFrame()
        docs_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        docs_layout = QVBoxLayout(docs_frame)
        
        # Upload button
        upload_btn = QPushButton("Upload Document")
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        upload_btn.clicked.connect(lambda: self.upload_document(dialog))
        docs_layout.addWidget(upload_btn)
        
        # Documents list
        self.documents_list = QVBoxLayout()
        self.load_coach_documents(name)
        docs_layout.addLayout(self.documents_list)
        
        layout.addWidget(docs_frame)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Save button
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        save_btn.clicked.connect(lambda: self.save_coach_details(dialog))
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        close_btn.clicked.connect(dialog.close)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.show()

    def upload_document(self, dialog):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Documents (*.pdf *.png)")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                file_name = os.path.basename(file_path)
                file_type = os.path.splitext(file_name)[1].lower()
                
                if file_type in ['.pdf', '.png']:
                    # Create coach's directory if it doesn't exist
                    coach_name = self.coaches_table.item(self.current_coach_row, 0).text()
                    coach_dir = os.path.join(self.documents_dir, coach_name.replace(" ", "_"))
                    if not os.path.exists(coach_dir):
                        os.makedirs(coach_dir)
                    
                    # Copy file to coach's directory
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{file_type}"
                    new_file_path = os.path.join(coach_dir, new_file_name)
                    shutil.copy2(file_path, new_file_path)
                    
                    # Add document to the list
                    self.add_document_to_list(new_file_name, file_type, coach_dir)
                else:
                    QMessageBox.warning(dialog, "Invalid File", "Please select a PDF or PNG file.")

    def load_coach_documents(self, coach_name):
        # Clear existing documents
        while self.documents_list.count():
            item = self.documents_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Load documents from coach's directory
        coach_dir = os.path.join(self.documents_dir, coach_name.replace(" ", "_"))
        if os.path.exists(coach_dir):
            for file_name in os.listdir(coach_dir):
                file_path = os.path.join(coach_dir, file_name)
                if os.path.isfile(file_path):
                    file_type = os.path.splitext(file_name)[1].lower()
                    if file_type in ['.pdf', '.png']:
                        self.add_document_to_list(file_name, file_type, coach_dir)

    def add_document_to_list(self, file_name, file_type, coach_dir):
        doc_widget = QWidget()
        doc_layout = QHBoxLayout(doc_widget)
        doc_layout.setContentsMargins(0, 0, 0, 0)
        
        # Document name and type
        doc_name = QLabel(f"{file_name}")
        doc_name.setStyleSheet("font-size: 12px;")
        
        # View button
        view_btn = QPushButton("View")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        view_btn.clicked.connect(lambda: self.view_document(os.path.join(coach_dir, file_name)))
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_document(os.path.join(coach_dir, file_name), doc_widget))
        
        doc_layout.addWidget(doc_name)
        doc_layout.addWidget(view_btn)
        doc_layout.addWidget(delete_btn)
        self.documents_list.addWidget(doc_widget)

    def view_document(self, file_path):
        # Open the document using the default system application
        os.startfile(file_path)

    def delete_document(self, file_path, widget):
        reply = QMessageBox.question(self, 'Delete Document', 
                                   'Are you sure you want to delete this document?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                widget.deleteLater()
                QMessageBox.information(self, "Success", "Document deleted successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete document: {str(e)}")

    def save_coach_details(self, dialog):
        QMessageBox.information(dialog, "Success", "Coach details saved successfully!")
        dialog.close()

    def show_delete_form(self, row=None):
        # Create delete form dialog
        dialog = QWidget()
        dialog.setWindowTitle("Delete Coach")
        dialog.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Coach information
        info_label = QLabel("Coach Information:")
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)
        
        if row is not None:
            name = self.coaches_table.item(row, 0).text()
            sport = self.coaches_table.item(row, 1).text()
            experience = self.coaches_table.item(row, 2).text()
            contact = self.coaches_table.item(row, 3).text()
            
            info_text = f"""
            Name: {name}
            Sport: {sport}
            Experience: {experience}
            Contact: {contact}
            """
            info_display = QLabel(info_text)
            layout.addWidget(info_display)
        
        # Reason for deletion
        reason_label = QLabel("Reason for Deletion:")
        reason_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(reason_label)
        
        reason_input = QLineEdit()
        reason_input.setPlaceholderText("Enter reason for deletion...")
        layout.addWidget(reason_input)
        
        # Confirmation buttons
        button_layout = QHBoxLayout()
        
        confirm_btn = QPushButton("Confirm Delete")
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        confirm_btn.clicked.connect(lambda: self.delete_coach(row, reason_input.text(), dialog))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        cancel_btn.clicked.connect(dialog.close)
        
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.show()

    def delete_coach(self, row, reason, dialog):
        if row is not None:
            # Remove the row from the table
            self.coaches_table.removeRow(row)
            
            # Update stats
            total = self.coaches_table.rowCount()
            self.total_value.setText(str(total))
            self.active_value.setText(str(total))
            
            # Show confirmation message
            QMessageBox.information(self, "Success", f"Coach deleted successfully.\nReason: {reason}")
            
            # Close the dialog
            dialog.close()

class FacilitiesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_sample_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Facilities")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage sports facilities and equipment")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Facilities Card
        total_card = QFrame()
        total_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        total_layout = QVBoxLayout(total_card)
        self.total_value = QLabel("8")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_label = QLabel("Total Facilities")
        total_label.setStyleSheet("color: gray;")
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        stats_layout.addWidget(total_card)
        
        # Available Facilities Card
        available_card = QFrame()
        available_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        available_layout = QVBoxLayout(available_card)
        self.available_value = QLabel("6")
        self.available_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        available_label = QLabel("Available")
        available_label.setStyleSheet("color: gray;")
        available_layout.addWidget(self.available_value)
        available_layout.addWidget(available_label)
        stats_layout.addWidget(available_card)

        # Under Maintenance Card
        maintenance_card = QFrame()
        maintenance_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        maintenance_layout = QVBoxLayout(maintenance_card)
        self.maintenance_value = QLabel("2")
        self.maintenance_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        maintenance_label = QLabel("Under Maintenance")
        maintenance_label.setStyleSheet("color: gray;")
        maintenance_layout.addWidget(self.maintenance_value)
        maintenance_layout.addWidget(maintenance_label)
        stats_layout.addWidget(maintenance_card)

        layout.addLayout(stats_layout)

        # Search and Add section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search facilities...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)

        # Facility type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "Indoor", "Outdoor", "Swimming Pool", "Gym"])
        
        # Add Facility button
        add_btn = QPushButton("Add Facility")
        add_btn.setStyleSheet("""
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

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.type_filter)
        search_layout.addWidget(add_btn)
        layout.addLayout(search_layout)

        # Facilities table
        self.facilities_table = QTableWidget()
        self.facilities_table.setColumnCount(5)
        self.facilities_table.setHorizontalHeaderLabels([
            "Name", "Capacity", "Status", "Last Maintenance", "Actions"
        ])
        self.facilities_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.facilities_table)

    def load_sample_data(self):
        # Sample facilities data
        facilities = [
            {
                "name": "Main Gymnasium",
                "capacity": "500 people",
                "status": "Available",
                "last_maintenance": "2024-01-15",
                "maintenance_schedule": "Monthly"
            },
            {
                "name": "Swimming Pool",
                "capacity": "100 people",
                "status": "Under Maintenance",
                "last_maintenance": "2024-02-01",
                "maintenance_schedule": "Weekly"
            },
            {
                "name": "Tennis Courts",
                "capacity": "4 courts",
                "status": "Available",
                "last_maintenance": "2024-01-20",
                "maintenance_schedule": "Bi-weekly"
            },
            {
                "name": "Fitness Center",
                "capacity": "50 people",
                "status": "Available",
                "last_maintenance": "2024-01-25",
                "maintenance_schedule": "Weekly"
            },
            {
                "name": "Running Track",
                "capacity": "8 lanes",
                "status": "Available",
                "last_maintenance": "2024-01-10",
                "maintenance_schedule": "Monthly"
            },
            {
                "name": "Basketball Court",
                "capacity": "2 courts",
                "status": "Available",
                "last_maintenance": "2024-01-30",
                "maintenance_schedule": "Weekly"
            },
            {
                "name": "Volleyball Court",
                "capacity": "2 courts",
                "status": "Available",
                "last_maintenance": "2024-01-28",
                "maintenance_schedule": "Weekly"
            },
            {
                "name": "Badminton Court",
                "capacity": "4 courts",
                "status": "Available",
                "last_maintenance": "2024-01-22",
                "maintenance_schedule": "Weekly"
            }
        ]

        self.facilities_table.setRowCount(len(facilities))
        for row, facility in enumerate(facilities):
            self.facilities_table.setItem(row, 0, QTableWidgetItem(facility["name"]))
            self.facilities_table.setItem(row, 1, QTableWidgetItem(facility["capacity"]))
            self.facilities_table.setItem(row, 2, QTableWidgetItem(facility["status"]))
            self.facilities_table.setItem(row, 3, QTableWidgetItem(facility["last_maintenance"]))
            
            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            
            actions_layout.addWidget(update_btn)
            self.facilities_table.setCellWidget(row, 4, actions_widget)

class FitnessClassesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_sample_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Fitness Classes")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage fitness classes and schedules")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Classes Card
        total_card = QFrame()
        total_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        total_layout = QVBoxLayout(total_card)
        self.total_value = QLabel("15")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_label = QLabel("Total Classes")
        total_label.setStyleSheet("color: gray;")
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        stats_layout.addWidget(total_card)
        
        # Active Classes Card
        active_card = QFrame()
        active_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        active_layout = QVBoxLayout(active_card)
        self.active_value = QLabel("12")
        self.active_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        active_label = QLabel("Active Classes")
        active_label.setStyleSheet("color: gray;")
        active_layout.addWidget(self.active_value)
        active_layout.addWidget(active_label)
        stats_layout.addWidget(active_card)

        layout.addLayout(stats_layout)

        # Search and Add section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search classes...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)

        # Level filter
        self.level_filter = QComboBox()
        self.level_filter.addItems(["All Levels", "Beginner", "Intermediate", "Advanced"])
        
        # Add Class button
        add_btn = QPushButton("Add Class")
        add_btn.setStyleSheet("""
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
        add_btn.clicked.connect(self.show_add_class_dialog)

        # Delete Class button
        delete_btn = QPushButton("Delete Class")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(self.delete_class)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.level_filter)
        search_layout.addWidget(add_btn)
        search_layout.addWidget(delete_btn)
        layout.addLayout(search_layout)

        # Classes table
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(8)
        self.classes_table.setHorizontalHeaderLabels([
            "Class Name", "Time", "Day", "Total Students", "Duration", "Level", "Location", "Actions"
        ])
        self.classes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.classes_table)

    def load_sample_data(self):
        # Sample fitness classes data
        classes = [
            {
                "name": "Morning Yoga",
                "time": "7:00 AM",
                "day": "Monday, Wednesday, Friday",
                "total_students": "20",
                "duration": "1 hour",
                "level": "Beginner",
                "location": "Yoga Studio"
            },
            {
                "name": "High-Intensity Training",
                "time": "5:00 PM",
                "day": "Tuesday, Thursday",
                "total_students": "15",
                "duration": "45 mins",
                "level": "Advanced",
                "location": "Main Gym"
            },
            {
                "name": "Zumba Fitness",
                "time": "6:00 PM",
                "day": "Monday, Wednesday",
                "total_students": "25",
                "duration": "1 hour",
                "level": "All Levels",
                "location": "Dance Studio"
            },
            {
                "name": "Pilates Core",
                "time": "4:00 PM",
                "day": "Tuesday, Thursday",
                "total_students": "12",
                "duration": "1 hour",
                "level": "Intermediate",
                "location": "Pilates Room"
            },
            {
                "name": "CrossFit Training",
                "time": "6:00 PM",
                "day": "Monday, Wednesday, Friday",
                "total_students": "18",
                "duration": "1 hour",
                "level": "Advanced",
                "location": "CrossFit Area"
            }
        ]

        self.classes_table.setRowCount(len(classes))
        for row, class_data in enumerate(classes):
            self.classes_table.setItem(row, 0, QTableWidgetItem(class_data["name"]))
            self.classes_table.setItem(row, 1, QTableWidgetItem(class_data["time"]))
            self.classes_table.setItem(row, 2, QTableWidgetItem(class_data["day"]))
            self.classes_table.setItem(row, 3, QTableWidgetItem(class_data["total_students"]))
            self.classes_table.setItem(row, 4, QTableWidgetItem(class_data["duration"]))
            self.classes_table.setItem(row, 5, QTableWidgetItem(class_data["level"]))
            self.classes_table.setItem(row, 6, QTableWidgetItem(class_data["location"]))
            
            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            
            actions_layout.addWidget(update_btn)
            self.classes_table.setCellWidget(row, 7, actions_widget)

    def show_add_class_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Class")
        dialog.setFixedSize(400, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Form fields
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        time_input = QLineEdit()
        day_input = QLineEdit()
        students_input = QLineEdit()
        location_input = QLineEdit()
        
        level_combo = QComboBox()
        level_combo.addItems(["Beginner", "Intermediate", "Advanced", "All Levels"])
        
        duration_combo = QComboBox()
        duration_combo.addItems(["30 mins", "1 hour", "1.5 hours", "2 hours"])
        
        form_layout.addRow("Class Name:", name_input)
        form_layout.addRow("Time:", time_input)
        form_layout.addRow("Day:", day_input)
        form_layout.addRow("Total Students:", students_input)
        form_layout.addRow("Location:", location_input)
        form_layout.addRow("Level:", level_combo)
        form_layout.addRow("Duration:", duration_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        save_btn.clicked.connect(lambda: self.save_new_class(
            dialog, name_input.text(), time_input.text(), day_input.text(),
            students_input.text(), location_input.text(), level_combo.currentText(),
            duration_combo.currentText()
        ))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()

    def save_new_class(self, dialog, name, time, day, students, location, level, duration):
        if not all([name, time, day, students, location]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return
        
        row = self.classes_table.rowCount()
        self.classes_table.insertRow(row)
        
        self.classes_table.setItem(row, 0, QTableWidgetItem(name))
        self.classes_table.setItem(row, 1, QTableWidgetItem(time))
        self.classes_table.setItem(row, 2, QTableWidgetItem(day))
        self.classes_table.setItem(row, 3, QTableWidgetItem(students))
        self.classes_table.setItem(row, 4, QTableWidgetItem(duration))
        self.classes_table.setItem(row, 5, QTableWidgetItem(level))
        self.classes_table.setItem(row, 6, QTableWidgetItem(location))
        
        # Add action buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        
        update_btn = QPushButton("Update")
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        
        actions_layout.addWidget(update_btn)
        self.classes_table.setCellWidget(row, 7, actions_widget)
        
        dialog.accept()
        QMessageBox.information(self, "Success", "Class added successfully!")

    def delete_class(self):
        current_row = self.classes_table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(self, 'Delete Class',
                                       'Are you sure you want to delete this class?',
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.classes_table.removeRow(current_row)
                QMessageBox.information(self, "Success", "Class deleted successfully!")

class RecreationActivitiesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_sample_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Recreation Activities")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage recreational activities and events")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Activities Card
        total_card = QFrame()
        total_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        total_layout = QVBoxLayout(total_card)
        self.total_value = QLabel("10")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_label = QLabel("Total Activities")
        total_label.setStyleSheet("color: gray;")
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        stats_layout.addWidget(total_card)
        
        # Student Participants Card
        participants_card = QFrame()
        participants_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        participants_layout = QVBoxLayout(participants_card)
        self.participants_value = QLabel("120")
        self.participants_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        participants_label = QLabel("Student Participants")
        participants_label.setStyleSheet("color: gray;")
        participants_layout.addWidget(self.participants_value)
        participants_layout.addWidget(participants_label)
        stats_layout.addWidget(participants_card)

        layout.addLayout(stats_layout)

        # Search and Add section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search activities...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)

        # Activity filter
        self.activity_filter = QComboBox()
        self.activity_filter.addItems(["All Activities", "Sports", "Arts", "Academic", "Games"])
        
        # Add Activity button
        add_btn = QPushButton("Add Activity")
        add_btn.setStyleSheet("""
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
        add_btn.clicked.connect(self.show_add_activity_dialog)

        # Delete Activity button
        delete_btn = QPushButton("Delete Activity")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(self.delete_activity)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.activity_filter)
        search_layout.addWidget(add_btn)
        search_layout.addWidget(delete_btn)
        layout.addLayout(search_layout)

        # Activities table
        self.activities_table = QTableWidget()
        self.activities_table.setColumnCount(8)
        self.activities_table.setHorizontalHeaderLabels([
            "Activity Name", "Day & Time", "Student Participants", "Location", "Coach", "Level", "Duration", "Actions"
        ])
        self.activities_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.activities_table)

    def load_sample_data(self):
        # Sample recreation activities data
        activities = [
            {
                "name": "Basketball Tournament",
                "day_time": "Saturday 2:00 PM",
                "participants": "24",
                "location": "Main Gym",
                "coach": "Coach Johnson",
                "level": "Intermediate",
                "duration": "2 hours"
            },
            {
                "name": "Chess Club",
                "day_time": "Monday, Wednesday 4:00 PM",
                "participants": "16",
                "location": "Library",
                "coach": "Mr. Smith",
                "level": "All Levels",
                "duration": "1 hour"
            },
            {
                "name": "Art Workshop",
                "day_time": "Tuesday, Thursday 3:30 PM",
                "participants": "20",
                "location": "Art Room",
                "coach": "Ms. Davis",
                "level": "Beginner",
                "duration": "1.5 hours"
            },
            {
                "name": "Drama Club",
                "day_time": "Friday 4:00 PM",
                "participants": "15",
                "location": "Auditorium",
                "coach": "Mrs. Wilson",
                "level": "Advanced",
                "duration": "2 hours"
            },
            {
                "name": "Science Club",
                "day_time": "Wednesday 3:30 PM",
                "participants": "18",
                "location": "Science Lab",
                "coach": "Dr. Brown",
                "level": "Intermediate",
                "duration": "1.5 hours"
            }
        ]

        self.activities_table.setRowCount(len(activities))
        for row, activity in enumerate(activities):
            self.activities_table.setItem(row, 0, QTableWidgetItem(activity["name"]))
            self.activities_table.setItem(row, 1, QTableWidgetItem(activity["day_time"]))
            self.activities_table.setItem(row, 2, QTableWidgetItem(activity["participants"]))
            self.activities_table.setItem(row, 3, QTableWidgetItem(activity["location"]))
            self.activities_table.setItem(row, 4, QTableWidgetItem(activity["coach"]))
            self.activities_table.setItem(row, 5, QTableWidgetItem(activity["level"]))
            self.activities_table.setItem(row, 6, QTableWidgetItem(activity["duration"]))
            
            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            
            actions_layout.addWidget(update_btn)
            self.activities_table.setCellWidget(row, 7, actions_widget)

    def show_add_activity_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Activity")
        dialog.setFixedSize(400, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Form fields
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        day_time_input = QLineEdit()
        participants_input = QLineEdit()
        location_input = QLineEdit()
        coach_input = QLineEdit()
        
        level_combo = QComboBox()
        level_combo.addItems(["Beginner", "Intermediate", "Advanced", "All Levels"])
        
        duration_combo = QComboBox()
        duration_combo.addItems(["30 mins", "1 hour", "1.5 hours", "2 hours", "2.5 hours", "3 hours"])
        
        form_layout.addRow("Activity Name:", name_input)
        form_layout.addRow("Day & Time:", day_time_input)
        form_layout.addRow("Student Participants:", participants_input)
        form_layout.addRow("Location:", location_input)
        form_layout.addRow("Coach:", coach_input)
        form_layout.addRow("Level:", level_combo)
        form_layout.addRow("Duration:", duration_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        save_btn.clicked.connect(lambda: self.save_new_activity(
            dialog, name_input.text(), day_time_input.text(), participants_input.text(),
            location_input.text(), coach_input.text(), level_combo.currentText(),
            duration_combo.currentText()
        ))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()

    def save_new_activity(self, dialog, name, day_time, participants, location, coach, level, duration):
        if not all([name, day_time, participants, location, coach]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return
        
        row = self.activities_table.rowCount()
        self.activities_table.insertRow(row)
        
        self.activities_table.setItem(row, 0, QTableWidgetItem(name))
        self.activities_table.setItem(row, 1, QTableWidgetItem(day_time))
        self.activities_table.setItem(row, 2, QTableWidgetItem(participants))
        self.activities_table.setItem(row, 3, QTableWidgetItem(location))
        self.activities_table.setItem(row, 4, QTableWidgetItem(coach))
        self.activities_table.setItem(row, 5, QTableWidgetItem(level))
        self.activities_table.setItem(row, 6, QTableWidgetItem(duration))
        
        # Add action buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        
        update_btn = QPushButton("Update")
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        
        actions_layout.addWidget(update_btn)
        self.activities_table.setCellWidget(row, 7, actions_widget)
        
        dialog.accept()
        QMessageBox.information(self, "Success", "Activity added successfully!")

    def delete_activity(self):
        current_row = self.activities_table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(self, 'Delete Activity',
                                       'Are you sure you want to delete this activity?',
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.activities_table.removeRow(current_row)
                QMessageBox.information(self, "Success", "Activity deleted successfully!")

class CompetitionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_sample_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Competitions")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage sports competitions and tournaments")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Competitions Card
        total_card = QFrame()
        total_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        total_layout = QVBoxLayout(total_card)
        self.total_value = QLabel("8")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_label = QLabel("Total Competitions")
        total_label.setStyleSheet("color: gray;")
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        stats_layout.addWidget(total_card)
        
        # Upcoming Competitions Card
        upcoming_card = QFrame()
        upcoming_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        upcoming_layout = QVBoxLayout(upcoming_card)
        self.upcoming_value = QLabel("3")
        self.upcoming_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        upcoming_label = QLabel("Upcoming")
        upcoming_label.setStyleSheet("color: gray;")
        upcoming_layout.addWidget(self.upcoming_value)
        upcoming_layout.addWidget(upcoming_label)
        stats_layout.addWidget(upcoming_card)

        # Participants Card
        participants_card = QFrame()
        participants_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        participants_layout = QVBoxLayout(participants_card)
        self.participants_value = QLabel("150")
        self.participants_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        participants_label = QLabel("Participants")
        participants_label.setStyleSheet("color: gray;")
        participants_layout.addWidget(self.participants_value)
        participants_layout.addWidget(participants_label)
        stats_layout.addWidget(participants_card)

        layout.addLayout(stats_layout)

        # Search and Add section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search competitions...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)

        # Competition type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "Inter-School", "Intra-School", "District", "State", "National"])
        
        # Add Competition button
        add_btn = QPushButton("Add Competition")
        add_btn.setStyleSheet("""
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

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.type_filter)
        search_layout.addWidget(add_btn)
        layout.addLayout(search_layout)

        # Competitions table
        self.competitions_table = QTableWidget()
        self.competitions_table.setColumnCount(7)
        self.competitions_table.setHorizontalHeaderLabels([
            "Competition Name", "Date", "Time", "Venue", "Participants", "Type", "Actions"
        ])
        self.competitions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.competitions_table)

    def load_sample_data(self):
        # Sample competitions data
        competitions = [
            {
                "name": "Annual Sports Day",
                "date": "2024-03-15",
                "time": "9:00 AM - 5:00 PM",
                "venue": "Main Stadium",
                "participants": "200 students",
                "type": "Inter-School"
            },
            {
                "name": "Basketball Championship",
                "date": "2024-02-20",
                "time": "2:00 PM - 6:00 PM",
                "venue": "Main Gymnasium",
                "participants": "16 teams",
                "type": "District Level"
            },
            {
                "name": "Swimming Meet",
                "date": "2024-04-05",
                "time": "8:00 AM - 12:00 PM",
                "venue": "Swimming Pool",
                "participants": "50 swimmers",
                "type": "State Level"
            },
            {
                "name": "Athletics Championship",
                "date": "2024-05-10",
                "time": "8:00 AM - 4:00 PM",
                "venue": "Running Track",
                "participants": "100 athletes",
                "type": "Inter-School"
            },
            {
                "name": "Tennis Tournament",
                "date": "2024-06-15",
                "time": "10:00 AM - 6:00 PM",
                "venue": "Tennis Courts",
                "participants": "32 players",
                "type": "District Level"
            },
            {
                "name": "Volleyball League",
                "date": "2024-07-20",
                "time": "3:00 PM - 7:00 PM",
                "venue": "Volleyball Court",
                "participants": "12 teams",
                "type": "Inter-School"
            },
            {
                "name": "Badminton Championship",
                "date": "2024-08-25",
                "time": "9:00 AM - 5:00 PM",
                "venue": "Badminton Court",
                "participants": "40 players",
                "type": "State Level"
            },
            {
                "name": "Table Tennis Tournament",
                "date": "2024-09-10",
                "time": "10:00 AM - 4:00 PM",
                "venue": "Indoor Sports Hall",
                "participants": "24 players",
                "type": "District Level"
            }
        ]

        self.competitions_table.setRowCount(len(competitions))
        for row, competition in enumerate(competitions):
            self.competitions_table.setItem(row, 0, QTableWidgetItem(competition["name"]))
            self.competitions_table.setItem(row, 1, QTableWidgetItem(competition["date"]))
            self.competitions_table.setItem(row, 2, QTableWidgetItem(competition["time"]))
            self.competitions_table.setItem(row, 3, QTableWidgetItem(competition["venue"]))
            self.competitions_table.setItem(row, 4, QTableWidgetItem(competition["participants"]))
            self.competitions_table.setItem(row, 5, QTableWidgetItem(competition["type"]))
            
            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            
            actions_layout.addWidget(update_btn)
            self.competitions_table.setCellWidget(row, 6, actions_widget)

class GalleryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Gallery")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("View and manage sports and recreation photos and videos")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Photos Card
        photos_card = QFrame()
        photos_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        photos_layout = QVBoxLayout(photos_card)
        self.photos_value = QLabel("250")
        self.photos_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        photos_label = QLabel("Total Photos")
        photos_label.setStyleSheet("color: gray;")
        photos_layout.addWidget(self.photos_value)
        photos_layout.addWidget(photos_label)
        stats_layout.addWidget(photos_card)
        
        # Total Videos Card
        videos_card = QFrame()
        videos_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        videos_layout = QVBoxLayout(videos_card)
        self.videos_value = QLabel("50")
        self.videos_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        videos_label = QLabel("Total Videos")
        videos_label.setStyleSheet("color: gray;")
        videos_layout.addWidget(self.videos_value)
        videos_layout.addWidget(videos_label)
        stats_layout.addWidget(videos_card)

        # Total Albums Card
        albums_card = QFrame()
        albums_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        albums_layout = QVBoxLayout(albums_card)
        self.albums_value = QLabel("15")
        self.albums_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        albums_label = QLabel("Total Albums")
        albums_label.setStyleSheet("color: gray;")
        albums_layout.addWidget(self.albums_value)
        albums_layout.addWidget(albums_label)
        stats_layout.addWidget(albums_card)

        layout.addLayout(stats_layout)

        # Search and Add section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search media...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)

        # Media type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "Photos", "Videos", "Albums"])
        
        # Upload Media button
        upload_btn = QPushButton("Upload Media")
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

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.type_filter)
        search_layout.addWidget(upload_btn)
        layout.addLayout(search_layout)

        # Media grid placeholder
        grid_placeholder = QLabel("Media Grid Will Appear Here")
        grid_placeholder.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            padding: 50px;
            background-color: #f8f9fa;
            border: 1px dashed #e0e0e0;
            border-radius: 4px;
        """)
        grid_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(grid_placeholder)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SportsRecreationPage()
    window.show()
    sys.exit(app.exec())
