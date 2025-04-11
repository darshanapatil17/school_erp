import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QComboBox, QMessageBox, QDialog, QFormLayout,
                           QDateEdit, QFrame, QStackedWidget, QSpinBox,
                           QFileDialog, QScrollArea, QGroupBox)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

class AddInspectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Inspection")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.equipment = QComboBox()
        self.equipment.addItems([
            "Fire Extinguisher", "First Aid Kit", "Eyewash Station",
            "Chemical Spill Kit", "Emergency Shower"
        ])
        
        self.location = QComboBox()
        self.location.addItems(["Main Lab", "Chemistry Section", "Biology Section", "Physics Section"])
        
        self.inspection_date = QDateEdit()
        self.inspection_date.setCalendarPopup(True)
        self.inspection_date.setDate(QDate.currentDate())
        
        self.status = QComboBox()
        self.status.addItems(["Operational", "Needs Restock", "Needs Maintenance", "Out of Service"])

        # Add fields to form
        layout.addRow("Equipment:", self.equipment)
        layout.addRow("Location:", self.location)
        layout.addRow("Inspection Date:", self.inspection_date)
        layout.addRow("Status:", self.status)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
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
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_inspection_data(self):
        next_inspection = self.inspection_date.date().addMonths(3)  # Schedule next inspection in 3 months
        return [
            self.equipment.currentText(),
            self.location.currentText(),
            self.inspection_date.date().toString("yyyy-MM-dd"),
            self.status.currentText(),
            next_inspection.toString("yyyy-MM-dd")
        ]

class ReportIssueDialog(QDialog):
    def __init__(self, equipment, location, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Report Safety Issue")
        self.setModal(True)
        self.equipment = equipment
        self.location = location
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Equipment and Location (read-only)
        self.equipment_label = QLabel(self.equipment)
        self.location_label = QLabel(self.location)

        # Issue Type
        self.issue_type = QComboBox()
        self.issue_type.addItems([
            "Malfunction",
            "Damage",
            "Missing Components",
            "Expired",
            "Safety Concern",
            "Other"
        ])

        # Priority Level
        self.priority = QComboBox()
        self.priority.addItems([
            "Low - Schedule Maintenance",
            "Medium - Needs Attention Soon",
            "High - Urgent Safety Risk"
        ])

        # Description
        self.description = QLineEdit()
        self.description.setPlaceholderText("Describe the issue in detail...")

        # Add fields to form
        layout.addRow("Equipment:", self.equipment_label)
        layout.addRow("Location:", self.location_label)
        layout.addRow("Issue Type:", self.issue_type)
        layout.addRow("Priority:", self.priority)
        layout.addRow("Description:", self.description)

        # Add buttons
        button_box = QHBoxLayout()
        submit_btn = QPushButton("Submit Report")
        submit_btn.setStyleSheet("""
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
        submit_btn.clicked.connect(self.validate_and_accept)
        
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
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(submit_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def validate_and_accept(self):
        if not self.description.text().strip():
            QMessageBox.warning(self, "Warning", "Please provide a description of the issue.")
            return
        self.accept()

    def get_report_data(self):
        return {
            "equipment": self.equipment,
            "location": self.location,
            "issue_type": self.issue_type.currentText(),
            "priority": self.priority.currentText(),
            "description": self.description.text().strip()
        }

class AddEquipmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Equipment")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.category = QComboBox()
        self.category.addItems(["Glassware", "Apparatus", "Measurement", "Optics"])
        
        self.equipment_name = QLineEdit()
        self.equipment_name.setPlaceholderText("Enter equipment name")
        
        self.quantity = QSpinBox()
        self.quantity.setRange(1, 1000)
        
        self.condition = QComboBox()
        self.condition.addItems(["Good", "Needs Calibration", "Needs Repair", "Out of Service"])

        # Add fields to form
        layout.addRow("Category:", self.category)
        layout.addRow("Equipment Name:", self.equipment_name)
        layout.addRow("Quantity:", self.quantity)
        layout.addRow("Condition:", self.condition)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.validate_and_accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
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
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def validate_and_accept(self):
        if not self.equipment_name.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter equipment name.")
            return
        self.accept()

    def get_equipment_data(self):
        return [
            self.category.currentText(),
            self.equipment_name.text().strip(),
            str(self.quantity.value()),
            datetime.now().strftime("%Y-%m-%d"),
            self.condition.currentText()
        ]

class SafetyEquipmentTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header section
        header_layout = QVBoxLayout()
        title = QLabel("Safety Equipment & Procedures")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Monitor and maintain laboratory safety equipment")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards section
        stats_layout = QHBoxLayout()
        
        # Equipment Operational Card
        operational_card = QFrame()
        operational_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        operational_layout = QVBoxLayout(operational_card)
        self.operational_value = QLabel("80%")
        self.operational_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #00c853;")
        operational_label = QLabel("Equipment Operational")
        operational_label.setStyleSheet("color: gray;")
        operational_layout.addWidget(self.operational_value)
        operational_layout.addWidget(operational_label)
        stats_layout.addWidget(operational_card)

        # Need Attention Card
        attention_card = QFrame()
        attention_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        attention_layout = QVBoxLayout(attention_card)
        self.attention_value = QLabel("2")
        self.attention_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffa000;")
        attention_label = QLabel("Need Attention")
        attention_label.setStyleSheet("color: gray;")
        attention_layout.addWidget(self.attention_value)
        attention_layout.addWidget(attention_label)
        stats_layout.addWidget(attention_card)

        # Next Inspection Card
        inspection_card = QFrame()
        inspection_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        inspection_layout = QVBoxLayout(inspection_card)
        self.inspection_value = QLabel("10/25")
        self.inspection_value.setStyleSheet("font-size: 32px; font-weight: bold;")
        inspection_label = QLabel("Next Inspection")
        inspection_label.setStyleSheet("color: gray;")
        inspection_layout.addWidget(self.inspection_value)
        inspection_layout.addWidget(inspection_label)
        stats_layout.addWidget(inspection_card)

        # Current Checking Date Card
        checking_card = QFrame()
        checking_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        checking_layout = QVBoxLayout(checking_card)
        self.checking_value = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.checking_value.setStyleSheet("font-size: 18px; font-weight: bold;")
        checking_label = QLabel("Last Inventory Check")
        checking_label.setStyleSheet("color: gray;")
        checking_layout.addWidget(self.checking_value)
        checking_layout.addWidget(checking_label)
        stats_layout.addWidget(checking_card)

        layout.addLayout(stats_layout)

        # Action buttons section
        action_layout = QHBoxLayout()
        
        report_btn = QPushButton("Report Issue")
        report_btn.setStyleSheet("""
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
        report_btn.clicked.connect(self.report_issue)

        schedule_btn = QPushButton("Schedule Inspection")
        schedule_btn.setStyleSheet("""
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
        schedule_btn.clicked.connect(self.schedule_inspection)

        action_layout.addStretch()
        action_layout.addWidget(report_btn)
        action_layout.addWidget(schedule_btn)
        layout.addLayout(action_layout)

        # Equipment table
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(6)
        self.equipment_table.setHorizontalHeaderLabels([
            "Equipment", "Location", "Last Inspection", "Status", "Next Inspection", "Actions"
        ])
        self.equipment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.equipment_table.setSortingEnabled(True)

        # Sample data
        self.sample_data = [
            ["Fire Extinguisher", "Main Lab", "2023-09-15", "Operational", "2023-12-15"],
            ["First Aid Kit", "Main Lab", "2023-09-15", "Needs Restock", "2023-10-15"],
            ["Eyewash Station", "Chemistry Section", "2023-09-02", "Operational", "2023-12-02"],
            ["Chemical Spill Kit", "Chemistry Section", "2023-08-20", "Operational", "2023-11-20"],
            ["Emergency Shower", "Main Lab", "2023-09-10", "Operational", "2023-12-10"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.equipment_table)

    def populate_table(self, data):
        self.equipment_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                
                # Make date columns sortable
                if col in [2, 4]:  # Last Inspection and Next Inspection columns
                    item.setData(Qt.ItemDataRole.UserRole, QDate.fromString(value, "yyyy-MM-dd"))
                
                # Center align all cells
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Make items read-only
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Set status color
                if col == 3:  # Status column
                    if value == "Operational":
                        item.setForeground(Qt.GlobalColor.green)
                    elif value == "Needs Restock":
                        item.setForeground(Qt.GlobalColor.yellow)
                    else:
                        item.setForeground(Qt.GlobalColor.red)
                
                self.equipment_table.setItem(row, col, item)
            
            # Create button container widget
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            update_btn.clicked.connect(lambda checked, row=row: self.update_equipment(row))
            
            # Add Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            delete_btn.clicked.connect(lambda checked, row=row: self.delete_equipment(row))
            
            # Add buttons to layout
            button_layout.addWidget(update_btn)
            button_layout.addWidget(delete_btn)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.equipment_table.setCellWidget(row, 5, button_widget)

        self.update_stats()

    def update_equipment(self, row):
        dialog = AddInspectionDialog(self)
        
        # Pre-fill the dialog with existing data
        dialog.equipment.setCurrentText(self.equipment_table.item(row, 0).text())
        dialog.location.setCurrentText(self.equipment_table.item(row, 1).text())
        dialog.inspection_date.setDate(QDate.currentDate())
        dialog.status.setCurrentText(self.equipment_table.item(row, 3).text())
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_inspection_data()
            self.sample_data[row] = new_data
            self.populate_table(self.sample_data)
            self.update_stats()
            QMessageBox.information(self, "Success", "Equipment status updated successfully!")

    def schedule_inspection(self):
        dialog = AddInspectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_inspection = dialog.get_inspection_data()
            self.sample_data.append(new_inspection)
            self.populate_table(self.sample_data)
            self.update_stats()
            QMessageBox.information(self, "Success", "Inspection scheduled successfully!")

    def report_issue(self):
        current_row = self.equipment_table.currentRow()
        if current_row >= 0:
            equipment = self.equipment_table.item(current_row, 0).text()
            location = self.equipment_table.item(current_row, 1).text()
            
            dialog = ReportIssueDialog(equipment, location, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                report_data = dialog.get_report_data()
                
                # Update equipment status to reflect the issue
                self.sample_data[current_row][3] = "Needs Maintenance"
                self.populate_table(self.sample_data)
                self.update_stats()
                
                # Show confirmation with report details
                QMessageBox.information(
                    self,
                    "Issue Reported",
                    f"Issue reported successfully!\n\n"
                    f"Equipment: {report_data['equipment']}\n"
                    f"Location: {report_data['location']}\n"
                    f"Issue Type: {report_data['issue_type']}\n"
                    f"Priority: {report_data['priority']}\n"
                    f"Description: {report_data['description']}"
                )
        else:
            QMessageBox.warning(self, "Warning", "Please select equipment to report an issue.")

    def delete_equipment(self, row):
        equipment_name = self.equipment_table.item(row, 1).text()
        reply = QMessageBox.question(
            self, 
            'Delete Equipment',
            f'Are you sure you want to delete {equipment_name}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.sample_data.pop(row)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", f"{equipment_name} has been deleted successfully!")

    def update_stats(self):
        total = len(self.sample_data)
        operational = sum(1 for item in self.sample_data if item[3] == "Operational")
        needs_attention = total - operational
        
        # Update stats
        self.operational_value.setText(f"{int(operational/total*100)}%")
        self.attention_value.setText(str(needs_attention))
        
        # Find next inspection date
        next_dates = [QDate.fromString(item[4], "yyyy-MM-dd") for item in self.sample_data]
        if next_dates:
            next_date = min(next_dates)
            self.inspection_value.setText(next_date.toString("MM/dd"))

        # Update current checking date
        self.checking_value.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))

class LabEquipmentTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header section
        header_layout = QVBoxLayout()
        title = QLabel("Laboratory Equipment")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage scientific apparatus, glassware, and tools")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Add section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search equipment...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_equipment)

        # Add Equipment button
        add_btn = QPushButton("Add Equipment")
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
        add_btn.clicked.connect(self.add_equipment)

        # Report Issue button
        report_btn = QPushButton("Report Issue")
        report_btn.setStyleSheet("""
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
        report_btn.clicked.connect(self.report_issue)

        search_layout.addWidget(self.search_box)
        search_layout.addStretch()
        search_layout.addWidget(report_btn)
        search_layout.addWidget(add_btn)
        layout.addLayout(search_layout)

        # Category cards section
        cards_layout = QHBoxLayout()
        
        # Glassware Card
        glassware_card = QFrame()
        glassware_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        glassware_layout = QVBoxLayout(glassware_card)
        glassware_title = QLabel("Glassware")
        glassware_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.glassware_count = QLabel("155 items")
        self.glassware_count.setStyleSheet("color: gray;")
        glassware_layout.addWidget(glassware_title)
        glassware_layout.addWidget(self.glassware_count)
        cards_layout.addWidget(glassware_card)

        # Measuring Card
        measuring_card = QFrame()
        measuring_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        measuring_layout = QVBoxLayout(measuring_card)
        measuring_title = QLabel("Measuring")
        measuring_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.measuring_count = QLabel("42 items")
        self.measuring_count.setStyleSheet("color: gray;")
        measuring_layout.addWidget(measuring_title)
        measuring_layout.addWidget(self.measuring_count)
        cards_layout.addWidget(measuring_card)

        # Physics Card
        physics_card = QFrame()
        physics_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        physics_layout = QVBoxLayout(physics_card)
        physics_title = QLabel("Physics")
        physics_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.physics_count = QLabel("68 items")
        self.physics_count.setStyleSheet("color: gray;")
        physics_layout.addWidget(physics_title)
        physics_layout.addWidget(self.physics_count)
        cards_layout.addWidget(physics_card)

        # Biology Card
        biology_card = QFrame()
        biology_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        biology_layout = QVBoxLayout(biology_card)
        biology_title = QLabel("Biology")
        biology_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.biology_count = QLabel("77 items")
        self.biology_count.setStyleSheet("color: gray;")
        biology_layout.addWidget(biology_title)
        biology_layout.addWidget(self.biology_count)
        cards_layout.addWidget(biology_card)

        layout.addLayout(cards_layout)

        # Equipment table
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(6)
        self.equipment_table.setHorizontalHeaderLabels([
            "Category", "Equipment Name", "Quantity", "Last Checked", "Condition", "Actions"
        ])
        self.equipment_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.equipment_table.setSortingEnabled(True)

        # Sample data
        self.sample_data = [
            ["Glassware", "Beakers (250ml)", "35", "2023-09-18", "Good"],
            ["Glassware", "Test Tubes", "120", "2023-09-18", "Good"],
            ["Apparatus", "Bunsen Burners", "25", "2023-09-10", "Good"],
            ["Measurement", "Digital Scales", "5", "2023-08-25", "Needs Calibration"],
            ["Optics", "Microscopes", "20", "2023-09-05", "Good"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.equipment_table)

    def populate_table(self, data):
        self.equipment_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                
                # Center align all cells
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Make items read-only
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Set condition color
                if col == 4:  # Condition column
                    if value == "Good":
                        item.setForeground(Qt.GlobalColor.green)
                    elif value == "Needs Calibration":
                        item.setForeground(Qt.GlobalColor.yellow)
                    else:
                        item.setForeground(Qt.GlobalColor.red)
                
                self.equipment_table.setItem(row, col, item)
            
            # Create button container widget
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            update_btn.clicked.connect(lambda checked, row=row: self.update_equipment(row))
            
            # Add Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            delete_btn.clicked.connect(lambda checked, row=row: self.delete_equipment(row))
            
            # Add buttons to layout
            button_layout.addWidget(update_btn)
            button_layout.addWidget(delete_btn)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.equipment_table.setCellWidget(row, 5, button_widget)

        self.update_category_counts()

    def update_category_counts(self):
        # Count items in each category
        glassware = sum(int(item[2]) for item in self.sample_data if item[0] == "Glassware")
        measuring = sum(int(item[2]) for item in self.sample_data if item[0] == "Measurement")
        physics = sum(int(item[2]) for item in self.sample_data if item[0] == "Physics")
        biology = sum(int(item[2]) for item in self.sample_data if item[0] == "Biology")

        # Update labels
        self.glassware_count.setText(f"{glassware} items")
        self.measuring_count.setText(f"{measuring} items")
        self.physics_count.setText(f"{physics} items")
        self.biology_count.setText(f"{biology} items")

    def search_equipment(self):
        search_text = self.search_box.text().lower()
        for row in range(self.equipment_table.rowCount()):
            should_show = False
            for col in range(self.equipment_table.columnCount() - 1):  # Exclude Actions column
                item = self.equipment_table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            self.equipment_table.setRowHidden(row, not should_show)

    def add_equipment(self):
        dialog = AddEquipmentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_equipment = dialog.get_equipment_data()
            self.sample_data.append(new_equipment)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Equipment added successfully!")

    def update_equipment(self, row):
        dialog = AddEquipmentDialog(self)
        
        # Pre-fill the dialog with existing data
        dialog.category.setCurrentText(self.equipment_table.item(row, 0).text())
        dialog.equipment_name.setText(self.equipment_table.item(row, 1).text())
        dialog.quantity.setValue(int(self.equipment_table.item(row, 2).text()))
        dialog.condition.setCurrentText(self.equipment_table.item(row, 4).text())
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_equipment_data()
            self.sample_data[row] = new_data
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Equipment updated successfully!")

    def delete_equipment(self, row):
        equipment_name = self.equipment_table.item(row, 1).text()
        reply = QMessageBox.question(
            self, 
            'Delete Equipment',
            f'Are you sure you want to delete {equipment_name}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.sample_data.pop(row)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", f"{equipment_name} has been deleted successfully!")

    def report_issue(self):
        current_row = self.equipment_table.currentRow()
        if current_row >= 0:
            equipment = self.equipment_table.item(current_row, 1).text()
            category = self.equipment_table.item(current_row, 0).text()
            
            dialog = ReportIssueDialog(equipment, category, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                report_data = dialog.get_report_data()
                
                # Update equipment condition
                self.sample_data[current_row][4] = "Needs Repair"
                self.populate_table(self.sample_data)
                
                # Show confirmation with report details
                QMessageBox.information(
                    self,
                    "Issue Reported",
                    f"Issue reported successfully!\n\n"
                    f"Equipment: {report_data['equipment']}\n"
                    f"Category: {report_data['location']}\n"
                    f"Issue Type: {report_data['issue_type']}\n"
                    f"Priority: {report_data['priority']}\n"
                    f"Description: {report_data['description']}"
                )
        else:
            QMessageBox.warning(self, "Warning", "Please select equipment to report an issue.")

class ChemicalStorageTab(QWidget):
    def __init__(self):
        super().__init__()
        # Define required chemicals by curriculum standards (1st to 10th)
        self.required_inventory = {
            "Primary (1st-5th)": {
                "count": 10,
                "chemicals": [
                    "Litmus Solution", "Universal Indicator",
                    "Sodium Chloride (Table Salt)", "Sugar Solution",
                    "Vinegar (Acetic Acid)", "Lime Water",
                    "Food Colors", "Starch Solution",
                    "Copper Sulfate", "Iodine Solution"
                ],
                "min_quantity": "500 ml"
            },
            "Middle School (6th-8th)": {
                "count": 15,
                "chemicals": [
                    "Hydrochloric Acid (HCl) - Dilute", "Sulfuric Acid (H2SO4) - Dilute",
                    "Sodium Hydroxide (NaOH)", "Calcium Hydroxide (Ca(OH)2)",
                    "Methyl Orange", "Phenolphthalein",
                    "Zinc Metal", "Copper Metal",
                    "Iron Filings", "Magnesium Ribbon",
                    "Copper Sulfate (CuSO4)", "Zinc Sulfate (ZnSO4)",
                    "Ammonium Chloride (NH4Cl)", "Sodium Bicarbonate (NaHCO3)",
                    "Potassium Permanganate (KMnO4)"
                ],
                "min_quantity": "1 liter"
            },
            "Secondary (9th-10th)": {
                "count": 20,
                "chemicals": [
                    "Hydrochloric Acid (HCl) - Concentrated", "Sulfuric Acid (H2SO4) - Concentrated",
                    "Nitric Acid (HNO3)", "Acetic Acid (CH3COOH)",
                    "Sodium Hydroxide (NaOH) - Pellets", "Potassium Hydroxide (KOH)",
                    "Ethanol", "Methanol",
                    "Benedict's Solution", "Fehling's Solution A & B",
                    "Silver Nitrate (AgNO3)", "Barium Chloride (BaCl2)",
                    "Lead Nitrate (Pb(NO3)2)", "Calcium Oxide (CaO)",
                    "Aluminum Sulfate (Al2(SO4)3)", "Ferric Chloride (FeCl3)",
                    "Potassium Iodide (KI)", "Sodium Thiosulfate (Na2S2O3)",
                    "Ammonium Hydroxide (NH4OH)", "Calcium Carbonate (CaCO3)"
                ],
                "min_quantity": "2 liters"
            }
        }
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header section
        header_layout = QVBoxLayout()
        title = QLabel("Chemical Storage & Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Track and secure laboratory chemicals")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats cards section
        stats_layout = QHBoxLayout()
        
        # Required Chemicals Card
        required_card = QFrame()
        required_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        required_layout = QVBoxLayout(required_card)
        self.required_value = QLabel("45")
        self.required_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #dc3545;")
        required_label = QLabel("Required Chemicals")
        required_label.setStyleSheet("color: gray;")
        required_layout.addWidget(self.required_value)
        required_layout.addWidget(required_label)
        stats_layout.addWidget(required_card)

        # Available Chemicals Card
        available_card = QFrame()
        available_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        available_layout = QVBoxLayout(available_card)
        self.available_value = QLabel("0")
        self.available_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #28a745;")
        available_label = QLabel("Available Chemicals")
        available_label.setStyleSheet("color: gray;")
        available_layout.addWidget(self.available_value)
        available_layout.addWidget(available_label)
        stats_layout.addWidget(available_card)

        # Need of Chemicals Card
        need_card = QFrame()
        need_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        need_layout = QVBoxLayout(need_card)
        self.need_value = QLabel("0")
        self.need_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffa000;")
        need_label = QLabel("Need of Chemicals")
        need_label.setStyleSheet("color: gray;")
        need_layout.addWidget(self.need_value)
        need_layout.addWidget(need_label)
        stats_layout.addWidget(need_card)

        # Current Checking Date/Time Card
        checking_card = QFrame()
        checking_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        checking_layout = QVBoxLayout(checking_card)
        self.checking_value = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.checking_value.setStyleSheet("font-size: 18px; font-weight: bold;")
        checking_label = QLabel("Last Inventory Check")
        checking_label.setStyleSheet("color: gray;")
        checking_layout.addWidget(self.checking_value)
        checking_layout.addWidget(checking_label)
        stats_layout.addWidget(checking_card)

        layout.addLayout(stats_layout)

        # Search and Action section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search chemicals...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_chemicals)

        # Order Supplies button
        order_btn = QPushButton("Order Supplies")
        order_btn.setStyleSheet("""
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
        order_btn.clicked.connect(self.order_supplies)

        # Add Chemical button
        add_btn = QPushButton("Add Chemical")
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
        add_btn.clicked.connect(self.add_chemical)

        search_layout.addWidget(self.search_box)
        search_layout.addStretch()
        search_layout.addWidget(order_btn)
        search_layout.addWidget(add_btn)
        layout.addLayout(search_layout)

        # Chemicals table
        self.chemicals_table = QTableWidget()
        self.chemicals_table.setColumnCount(6)
        self.chemicals_table.setHorizontalHeaderLabels([
            "Chemical Name", "Category", "Storage Location", "Quantity", "Hazard Level", "Actions"
        ])
        self.chemicals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.chemicals_table.setSortingEnabled(True)

        # Sample data - empty initially
        self.sample_data = []
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.chemicals_table)
        
        # Update stats initially
        self.update_stats()

    def populate_table(self, data):
        self.chemicals_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                
                # Center align all cells
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Make items read-only
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Set hazard level color
                if col == 4:  # Hazard Level column
                    if value == "High":
                        item.setForeground(Qt.GlobalColor.red)
                    elif value == "Medium":
                        item.setForeground(Qt.GlobalColor.darkYellow)
                    else:
                        item.setForeground(Qt.GlobalColor.green)
                
                self.chemicals_table.setItem(row, col, item)
            
            # Create button container widget
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            update_btn.clicked.connect(lambda checked, row=row: self.update_chemical(row))
            
            # Add Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            delete_btn.clicked.connect(lambda checked, row=row: self.delete_chemical(row))
            
            # Add buttons to layout
            button_layout.addWidget(update_btn)
            button_layout.addWidget(delete_btn)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.chemicals_table.setCellWidget(row, 5, button_widget)

    def search_chemicals(self):
        search_text = self.search_box.text().lower()
        for row in range(self.chemicals_table.rowCount()):
            should_show = False
            for col in range(self.chemicals_table.columnCount() - 1):  # Exclude Actions column
                item = self.chemicals_table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            self.chemicals_table.setRowHidden(row, not should_show)

    def add_chemical(self):
        dialog = AddChemicalDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_chemical = dialog.get_chemical_data()
            self.sample_data.append(new_chemical)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Chemical added successfully!")

    def update_chemical(self, row):
        dialog = AddChemicalDialog(self)
        
        # Pre-fill the dialog with existing data
        dialog.chemical_name.setText(self.chemicals_table.item(row, 0).text())
        dialog.category.setCurrentText(self.chemicals_table.item(row, 1).text())
        dialog.location.setCurrentText(self.chemicals_table.item(row, 2).text())
        dialog.quantity.setText(self.chemicals_table.item(row, 3).text())
        dialog.hazard_level.setCurrentText(self.chemicals_table.item(row, 4).text())
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_chemical_data()
            self.sample_data[row] = new_data
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Chemical updated successfully!")

    def delete_chemical(self, row):
        chemical_name = self.chemicals_table.item(row, 0).text()
        reply = QMessageBox.question(
            self, 
            'Delete Chemical',
            f'Are you sure you want to delete {chemical_name}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.sample_data.pop(row)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", f"{chemical_name} has been deleted successfully!")

    def order_supplies(self):
        # Get both missing and low stock chemicals
        missing_chemicals = []
        low_stock = self.get_low_stock_chemicals()
        
        # Check for missing required chemicals by grade level
        for grade_level, info in self.required_inventory.items():
            required_chemicals = set(info["chemicals"])
            available_chemicals = set(item[0] for item in self.sample_data)
            missing = required_chemicals - available_chemicals
            for chemical in missing:
                missing_chemicals.append({
                    'name': chemical,
                    'grade_level': grade_level,
                    'category': self.get_chemical_category(chemical),
                    'current_quantity': "0",
                    'required_quantity': info["min_quantity"]
                })

        all_needed = missing_chemicals + low_stock
        
        if all_needed:
            # Create a custom dialog with scrollable area
            dialog = QDialog(self)
            dialog.setWindowTitle("Order Supplies")
            dialog.setMinimumWidth(500)
            dialog.setMinimumHeight(400)
            
            layout = QVBoxLayout(dialog)
            
            # Create scroll area
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            
            # Add title
            title = QLabel("Chemicals needed for curriculum requirements:")
            title.setStyleSheet("font-weight: bold; font-size: 14px;")
            scroll_layout.addWidget(title)
            
            # Add chemicals by grade level
            for grade_level in ["Primary (1st-5th)", "Middle School (6th-8th)", "Secondary (9th-10th)"]:
                grade_chemicals = [c for c in missing_chemicals if c['grade_level'] == grade_level]
                if grade_chemicals:
                    grade_label = QLabel(f"\n{grade_level}:")
                    grade_label.setStyleSheet("font-weight: bold;")
                    scroll_layout.addWidget(grade_label)
                    
                    for chemical in grade_chemicals:
                        chemical_info = QLabel(
                            f"• {chemical['name']}\n"
                            f"  Required Quantity: {chemical['required_quantity']}"
                        )
                        scroll_layout.addWidget(chemical_info)
            
            if low_stock:
                low_stock_label = QLabel("\nLow Stock Chemicals:")
                low_stock_label.setStyleSheet("font-weight: bold;")
                scroll_layout.addWidget(low_stock_label)
                
                for chemical in low_stock:
                    chemical_info = QLabel(
                        f"• {chemical['name']} (Current: {chemical['current_quantity']})\n"
                        f"  Category: {chemical['category']}"
                    )
                    scroll_layout.addWidget(chemical_info)
            
            scroll_layout.addStretch()
            scroll.setWidget(scroll_content)
            layout.addWidget(scroll)
            
            # Add buttons
            button_layout = QHBoxLayout()
            
            generate_pdf_btn = QPushButton("Generate PDF")
            generate_pdf_btn.setStyleSheet("""
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
            
            button_layout.addWidget(generate_pdf_btn)
            button_layout.addWidget(cancel_btn)
            layout.addLayout(button_layout)
            
            # Connect button signals
            generate_pdf_btn.clicked.connect(lambda: self.generate_pdf_report(all_needed))
            generate_pdf_btn.clicked.connect(dialog.accept)
            cancel_btn.clicked.connect(dialog.reject)
            
            # Show dialog
            dialog.exec()
        else:
            QMessageBox.information(
                self,
                "Order Supplies",
                "All curriculum-required chemicals are at adequate levels.\nNo new orders needed at this time."
            )
    
    def generate_pdf_report(self, all_needed):
        # Get save location for PDF
        current_date = datetime.now().strftime("%Y-%m-%d")
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Chemical Order List",
            f"Chemical_Order_List_{current_date}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            # Create order details for PDF
            order_details = []
            
            # Add header information
            order_details.append(["Chemical Order List", "", "", "", ""])
            order_details.append([f"Date: {current_date}", "", "", "", ""])
            order_details.append(["", "", "", "", ""])  # Empty row for spacing
            order_details.append(["Chemical Name", "Grade Level", "Category", "Current Stock", "Order Amount"])
            
            # Add chemicals by grade level
            for chemical in all_needed:
                if 'grade_level' in chemical:  # Missing chemicals
                    order_amount = "1 liter"
                    if chemical['grade_level'] == "Middle School (6th-8th)":
                        order_amount = "2 liters"
                    elif chemical['grade_level'] == "Secondary (9th-10th)":
                        order_amount = "5 liters"
                    
                    order_details.append([
                        chemical['name'],
                        chemical['grade_level'],
                        chemical['category'],
                        chemical['current_quantity'],
                        order_amount
                    ])
                else:  # Low stock chemicals
                    if 'kg' in chemical['current_quantity'].lower():
                        order_amount = "5 kg"
                    elif 'liter' in chemical['current_quantity'].lower():
                        order_amount = "5 liters"
                    elif 'ml' in chemical['current_quantity'].lower():
                        order_amount = "1000 ml"
                    else:
                        order_amount = "Standard package"
                    
                    order_details.append([
                        chemical['name'],
                        "Low Stock",
                        chemical['category'],
                        chemical['current_quantity'],
                        order_amount
                    ])
            
            # Create PDF
            doc = SimpleDocTemplate(
                file_name,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Create story for PDF
            story = []
            styles = getSampleStyleSheet()
            
            # Create title style
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30
            )
            
            # Add title
            story.append(Paragraph("Chemical Order List", title_style))
            story.append(Paragraph(f"Generated on: {current_date}", styles["Normal"]))
            story.append(Spacer(1, 20))
            
            # Create table
            table = Table(order_details[3:])  # Skip the header rows we added earlier
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
            
            story.append(table)
            
            # Build PDF
            doc.build(story)
            
            QMessageBox.information(
                self,
                "Success",
                f"Purchase order has been created and PDF saved as:\n{file_name}"
            )

    def update_stats(self):
        # Calculate total required chemicals across all standards
        total_required = sum(category["count"] for category in self.required_inventory.values())
        self.required_value.setText(str(total_required))
        
        # Count available chemicals
        total_available = len(self.sample_data)
        self.available_value.setText(str(total_available))
        
        # Calculate missing and low stock chemicals
        missing_chemicals = []
        low_stock = self.get_low_stock_chemicals()
        
        # Check for missing required chemicals
        for grade_level, info in self.required_inventory.items():
            required_chemicals = set(info["chemicals"])
            available_chemicals = set(item[0] for item in self.sample_data)
            missing = required_chemicals - available_chemicals
            missing_chemicals.extend(missing)

        total_missing = len(missing_chemicals) + len(low_stock)
        self.need_value.setText(str(total_missing))
        
        # Update current checking date/time
        self.checking_value.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))

        # Update colors based on curriculum requirements
        if total_available >= total_required and not low_stock:
            self.available_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #28a745;")  # Green
        elif total_available >= total_required * 0.7:
            self.available_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffa000;")  # Yellow
        else:
            self.available_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #dc3545;")  # Red

    def get_chemical_category(self, chemical_name):
        # Helper function to determine chemical category
        chemical_lower = chemical_name.lower()
        if any(acid in chemical_lower for acid in ["acid", "hcl", "h2so4", "hno3"]):
            return "Acid"
        elif any(base in chemical_lower for base in ["hydroxide", "naoh", "koh", "base"]):
            return "Base"
        elif any(organic in chemical_lower for organic in ["ethanol", "methanol", "alcohol"]):
            return "Organic"
        elif any(indicator in chemical_lower for indicator in ["indicator", "litmus", "phenolphthalein"]):
            return "Indicator"
        else:
            return "Salt"

    def get_storage_requirement(self, category):
        storage_requirements = {
            "Acid": "Acid Cabinet",
            "Base": "Base Cabinet",
            "Organic": "Flammable Cabinet",
            "Salt": "General Storage",
            "Indicator": "General Storage"
        }
        return storage_requirements.get(category, "General Storage")

    def get_low_stock_chemicals(self):
        low_stock = []
        for item in self.sample_data:
            name = item[0]
            category = item[1]
            quantity = item[3]
            if self.is_low_quantity(quantity):
                low_stock.append({
                    'name': name,
                    'category': category,
                    'current_quantity': quantity
                })
        return low_stock

    def is_low_quantity(self, quantity):
        try:
            # Extract numeric value and unit from quantity string
            num = float(''.join(filter(str.isdigit, quantity)))
            unit = ''.join(filter(str.isalpha, quantity.lower()))
            
            # Define minimum thresholds
            if 'kg' in unit:
                return num < 2  # Less than 2 kg
            elif 'liter' in unit or 'l' in unit:
                return num < 5  # Less than 5 liters
            elif 'ml' in unit:
                return num < 500  # Less than 500 ml
            elif 'g' in unit:
                return num < 500  # Less than 500 g
            return False
        except:
            return False

class AddChemicalDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Chemical")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.chemical_name = QLineEdit()
        self.chemical_name.setPlaceholderText("Enter chemical name")
        
        self.category = QComboBox()
        self.category.addItems(["Acid", "Base", "Organic", "Salt", "Indicator"])
        
        self.location = QComboBox()
        self.location.addItems([
            "Acid Cabinet", "Base Cabinet", "Flammable Cabinet", 
            "General Storage", "Cold Storage"
        ])
        
        self.quantity = QLineEdit()
        self.quantity.setPlaceholderText("Enter quantity (e.g., 5 liters, 3 kg)")
        
        self.hazard_level = QComboBox()
        self.hazard_level.addItems(["High", "Medium", "Low"])

        # Add fields to form
        layout.addRow("Chemical Name:", self.chemical_name)
        layout.addRow("Category:", self.category)
        layout.addRow("Storage Location:", self.location)
        layout.addRow("Quantity:", self.quantity)
        layout.addRow("Hazard Level:", self.hazard_level)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.validate_and_accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
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
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def validate_and_accept(self):
        if not self.chemical_name.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter chemical name.")
            return
        if not self.quantity.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter quantity.")
            return
        self.accept()

    def get_chemical_data(self):
        return [
            self.chemical_name.text().strip(),
            self.category.currentText(),
            self.location.currentText(),
            self.quantity.text().strip(),
            self.hazard_level.currentText()
        ]

class GuestLecturesTab(QWidget):
    def __init__(self):
        super().__init__()
        # Sample data for lectures - moved before initUI()
        self.sample_lectures = [
            ["DSJ", "Dr. Sarah Johnson", "Advances in Biotechnology", "2023-09-05", "10:00 - 12:00", "11th & 12th Grade"],
            ["PMC", "Prof. Michael Chen", "Quantum Physics in Everyday Life", "2023-08-15", "13:00 - 15:00", "10th Grade"],
            ["RKP", "Dr. Rachel K. Peterson", "Chemistry in Daily Life", "2023-09-20", "14:00 - 16:00", "9th Grade"],
            ["AKM", "Prof. Alan K. Miller", "Environmental Science Today", "2023-10-01", "11:00 - 13:00", "All Grades"],
            ["LWS", "Dr. Lisa W. Smith", "Modern Biology Applications", "2023-10-15", "09:00 - 11:00", "11th & 12th Grade"]
        ]
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header section
        header_layout = QVBoxLayout()
        title = QLabel("Guest Lectures & Workshops")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Track and manage guest expert sessions")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Action section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search lectures...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_lectures)

        # Schedule New Lecture button
        schedule_btn = QPushButton("Schedule New Lecture")
        schedule_btn.setStyleSheet("""
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
        schedule_btn.clicked.connect(self.schedule_lecture)

        search_layout.addWidget(self.search_box)
        search_layout.addStretch()
        search_layout.addWidget(schedule_btn)
        layout.addLayout(search_layout)

        # Lectures table
        self.lectures_table = QTableWidget()
        self.lectures_table.setColumnCount(7)
        self.lectures_table.setHorizontalHeaderLabels([
            "ID", "Guest Speaker", "Topic", "Date", "Time", "Audience", "Actions"
        ])
        self.lectures_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.lectures_table.setSortingEnabled(True)
        
        self.populate_table(self.sample_lectures)
        layout.addWidget(self.lectures_table)

    def populate_table(self, data):
        self.lectures_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.lectures_table.setItem(row, col, item)
            
            # Create button container widget
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            # Add View Details button
            view_btn = QPushButton("View Details")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            view_btn.clicked.connect(lambda checked, row=row: self.view_lecture_details(row))
            
            # Add Cancel button
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            cancel_btn.clicked.connect(lambda checked, row=row: self.cancel_lecture(row))
            
            button_layout.addWidget(view_btn)
            button_layout.addWidget(cancel_btn)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.lectures_table.setCellWidget(row, 6, button_widget)

    def search_lectures(self):
        search_text = self.search_box.text().lower()
        for row in range(self.lectures_table.rowCount()):
            should_show = False
            for col in range(self.lectures_table.columnCount() - 1):  # Exclude Actions column
                item = self.lectures_table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            self.lectures_table.setRowHidden(row, not should_show)

    def schedule_lecture(self):
        dialog = ScheduleLectureDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_lecture = dialog.get_lecture_data()
            self.sample_lectures.append(new_lecture)
            self.populate_table(self.sample_lectures)
            QMessageBox.information(self, "Success", "Lecture scheduled successfully!")

    def view_lecture_details(self, row):
        lecture_data = [self.lectures_table.item(row, col).text() for col in range(6)]
        
        # Create a custom dialog for lecture details
        dialog = QDialog(self)
        dialog.setWindowTitle("Lecture Details")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(400)
        
        layout = QVBoxLayout(dialog)
        
        # Basic lecture information
        info_group = QGroupBox("Lecture Information")
        info_layout = QFormLayout()
        
        info_layout.addRow("ID:", QLabel(lecture_data[0]))
        info_layout.addRow("Speaker:", QLabel(lecture_data[1]))
        info_layout.addRow("Topic:", QLabel(lecture_data[2]))
        info_layout.addRow("Date:", QLabel(lecture_data[3]))
        info_layout.addRow("Time:", QLabel(lecture_data[4]))
        info_layout.addRow("Audience:", QLabel(lecture_data[5]))
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Resources section
        resources_group = QGroupBox("Lecture Resources")
        resources_layout = QVBoxLayout()
        
        # Presentation upload section
        ppt_layout = QHBoxLayout()
        ppt_label = QLabel("Presentation:")
        self.ppt_path_label = QLabel("No file selected")
        ppt_upload_btn = QPushButton("Upload Presentation")
        ppt_upload_btn.setStyleSheet("""
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
        ppt_upload_btn.clicked.connect(lambda: self.upload_presentation(lecture_data[0]))
        
        ppt_layout.addWidget(ppt_label)
        ppt_layout.addWidget(self.ppt_path_label)
        ppt_layout.addWidget(ppt_upload_btn)
        resources_layout.addLayout(ppt_layout)
        
        # Photos upload section
        photos_layout = QHBoxLayout()
        photos_label = QLabel("Photos:")
        self.photos_count_label = QLabel("No photos uploaded")
        photos_upload_btn = QPushButton("Upload Photos")
        photos_upload_btn.setStyleSheet("""
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
        photos_upload_btn.clicked.connect(lambda: self.upload_photos(lecture_data[0]))
        
        photos_layout.addWidget(photos_label)
        photos_layout.addWidget(self.photos_count_label)
        photos_layout.addWidget(photos_upload_btn)
        resources_layout.addLayout(photos_layout)
        
        resources_group.setLayout(resources_layout)
        layout.addWidget(resources_group)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
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
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec()

    def upload_presentation(self, lecture_id):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Upload Presentation",
            "",
            "Presentations (*.pptx *.ppt *.pdf)"
        )
        
        if file_name:
            # Create lectures directory if it doesn't exist
            lecture_dir = f"lecture_resources/{lecture_id}"
            os.makedirs(lecture_dir, exist_ok=True)
            
            # Copy the presentation file
            presentation_path = f"{lecture_dir}/presentation{os.path.splitext(file_name)[1]}"
            try:
                import shutil
                shutil.copy2(file_name, presentation_path)
                self.ppt_path_label.setText(os.path.basename(file_name))
                QMessageBox.information(
                    self,
                    "Success",
                    "Presentation uploaded successfully!"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Failed to upload presentation: {str(e)}"
                )

    def upload_photos(self, lecture_id):
        file_names, _ = QFileDialog.getOpenFileNames(
            self,
            "Upload Photos",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        
        if file_names:
            # Create lectures directory if it doesn't exist
            lecture_dir = f"lecture_resources/{lecture_id}/photos"
            os.makedirs(lecture_dir, exist_ok=True)
            
            # Copy all selected photos
            try:
                import shutil
                for file_name in file_names:
                    photo_path = f"{lecture_dir}/{os.path.basename(file_name)}"
                    shutil.copy2(file_name, photo_path)
                
                self.photos_count_label.setText(f"{len(file_names)} photos uploaded")
                QMessageBox.information(
                    self,
                    "Success",
                    f"{len(file_names)} photos uploaded successfully!"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Failed to upload photos: {str(e)}"
                )

    def cancel_lecture(self, row):
        lecture_id = self.lectures_table.item(row, 0).text()
        speaker = self.lectures_table.item(row, 1).text()
        reply = QMessageBox.question(
            self, 
            'Cancel Lecture',
            f'Are you sure you want to cancel the lecture by {speaker}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.sample_lectures.pop(row)
            self.populate_table(self.sample_lectures)
            QMessageBox.information(self, "Success", f"Lecture {lecture_id} has been cancelled!")

class ScheduleLectureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule New Lecture")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.lecture_id = QLineEdit()
        self.lecture_id.setPlaceholderText("Enter unique ID (e.g., ABC)")
        
        self.speaker_name = QLineEdit()
        self.speaker_name.setPlaceholderText("Enter speaker's full name")
        
        self.topic = QLineEdit()
        self.topic.setPlaceholderText("Enter lecture topic")
        
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())
        
        self.time = QLineEdit()
        self.time.setPlaceholderText("Enter time (e.g., 10:00 - 12:00)")
        
        self.audience = QComboBox()
        self.audience.addItems([
            "9th Grade", "10th Grade", "11th Grade", "12th Grade",
            "11th & 12th Grade", "All Grades"
        ])

        # Add fields to form
        layout.addRow("Lecture ID:", self.lecture_id)
        layout.addRow("Speaker Name:", self.speaker_name)
        layout.addRow("Topic:", self.topic)
        layout.addRow("Date:", self.date)
        layout.addRow("Time:", self.time)
        layout.addRow("Target Audience:", self.audience)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.validate_and_accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
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
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def validate_and_accept(self):
        if not self.lecture_id.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a lecture ID.")
            return
        if not self.speaker_name.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter speaker's name.")
            return
        if not self.topic.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter lecture topic.")
            return
        if not self.time.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter lecture time.")
            return
        self.accept()

    def get_lecture_data(self):
        return [
            self.lecture_id.text().strip(),
            self.speaker_name.text().strip(),
            self.topic.text().strip(),
            self.date.date().toString("yyyy-MM-dd"),
            self.time.text().strip(),
            self.audience.currentText()
        ]

class ScienceLabDepartment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Science Lab Management")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add description text at the top
        description = QLabel("Manage lab safety, equipment, materials, and guest lectures")
        description.setStyleSheet("color: gray; padding: 10px 0;")
        main_layout.addWidget(description)
        
        # Create tab buttons
        tab_layout = QHBoxLayout()
        self.tab_buttons = []
        tabs = ["Safety Equipment", "Lab Equipment", "Chemical Storage", "Guest Lectures"]
        
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
        self.safety_equipment_page = SafetyEquipmentTab()
        self.lab_equipment_page = LabEquipmentTab()
        self.chemical_storage_page = ChemicalStorageTab()
        self.guest_lectures_page = GuestLecturesTab()
        
        self.stack.addWidget(self.safety_equipment_page)
        self.stack.addWidget(self.lab_equipment_page)
        self.stack.addWidget(self.chemical_storage_page)
        self.stack.addWidget(self.guest_lectures_page)

    def switch_tab(self, index):
        # Update button states
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)
        
        # Switch page
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScienceLabDepartment()
    window.show()
    sys.exit(app.exec()) 