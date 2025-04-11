import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar,
                           QMenu, QTableWidget, QTableWidgetItem, QHeaderView,
                           QStackedWidget, QComboBox, QMessageBox, QDialog,
                           QFormLayout, QSpinBox, QFrame, QGroupBox, QDateEdit,
                           QTimeEdit)
from PyQt6.QtCore import Qt, QTimer, QDate, QTime
from PyQt6.QtGui import QAction
from datetime import datetime

class AddHardwareDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Hardware")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.hardware_name = QLineEdit()
        self.lab = QComboBox()
        self.lab.addItems(["Lab A", "Lab B", "Lab C", "Lab D"])
        self.status = QComboBox()
        self.status.addItems(["Operational", "Needs Maintenance", "Out of Service"])
        self.details = QLineEdit()

        # Add fields to form
        layout.addRow("Hardware Name:", self.hardware_name)
        layout.addRow("Lab:", self.lab)
        layout.addRow("Status:", self.status)
        layout.addRow("Details:", self.details)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_hardware_data(self):
        return [
            self.hardware_name.text(),
            self.lab.currentText(),
            self.status.currentText(),
            datetime.now().strftime("%Y-%m-%d"),
            self.details.text()
        ]

class HardwareInventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Computer Hardware Inventory")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage computers, peripherals, and network equipment")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Filter section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search hardware...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_hardware)

        # Lab filter
        self.lab_filter = QComboBox()
        self.lab_filter.addItems(["All Labs", "Lab A", "Lab B", "Lab C", "Lab D"])
        self.lab_filter.currentTextChanged.connect(self.filter_by_lab)
        
        # Add Hardware button
        add_hardware_btn = QPushButton("Add Hardware")
        add_hardware_btn.setStyleSheet("""
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
        add_hardware_btn.clicked.connect(self.add_hardware)

        # Delete Hardware button
        delete_hardware_btn = QPushButton("Delete Hardware")
        delete_hardware_btn.setStyleSheet("""
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
        delete_hardware_btn.clicked.connect(self.delete_hardware)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.lab_filter)
        search_layout.addWidget(add_hardware_btn)
        search_layout.addWidget(delete_hardware_btn)
        layout.addLayout(search_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Computers Card
        total_card = QFrame()
        total_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        total_layout = QVBoxLayout(total_card)
        self.total_value = QLabel("92")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_label = QLabel("Total Computers")
        total_label.setStyleSheet("color: gray;")
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        stats_layout.addWidget(total_card)
        
        # Operational Card
        operational_card = QFrame()
        operational_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        operational_layout = QVBoxLayout(operational_card)
        self.operational_value = QLabel("85")
        self.operational_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        operational_label = QLabel("Operational")
        operational_label.setStyleSheet("color: gray;")
        operational_layout.addWidget(self.operational_value)
        operational_layout.addWidget(operational_label)
        stats_layout.addWidget(operational_card)

        # Need Maintenance Card
        maintenance_card = QFrame()
        maintenance_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        maintenance_layout = QVBoxLayout(maintenance_card)
        self.maintenance_value = QLabel("7")
        self.maintenance_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        maintenance_label = QLabel("Need Maintenance")
        maintenance_label.setStyleSheet("color: gray;")
        maintenance_layout.addWidget(self.maintenance_value)
        maintenance_layout.addWidget(maintenance_label)
        stats_layout.addWidget(maintenance_card)

        # Computer Labs Card
        labs_card = QFrame()
        labs_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        labs_layout = QVBoxLayout(labs_card)
        self.labs_value = QLabel("4")
        self.labs_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        labs_label = QLabel("Computer Labs")
        labs_label.setStyleSheet("color: gray;")
        labs_layout.addWidget(self.labs_value)
        labs_layout.addWidget(labs_label)
        stats_layout.addWidget(labs_card)

        # Inventory Check Date Card
        check_date_card = QFrame()
        check_date_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        check_date_layout = QVBoxLayout(check_date_card)
        self.check_date_value = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.check_date_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        check_date_label = QLabel("Last Inventory Check")
        check_date_label.setStyleSheet("color: gray;")
        check_date_layout.addWidget(self.check_date_value)
        check_date_layout.addWidget(check_date_label)
        stats_layout.addWidget(check_date_card)
        
        layout.addLayout(stats_layout)

        # Hardware table
        self.hardware_table = QTableWidget()
        self.hardware_table.setColumnCount(6)
        self.hardware_table.setHorizontalHeaderLabels([
            "Hardware Name", "Lab", "Status", "Last Serviced", "Details", "Actions"
        ])
        self.hardware_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data
        self.sample_data = [
            ["Dell Desktop Computer", "Lab A", "Operational", "2023-09-15", "Intel i5, 8GB RAM, 512GB SSD"],
            ["HP Monitor 24\"", "Lab A", "Operational", "2023-08-20", "LCD Display"],
            ["Logitech Mouse & Keyboard Set", "Lab A", "Operational", "2023-09-01", "Wireless"],
            ["HP LaserJet Printer", "Lab B", "Needs Maintenance", "2023-06-10", "Paper jam issues"],
            ["Cisco Network Switch", "Lab C", "Operational", "2023-09-05", "24 port gigabit"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.hardware_table)

        # Start timer to update the check date
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_check_date)
        self.timer.start(60000)  # Update every minute

    def populate_table(self, data):
        self.hardware_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.hardware_table.setItem(row, col, QTableWidgetItem(str(value)))
            
            # Add Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
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
            update_btn.clicked.connect(lambda checked, row=row: self.update_hardware(row))
            self.hardware_table.setCellWidget(row, 5, update_btn)

            # Set status color
            status_item = self.hardware_table.item(row, 2)
            if status_item.text() == "Operational":
                status_item.setForeground(Qt.GlobalColor.green)
            elif status_item.text() == "Needs Maintenance":
                status_item.setForeground(Qt.GlobalColor.yellow)
            else:
                status_item.setForeground(Qt.GlobalColor.red)

    def search_hardware(self):
        search_text = self.search_box.text().lower()
        for row in range(self.hardware_table.rowCount()):
            should_show = False
            for col in range(self.hardware_table.columnCount() - 1):  # Exclude Actions column
                item = self.hardware_table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            self.hardware_table.setRowHidden(row, not should_show)

    def filter_by_lab(self, lab):
        for row in range(self.hardware_table.rowCount()):
            lab_item = self.hardware_table.item(row, 1)
            should_show = lab == "All Labs" or (lab_item and lab == lab_item.text())
            self.hardware_table.setRowHidden(row, not should_show)

    def add_hardware(self):
        dialog = AddHardwareDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_hardware = dialog.get_hardware_data()
            self.sample_data.append(new_hardware)
            self.populate_table(self.sample_data)
            self.update_stats()
            QMessageBox.information(self, "Success", "Hardware added successfully!")

    def update_hardware(self, row):
        QMessageBox.information(self, "Update Hardware", 
                              f"Update dialog for {self.hardware_table.item(row, 0).text()} will be implemented.")

    def update_stats(self):
        total = len(self.sample_data)
        operational = sum(1 for item in self.sample_data if item[2] == "Operational")
        maintenance = sum(1 for item in self.sample_data if item[2] == "Needs Maintenance")
        
        self.total_value.setText(str(total))
        self.operational_value.setText(str(operational))
        self.maintenance_value.setText(str(maintenance))

    def update_check_date(self):
        self.check_date_value.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))

    def delete_hardware(self):
        current_row = self.hardware_table.currentRow()
        if current_row >= 0:
            hardware_name = self.hardware_table.item(current_row, 0).text()
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete {hardware_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                self.hardware_table.removeRow(current_row)
                self.sample_data.pop(current_row)
                self.update_stats()
                QMessageBox.information(self, "Success", "Hardware deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a hardware item to delete.")

class AddSoftwareDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Software")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.software_name = QLineEdit()
        self.lab = QComboBox()
        self.lab.addItems(["All", "Lab A", "Lab B", "Lab C", "Lab D"])
        self.type = QComboBox()
        self.type.addItems(["OS", "Productivity", "Design", "Programming", "Development"])
        self.license_status = QComboBox()
        self.license_status.addItems(["Active", "Open Source", "Expired"])
        self.expiry_date = QLineEdit()
        self.expiry_date.setPlaceholderText("YYYY-MM-DD (or N/A for Open Source)")

        # Add fields to form
        layout.addRow("Software Name:", self.software_name)
        layout.addRow("Lab:", self.lab)
        layout.addRow("Type:", self.type)
        layout.addRow("License Status:", self.license_status)
        layout.addRow("Expiry Date:", self.expiry_date)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_software_data(self):
        return [
            self.software_name.text(),
            self.lab.currentText(),
            self.type.currentText(),
            self.license_status.currentText(),
            self.expiry_date.text() if self.license_status.currentText() != "Open Source" else "N/A"
        ]

class SoftwareInventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Software Inventory")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage installed software and licenses")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Filter section
        search_layout = QHBoxLayout()
        
        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search software...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_software)

        # Lab filter
        self.lab_filter = QComboBox()
        self.lab_filter.addItems(["All Labs", "Lab A", "Lab B", "Lab C", "Lab D"])
        self.lab_filter.currentTextChanged.connect(self.filter_by_lab)
        
        # Add Software button
        add_software_btn = QPushButton("Add Software")
        add_software_btn.setStyleSheet("""
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
        add_software_btn.clicked.connect(self.add_software)

        # Delete Software button
        delete_software_btn = QPushButton("Delete Software")
        delete_software_btn.setStyleSheet("""
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
        delete_software_btn.clicked.connect(self.delete_software)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.lab_filter)
        search_layout.addWidget(add_software_btn)
        search_layout.addWidget(delete_software_btn)
        layout.addLayout(search_layout)

        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Total Software Card
        total_card = QFrame()
        total_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        total_layout = QVBoxLayout(total_card)
        self.total_value = QLabel("5")
        self.total_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        total_label = QLabel("Total Software")
        total_label.setStyleSheet("color: gray;")
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        stats_layout.addWidget(total_card)
        
        # Need Installation Card
        installation_card = QFrame()
        installation_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        installation_layout = QVBoxLayout(installation_card)
        self.installation_value = QLabel("2")
        self.installation_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        installation_label = QLabel("Need Installation")
        installation_label.setStyleSheet("color: gray;")
        installation_layout.addWidget(self.installation_value)
        installation_layout.addWidget(installation_label)
        stats_layout.addWidget(installation_card)

        # Last Inventory Check Card
        check_date_card = QFrame()
        check_date_card.setStyleSheet("QFrame { background-color: white; border-radius: 10px; padding: 15px; }")
        check_date_layout = QVBoxLayout(check_date_card)
        self.check_date_value = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.check_date_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        check_date_label = QLabel("Last Inventory Check")
        check_date_label.setStyleSheet("color: gray;")
        check_date_layout.addWidget(self.check_date_value)
        check_date_layout.addWidget(check_date_label)
        stats_layout.addWidget(check_date_card)
        
        layout.addLayout(stats_layout)

        # Software table
        self.software_table = QTableWidget()
        self.software_table.setColumnCount(5)  # Reduced from 6 to 5 columns
        self.software_table.setHorizontalHeaderLabels([
            "Software Name", "Lab", "Type", "License Status", "Actions"
        ])
        self.software_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data
        self.sample_data = [
            ["Microsoft Windows 11", "All", "OS", "Active"],
            ["Microsoft Office 365", "All", "Productivity", "Active"],
            ["Adobe Creative Cloud", "Lab C", "Design", "Active"],
            ["Python 3.11", "All", "Programming", "Open Source"],
            ["Visual Studio Code", "All", "Development", "Open Source"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.software_table)

        # Start timer to update the check date
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_check_date)
        self.timer.start(60000)  # Update every minute

    def populate_table(self, data):
        self.software_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.software_table.setItem(row, col, item)
            
            # Add Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
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
            update_btn.clicked.connect(lambda checked, row=row: self.update_software(row))
            self.software_table.setCellWidget(row, 4, update_btn)

            # Set license status color
            status_item = self.software_table.item(row, 3)
            if status_item.text() == "Active":
                status_item.setForeground(Qt.GlobalColor.green)
            elif status_item.text() == "Open Source":
                status_item.setForeground(Qt.GlobalColor.gray)
            else:
                status_item.setForeground(Qt.GlobalColor.red)

    def update_check_date(self):
        self.check_date_value.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))

    def update_software(self, row):
        software_name = self.software_table.item(row, 0).text()
        QMessageBox.information(self, "Update Software", 
                              f"Update dialog for {software_name} will be implemented.")

    def search_software(self):
        search_text = self.search_box.text().lower()
        for row in range(self.software_table.rowCount()):
            should_show = False
            for col in range(self.software_table.columnCount() - 1):  # Exclude Actions column
                item = self.software_table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            self.software_table.setRowHidden(row, not should_show)

    def filter_by_lab(self, lab):
        lab = "All" if lab == "All Labs" else lab
        for row in range(self.software_table.rowCount()):
            lab_item = self.software_table.item(row, 1)
            should_show = lab == "All" or (lab_item and lab == lab_item.text())
            self.software_table.setRowHidden(row, not should_show)

    def add_software(self):
        dialog = AddSoftwareDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_software = dialog.get_software_data()
            self.sample_data.append(new_software)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Software added successfully!")

    def delete_software(self):
        current_row = self.software_table.currentRow()
        if current_row >= 0:
            software_name = self.software_table.item(current_row, 0).text()
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete {software_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                self.software_table.removeRow(current_row)
                self.sample_data.pop(current_row)
                self.total_value.setText(str(len(self.sample_data)))
                QMessageBox.information(self, "Success", "Software deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a software item to delete.")

class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Class")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())
        
        # Day label will be updated automatically when date changes
        self.day_label = QLabel()
        self.update_day_label()
        self.date.dateChanged.connect(self.update_day_label)

        self.time_start = QTimeEdit()
        self.time_start.setTime(QTime(9, 0))
        self.time_end = QTimeEdit()
        self.time_end.setTime(QTime(10, 30))

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_start)
        time_layout.addWidget(QLabel("-"))
        time_layout.addWidget(self.time_end)

        self.lab = QComboBox()
        self.lab.addItems(["Lab A", "Lab B", "Lab C"])
        
        self.class_name = QLineEdit()
        self.class_name.setPlaceholderText("Enter class (e.g., 10B)")
        
        self.subject = QComboBox()
        self.subject.addItems([
            "Computer Science", "Programming", "Computer Basics",
            "Web Development", "MCQ exam", "Practical Exam"
        ])
        
        self.teacher = QLineEdit()
        self.teacher.setPlaceholderText("Enter teacher name")

        # Add fields to form
        layout.addRow("Date:", self.date)
        layout.addRow("Day:", self.day_label)
        layout.addRow("Time:", time_layout)
        layout.addRow("Lab:", self.lab)
        layout.addRow("Class:", self.class_name)
        layout.addRow("Subject:", self.subject)
        layout.addRow("Teacher:", self.teacher)

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

    def update_day_label(self):
        selected_date = self.date.date()
        day_name = selected_date.toString("dddd")
        self.day_label.setText(day_name)

    def validate_and_accept(self):
        # Validate all required fields
        if not self.lab.currentText():
            QMessageBox.warning(self, "Warning", "Please select a lab.")
            return
            
        if not self.class_name.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a class name.")
            return
            
        if not self.subject.currentText():
            QMessageBox.warning(self, "Warning", "Please select a subject.")
            return
            
        if not self.teacher.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a teacher name.")
            return
            
        # Validate time range
        start_time = self.time_start.time()
        end_time = self.time_end.time()
        if start_time >= end_time:
            QMessageBox.warning(self, "Warning", "End time must be after start time.")
            return
            
        self.accept()

    def get_class_data(self):
        time_start = self.time_start.time().toString("HH:mm")
        time_end = self.time_end.time().toString("HH:mm")
        return [
            self.date.date().toString("yyyy-MM-dd"),
            self.date.date().toString("dddd"),
            f"{time_start} - {time_end}",
            self.lab.currentText(),
            self.class_name.text().strip(),
            self.subject.currentText(),
            self.teacher.text().strip()
        ]

class LabClassesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Computer Lab Class Schedule")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Track classes using computer labs")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Time filter buttons
        filter_layout = QHBoxLayout()
        
        self.today_btn = QPushButton("Today")
        self.this_week_btn = QPushButton("This Week")
        
        for btn in [self.today_btn, self.this_week_btn]:
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f2f5;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #e4e6e9;
                }
                QPushButton:checked {
                    background-color: #1a73e8;
                    color: white;
                }
            """)
        
        self.today_btn.clicked.connect(lambda: self.filter_classes("today"))
        self.this_week_btn.clicked.connect(lambda: self.filter_classes("week"))

        filter_layout.addWidget(self.today_btn)
        filter_layout.addWidget(self.this_week_btn)
        
        # Schedule Class button
        schedule_btn = QPushButton("Schedule Class")
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
        schedule_btn.clicked.connect(self.schedule_class)

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
        
        filter_layout.addStretch()
        filter_layout.addWidget(schedule_btn)
        filter_layout.addWidget(delete_btn)
        layout.addLayout(filter_layout)

        # Classes table
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(8)  # Increased from 7 to 8 for the Day column
        self.classes_table.setHorizontalHeaderLabels([
            "Date", "Day", "Time", "Lab", "Class", "Subject", "Teacher", "Actions"
        ])
        self.classes_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.classes_table.setSortingEnabled(True)

        # Generate sample data with current dates
        self.sample_data = self.generate_sample_data()
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.classes_table)

        # Show all classes by default
        self.show_all_classes()

    def generate_sample_data(self):
        current_date = QDate.currentDate()
        current_day = current_date.dayOfWeek()  # Monday is 1, Sunday is 7
        
        # Calculate dates for the current week
        days_data = []
        
        # Today's classes
        today_str = current_date.toString("yyyy-MM-dd")
        today_day = current_date.toString("dddd")  # Gets the day name (Monday, Tuesday, etc.)
        days_data.extend([
            [today_str, today_day, "09:00 - 10:30", "Lab A", "10A", "Computer Science", "Mr. Richards"],
            [today_str, today_day, "11:00 - 12:30", "Lab B", "11B", "Programming", "Ms. Zhang"],
            [today_str, today_day, "14:00 - 15:30", "Lab C", "12A", "Web Development", "Mrs. Patel"]
        ])

        # Add classes for remaining days of the week (until Saturday)
        for i in range(1, 7 - current_day + 1):  # From tomorrow until Saturday
            next_date = current_date.addDays(i)
            date_str = next_date.toString("yyyy-MM-dd")
            day_str = next_date.toString("dddd")  # Gets the day name
            
            if i == 1:  # Tomorrow
                days_data.extend([
                    [date_str, day_str, "09:00 - 10:30", "Lab A", "9C", "Computer Basics", "Mr. Thompson"],
                    [date_str, day_str, "11:00 - 12:30", "Lab B", "10B", "Computer Science", "Mr. Richards"]
                ])
            elif i == 2:  # Day after tomorrow
                days_data.extend([
                    [date_str, day_str, "10:00 - 11:30", "Lab C", "11A", "Programming", "Ms. Zhang"],
                    [date_str, day_str, "13:00 - 14:30", "Lab A", "12B", "Web Development", "Mrs. Patel"]
                ])
            else:  # Rest of the week
                days_data.extend([
                    [date_str, day_str, "09:00 - 10:30", "Lab " + chr(65 + (i % 3)), f"{9 + (i % 4)}{'ABC'[i % 3]}", 
                     ["Computer Science", "Programming", "Web Development", "Computer Basics"][i % 4],
                     ["Mr. Richards", "Ms. Zhang", "Mrs. Patel", "Mr. Thompson"][i % 4]]
                ])

        return days_data

    def populate_table(self, data):
        self.classes_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col == 0:  # Make date column sortable
                    item.setData(Qt.ItemDataRole.UserRole, QDate.fromString(value, "yyyy-MM-dd"))
                elif col == 2:  # Make time column sortable
                    time_start = value.split(" - ")[0]
                    item.setData(Qt.ItemDataRole.UserRole, QTime.fromString(time_start, "HH:mm"))
                
                # Center align all cells
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Make items read-only
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                self.classes_table.setItem(row, col, item)
            
            # Add Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            update_btn.clicked.connect(lambda checked, row=row: self.update_class(row))
            
            # Create a widget to center the button
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.addWidget(update_btn)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            self.classes_table.setCellWidget(row, 7, button_widget)

        # Sort by date and time
        self.classes_table.sortItems(0)  # Sort by date column
        self.classes_table.sortItems(2)  # Then sort by time

    def show_all_classes(self):
        # Show all rows and uncheck filter buttons
        for row in range(self.classes_table.rowCount()):
            self.classes_table.setRowHidden(row, False)
        self.today_btn.setChecked(False)
        self.this_week_btn.setChecked(False)

    def filter_classes(self, period):
        # First show all classes
        for row in range(self.classes_table.rowCount()):
            self.classes_table.setRowHidden(row, False)

        # Uncheck all buttons
        self.today_btn.setChecked(False)
        self.this_week_btn.setChecked(False)
        
        current_date = QDate.currentDate()
        
        if period == "today":
            self.today_btn.setChecked(True)
            for row in range(self.classes_table.rowCount()):
                date = QDate.fromString(self.classes_table.item(row, 0).text(), "yyyy-MM-dd")
                self.classes_table.setRowHidden(row, date != current_date)
        
        elif period == "week":
            self.this_week_btn.setChecked(True)
            current_day = current_date.dayOfWeek()  # Monday is 1, Sunday is 7
            
            # Calculate tomorrow and Saturday
            tomorrow = current_date.addDays(1)
            days_until_saturday = 6 - current_day  # 6 is Saturday
            saturday = current_date.addDays(days_until_saturday)
            
            for row in range(self.classes_table.rowCount()):
                date = QDate.fromString(self.classes_table.item(row, 0).text(), "yyyy-MM-dd")
                # Show only classes from tomorrow to Saturday
                self.classes_table.setRowHidden(row, date < tomorrow or date > saturday)

    def delete_class(self):
        current_row = self.classes_table.currentRow()
        if current_row >= 0:
            date = self.classes_table.item(current_row, 0).text()
            day = self.classes_table.item(current_row, 1).text()
            time = self.classes_table.item(current_row, 2).text()
            class_name = self.classes_table.item(current_row, 4).text()
            
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete the class:\n\n"
                f"Date: {date}\n"
                f"Day: {day}\n"
                f"Time: {time}\n"
                f"Class: {class_name}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.classes_table.removeRow(current_row)
                self.sample_data.pop(current_row)
                QMessageBox.information(self, "Success", "Class deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select a class to delete.")

    def schedule_class(self):
        dialog = AddClassDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_class = dialog.get_class_data()
            
            # Check for time conflicts
            date = new_class[0]
            time_range = new_class[2]
            lab = new_class[3]
            
            for existing_class in self.sample_data:
                if (existing_class[0] == date and 
                    existing_class[2] == time_range and 
                    existing_class[3] == lab):
                    QMessageBox.warning(
                        self,
                        "Scheduling Conflict",
                        f"There is already a class scheduled in {lab} at {time_range} on {date}."
                    )
                    return
            
            self.sample_data.append(new_class)
            self.populate_table(self.sample_data)
            
            QMessageBox.information(
                self,
                "Success",
                f"Class scheduled successfully!\n\n"
                f"Date: {new_class[0]}\n"
                f"Day: {new_class[1]}\n"
                f"Time: {new_class[2]}\n"
                f"Lab: {new_class[3]}\n"
                f"Class: {new_class[4]}\n"
                f"Subject: {new_class[5]}\n"
                f"Teacher: {new_class[6]}"
            )

    def update_class(self, row):
        dialog = AddClassDialog(self)
        
        # Pre-fill the dialog with existing data
        date = QDate.fromString(self.classes_table.item(row, 0).text(), "yyyy-MM-dd")
        dialog.date.setDate(date)
        
        time_range = self.classes_table.item(row, 2).text().split(" - ")
        dialog.time_start.setTime(QTime.fromString(time_range[0], "HH:mm"))
        dialog.time_end.setTime(QTime.fromString(time_range[1], "HH:mm"))
        
        dialog.lab.setCurrentText(self.classes_table.item(row, 3).text())
        dialog.class_name.setText(self.classes_table.item(row, 4).text())
        dialog.subject.setCurrentText(self.classes_table.item(row, 5).text())
        dialog.teacher.setText(self.classes_table.item(row, 6).text())

        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_class = dialog.get_class_data()
            
            # Check for time conflicts with other classes (excluding the current row)
            date = updated_class[0]
            time_range = updated_class[2]
            lab = updated_class[3]
            
            for i, existing_class in enumerate(self.sample_data):
                if i != row and (existing_class[0] == date and 
                    existing_class[2] == time_range and 
                    existing_class[3] == lab):
                    QMessageBox.warning(
                        self,
                        "Scheduling Conflict",
                        f"There is already a class scheduled in {lab} at {time_range} on {date}."
                    )
                    return
            
            self.sample_data[row] = updated_class
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Class updated successfully!")

class AddExamDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Exam")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.exam_name = QLineEdit()
        self.exam_name.setPlaceholderText("Enter exam name")
        
        self.class_name = QLineEdit()
        self.class_name.setPlaceholderText("Enter class (e.g., 10A)")
        
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())
        
        self.time_start = QTimeEdit()
        self.time_start.setTime(QTime(9, 0))
        self.time_end = QTimeEdit()
        self.time_end.setTime(QTime(11, 0))

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_start)
        time_layout.addWidget(QLabel("-"))
        time_layout.addWidget(self.time_end)

        self.lab = QComboBox()
        self.lab.addItems(["Lab A", "Lab B", "Lab C"])
        
        self.supervisor = QLineEdit()
        self.supervisor.setPlaceholderText("Enter supervisor name")

        # Add fields to form
        layout.addRow("Exam Name:", self.exam_name)
        layout.addRow("Class:", self.class_name)
        layout.addRow("Date:", self.date)
        layout.addRow("Time:", time_layout)
        layout.addRow("Lab:", self.lab)
        layout.addRow("Supervisor:", self.supervisor)

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
        if not self.exam_name.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter an exam name.")
            return
            
        if not self.class_name.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a class name.")
            return
            
        if not self.supervisor.text().strip():
            QMessageBox.warning(self, "Warning", "Please enter a supervisor name.")
            return
            
        start_time = self.time_start.time()
        end_time = self.time_end.time()
        if start_time >= end_time:
            QMessageBox.warning(self, "Warning", "End time must be after start time.")
            return
            
        self.accept()

    def get_exam_data(self):
        return [
            self.exam_name.text().strip(),
            self.class_name.text().strip(),
            self.date.date().toString("yyyy-MM-dd"),
            f"{self.time_start.time().toString('HH:mm')} - {self.time_end.time().toString('HH:mm')}",
            self.lab.currentText(),
            self.supervisor.text().strip(),
            "Scheduled"
        ]

class PracticalExamsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Practical Exam Schedule")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage computer-based examinations")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Filter section
        search_layout = QHBoxLayout()
        
        # Search bar
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

        # Filter dropdown
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All Status", "Scheduled", "In Progress", "Completed"])
        self.status_filter.currentTextChanged.connect(self.filter_by_status)
        
        # Schedule Exam button
        schedule_btn = QPushButton("Schedule Exam")
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
        schedule_btn.clicked.connect(self.schedule_exam)

        # Delete Exam button
        delete_btn = QPushButton("Delete Exam")
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
        delete_btn.clicked.connect(self.delete_exam)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.status_filter)
        search_layout.addWidget(schedule_btn)
        search_layout.addWidget(delete_btn)
        layout.addLayout(search_layout)

        # Exams table
        self.exams_table = QTableWidget()
        self.exams_table.setColumnCount(8)
        self.exams_table.setHorizontalHeaderLabels([
            "Exam Name", "Class", "Date", "Time", "Lab", "Supervisor", "Status", "Actions"
        ])
        self.exams_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.exams_table.setSortingEnabled(True)

        # Sample data
        self.sample_data = [
            ["Computer Science Mid-Term", "10A", "2023-10-20", "09:00 - 11:00", "Lab A", "Mr. Richards", "Scheduled"],
            ["Programming Practical", "11B", "2023-10-22", "13:00 - 15:00", "Lab B", "Ms. Zhang", "Scheduled"],
            ["Web Development Project Submission", "12A", "2023-10-25", "09:00 - 11:00", "Lab C", "Mrs. Patel", "Scheduled"],
            ["Computer Basics Quiz", "9C", "2023-09-28", "10:00 - 12:00", "Lab A", "Mr. Thompson", "Completed"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.exams_table)

    def populate_table(self, data):
        self.exams_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col == 2:  # Make date column sortable
                    item.setData(Qt.ItemDataRole.UserRole, QDate.fromString(value, "yyyy-MM-dd"))
                elif col == 3:  # Make time column sortable
                    time_start = value.split(" - ")[0]
                    item.setData(Qt.ItemDataRole.UserRole, QTime.fromString(time_start, "HH:mm"))
                
                # Center align all cells
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Make items read-only
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Set status color
                if col == 6:  # Status column
                    if value == "Completed":
                        item.setForeground(Qt.GlobalColor.green)
                    elif value == "In Progress":
                        item.setForeground(Qt.GlobalColor.blue)
                    else:  # Scheduled
                        item.setForeground(Qt.GlobalColor.gray)
                
                self.exams_table.setItem(row, col, item)
            
            # Add Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a73e8;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #1557b0;
                }
            """)
            update_btn.clicked.connect(lambda checked, row=row: self.manage_exam(row))
            
            # Create a widget to center the button
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.addWidget(update_btn)
            button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_layout.setContentsMargins(0, 0, 0, 0)
            
            self.exams_table.setCellWidget(row, 7, button_widget)

        # Sort by date and time
        self.exams_table.sortItems(2)  # Sort by date column
        self.exams_table.sortItems(3)  # Then sort by time

    def search_exams(self):
        search_text = self.search_box.text().lower()
        for row in range(self.exams_table.rowCount()):
            should_show = False
            for col in range(self.exams_table.columnCount() - 1):  # Exclude Actions column
                item = self.exams_table.item(row, col)
                if item and search_text in item.text().lower():
                    should_show = True
                    break
            self.exams_table.setRowHidden(row, not should_show)

    def filter_by_status(self, status):
        status = "" if status == "All Status" else status
        for row in range(self.exams_table.rowCount()):
            status_item = self.exams_table.item(row, 6)
            should_show = not status or (status_item and status == status_item.text())
            self.exams_table.setRowHidden(row, not should_show)

    def schedule_exam(self):
        dialog = AddExamDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_exam = dialog.get_exam_data()
            
            # Check for time conflicts
            date = new_exam[2]
            time_range = new_exam[3]
            lab = new_exam[4]
            
            for existing_exam in self.sample_data:
                if (existing_exam[2] == date and 
                    existing_exam[3] == time_range and 
                    existing_exam[4] == lab):
                    QMessageBox.warning(
                        self,
                        "Scheduling Conflict",
                        f"There is already an exam scheduled in {lab} at {time_range} on {date}."
                    )
                    return
            
            self.sample_data.append(new_exam)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Exam scheduled successfully!")

    def delete_exam(self):
        current_row = self.exams_table.currentRow()
        if current_row >= 0:
            exam_name = self.exams_table.item(current_row, 0).text()
            date = self.exams_table.item(current_row, 2).text()
            time = self.exams_table.item(current_row, 3).text()
            
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete the exam:\n\n"
                f"Exam: {exam_name}\n"
                f"Date: {date}\n"
                f"Time: {time}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.exams_table.removeRow(current_row)
                self.sample_data.pop(current_row)
                QMessageBox.information(self, "Success", "Exam deleted successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please select an exam to delete.")

    def manage_exam(self, row):
        exam_name = self.exams_table.item(row, 0).text()
        current_status = self.exams_table.item(row, 6).text()
        
        if current_status == "Completed":
            QMessageBox.information(
                self,
                "View Exam Details",
                f"Exam: {exam_name}\n"
                f"Status: {current_status}\n\n"
                "This exam has been completed."
            )
            return
        
        new_status = "In Progress" if current_status == "Scheduled" else "Completed"
        
        confirm = QMessageBox.question(
            self,
            "Update Exam Status",
            f"Would you like to mark {exam_name} as {new_status}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.sample_data[row][6] = new_status
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", f"Exam status updated to {new_status}!")

class ComputerDepartment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System - Computer Department")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menubar
        menubar = self.menuBar()
        departments_menu = menubar.addMenu("Departments")
        
        # Add Computer Department action
        computer_action = QAction("Computer Department", self)
        departments_menu.addAction(computer_action)
        
        # Add separator and exit action
        departments_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        departments_menu.addAction(exit_action)

        # Create tab buttons
        tab_layout = QHBoxLayout()
        self.tab_buttons = []
        tabs = ["Hardware Inventory", "Software Inventory", "Lab Classes", "Practical Exams"]
        
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
        self.hardware_inventory_page = HardwareInventoryPage()
        self.software_inventory_page = SoftwareInventoryPage()
        self.lab_classes_page = LabClassesPage()
        self.practical_exams_page = PracticalExamsPage()
        
        self.stack.addWidget(self.hardware_inventory_page)
        self.stack.addWidget(self.software_inventory_page)
        self.stack.addWidget(self.lab_classes_page)
        self.stack.addWidget(self.practical_exams_page)

    def switch_tab(self, index):
        # Update button states
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)
        
        # Switch page
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ComputerDepartment()
    window.show()
    sys.exit(app.exec())
