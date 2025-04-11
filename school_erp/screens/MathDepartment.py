import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, QMenuBar,
                           QMenu, QTableWidget, QTableWidgetItem, QHeaderView,
                           QStackedWidget, QFileDialog, QMessageBox, QDialog,
                           QFormLayout, QDateEdit, QComboBox, QSpinBox,
                           QFrame, QDoubleSpinBox, QTabWidget, QGroupBox,
                           QGridLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QAction
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from datetime import datetime

class AddTextbookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Textbook")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.title = QLineEdit()
        self.grade = QComboBox()
        self.grade.addItems(["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        self.publisher = QLineEdit()
        self.quantity = QSpinBox()
        self.quantity.setRange(1, 1000)
        self.condition = QComboBox()
        self.condition.addItems(["Good", "Needs Replacement"])

        # Add fields to form
        layout.addRow("Title:", self.title)
        layout.addRow("Grade:", self.grade)
        layout.addRow("Publisher:", self.publisher)
        layout.addRow("Quantity:", self.quantity)
        layout.addRow("Condition:", self.condition)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_textbook_data(self):
        return [
            self.title.text(),
            self.publisher.text(),
            str(self.quantity.value()),
            self.condition.currentText(),
            datetime.now().strftime("%Y-%m-%d")
        ]

class TextbooksPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Mathematics Textbooks")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage textbooks and reference materials")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)  # Reduce spacing between cards
        
        # Total Textbooks Card
        total_card = QFrame()
        total_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
                max-width: 160px;
                min-width: 160px;
            }
        """)
        total_layout = QVBoxLayout(total_card)
        total_layout.setSpacing(2)
        total_layout.setContentsMargins(8, 6, 8, 6)
        
        total_icon = QLabel("📚")
        total_icon.setStyleSheet("font-size: 16px;")
        self.total_value = QLabel("45")
        self.total_value.setStyleSheet("font-size: 18px; font-weight: bold;")
        total_label = QLabel("Total Textbooks")
        total_label.setStyleSheet("color: gray; font-size: 11px;")
        
        total_layout.addWidget(total_icon)
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)

        # Available Textbooks Card
        available_card = QFrame()
        available_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
                max-width: 160px;
                min-width: 160px;
            }
        """)
        available_layout = QVBoxLayout(available_card)
        available_layout.setSpacing(2)
        available_layout.setContentsMargins(8, 6, 8, 6)
        
        available_icon = QLabel("✅")
        available_icon.setStyleSheet("font-size: 16px;")
        self.available_value = QLabel("38")
        self.available_value.setStyleSheet("font-size: 18px; font-weight: bold;")
        available_label = QLabel("Available Textbooks")
        available_label.setStyleSheet("color: gray; font-size: 11px;")
        
        available_layout.addWidget(available_icon)
        available_layout.addWidget(self.available_value)
        available_layout.addWidget(available_label)

        # Need of Textbooks Card
        need_card = QFrame()
        need_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
                max-width: 160px;
                min-width: 160px;
            }
        """)
        need_layout = QVBoxLayout(need_card)
        need_layout.setSpacing(2)
        need_layout.setContentsMargins(8, 6, 8, 6)
        
        need_icon = QLabel("⚠️")
        need_icon.setStyleSheet("font-size: 16px;")
        self.need_value = QLabel("7")
        self.need_value.setStyleSheet("font-size: 18px; font-weight: bold;")
        need_label = QLabel("Need of Textbooks")
        need_label.setStyleSheet("color: gray; font-size: 11px;")
        
        need_layout.addWidget(need_icon)
        need_layout.addWidget(self.need_value)
        need_layout.addWidget(need_label)

        # Need Replacement Card
        replacement_card = QFrame()
        replacement_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
                max-width: 160px;
                min-width: 160px;
            }
        """)
        replacement_layout = QVBoxLayout(replacement_card)
        replacement_layout.setSpacing(2)
        replacement_layout.setContentsMargins(8, 6, 8, 6)
        
        replacement_icon = QLabel("🔄")
        replacement_icon.setStyleSheet("font-size: 16px;")
        self.replacement_value = QLabel("5")
        self.replacement_value.setStyleSheet("font-size: 18px; font-weight: bold;")
        replacement_label = QLabel("Need Replacement")
        replacement_label.setStyleSheet("color: gray; font-size: 11px;")
        
        replacement_layout.addWidget(replacement_icon)
        replacement_layout.addWidget(self.replacement_value)
        replacement_layout.addWidget(replacement_label)

        stats_layout.addWidget(total_card)
        stats_layout.addWidget(available_card)
        stats_layout.addWidget(need_card)
        stats_layout.addWidget(replacement_card)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Search and Action section
        search_layout = QHBoxLayout()
        
        # Search bar with icon
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
        """)
        search_layout_inner = QHBoxLayout(search_container)
        search_layout_inner.setContentsMargins(10, 5, 10, 5)
        
        search_icon = QLabel("🔍")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search textbooks...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_textbooks)
        
        search_layout_inner.addWidget(search_icon)
        search_layout_inner.addWidget(self.search_box)

        # Grade filter
        self.grade_filter = QComboBox()
        self.grade_filter.addItems(["All Grades", "Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)])
        self.grade_filter.currentTextChanged.connect(self.filter_by_grade)
        self.grade_filter.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 120px;
            }
        """)

        # Buttons container
        buttons_container = QFrame()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)

        add_btn = QPushButton("Add Textbook")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        add_btn.clicked.connect(self.add_textbook)

        delete_btn = QPushButton("Delete Textbook")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(self.delete_textbook)

        order_btn = QPushButton("Order Supplies")
        order_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        order_btn.clicked.connect(self.generate_order_pdf)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(order_btn)

        search_layout.addWidget(search_container)
        search_layout.addWidget(self.grade_filter)
        search_layout.addWidget(buttons_container)
        layout.addLayout(search_layout)

        # Textbooks table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Title", "Publisher", "Quantity", "Condition", "Last Inventory", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data
        self.sample_data = [
            ["Mathematics Nursery", "Pearson Education", "30", "Good", "2023-09-10"],
            ["Mathematics LKG", "Pearson Education", "35", "Good", "2023-09-10"],
            ["Mathematics UKG", "Pearson Education", "40", "Good", "2023-09-10"],
            ["Mathematics Grade 1", "Pearson Education", "42", "Good", "2023-09-10"],
            ["Mathematics Grade 2", "Pearson Education", "45", "Good", "2023-09-10"],
            ["Mathematics Grade 3", "Pearson Education", "48", "Good", "2023-09-10"],
            ["Mathematics Grade 4", "Pearson Education", "50", "Good", "2023-09-10"],
            ["Mathematics Grade 5", "Pearson Education", "52", "Good", "2023-09-10"],
            ["Mathematics Grade 6", "Pearson Education", "45", "Good", "2023-09-10"],
            ["Mathematics Grade 7", "Pearson Education", "50", "Good", "2023-09-10"],
            ["Mathematics Grade 8", "Pearson Education", "48", "Good", "2023-09-10"],
            ["Mathematics Grade 9", "Pearson Education", "52", "Good", "2023-09-10"],
            ["Algebra & Calculus Grade 10", "Oxford Publications", "40", "Needs Replacement", "2023-09-10"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.table)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col == 2:  # Quantity column
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
                
                # Color code the condition
                if col == 3:
                    if value == "Good":
                        item.setForeground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setForeground(Qt.GlobalColor.darkYellow)
            
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
            update_btn.clicked.connect(lambda checked, row=row: self.update_textbook(row))
            self.table.setCellWidget(row, 5, update_btn)

        # Update stats
        self.update_stats()

    def search_textbooks(self):
        search_text = self.search_box.text().lower()
        grade_filter = self.grade_filter.currentText()
        
        for row in range(self.table.rowCount()):
            title = self.table.item(row, 0).text().lower()
            publisher = self.table.item(row, 1).text().lower()
            
            title_match = search_text in title or search_text in publisher
            grade_match = grade_filter == "All Grades" or grade_filter in title
            
            self.table.setRowHidden(row, not (title_match and grade_match))

    def filter_by_grade(self, grade):
        if grade == "All Grades":
            self.populate_table(self.sample_data)
            return

        filtered_data = [
            row for row in self.sample_data
            if grade in row[0]  # Check if grade appears in the title
        ]
        self.populate_table(filtered_data)
        
        # Update stats for filtered data
        total_books = sum(int(row[2]) for row in filtered_data)
        available_books = sum(int(row[2]) for row in filtered_data if row[3] == "Good")
        needed_books = total_books - available_books
        replacement_books = sum(int(row[2]) for row in filtered_data if row[3] == "Needs Replacement")
        
        self.total_value.setText(str(total_books))
        self.available_value.setText(str(available_books))
        self.need_value.setText(str(needed_books))
        self.replacement_value.setText(str(replacement_books))

        # Show summary message
        QMessageBox.information(
            self,
            f"{grade} Books",
            f"Total Books: {total_books}\n"
            f"Available Books: {available_books}\n"
            f"Needed Books: {needed_books}\n"
            f"Books Needing Replacement: {replacement_books}"
        )

    def add_textbook(self):
        dialog = AddTextbookDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_textbook = dialog.get_textbook_data()
            self.sample_data.append(new_textbook)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Textbook added successfully!")

    def update_textbook(self, row):
        current_data = [
            self.table.item(row, col).text()
            for col in range(self.table.columnCount() - 1)
        ]
        
        dialog = AddTextbookDialog(self)
        dialog.title.setText(current_data[0])
        dialog.publisher.setText(current_data[1])
        dialog.quantity.setValue(int(current_data[2]))
        dialog.condition.setCurrentText(current_data[3])
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_textbook_data()
            self.sample_data[row] = updated_data
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Textbook updated successfully!")

    def delete_textbook(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a textbook to delete.")
            return

        row = selected_rows[0].row()
        textbook_name = self.table.item(row, 0).text()

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{textbook_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            del self.sample_data[row]
            QMessageBox.information(self, "Success", f"'{textbook_name}' has been deleted successfully.")

    def update_stats(self):
        # Update total textbooks
        total_books = sum(int(row[2]) for row in self.sample_data)
        self.total_value.setText(str(total_books))
        
        # Update available textbooks (those in "Good" condition)
        available_books = sum(int(row[2]) for row in self.sample_data if row[3] == "Good")
        self.available_value.setText(str(available_books))
        
        # Update need of textbooks (difference between required and available)
        needed_books = total_books - available_books
        self.need_value.setText(str(needed_books))
        
        # Update need replacement (those marked as "Needs Replacement")
        replacement_books = sum(int(row[2]) for row in self.sample_data if row[3] == "Needs Replacement")
        self.replacement_value.setText(str(replacement_books))

    def generate_order_pdf(self):
        try:
            # Ask user for save location
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save Order List PDF",
                os.path.expanduser("~/Documents"),  # Default to Documents folder
                "PDF Files (*.pdf)"
            )
            
            if not file_name:  # User cancelled
                return
                
            # Add .pdf extension if not present
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'

            # Create PDF document
            doc = SimpleDocTemplate(file_name, pagesize=letter)
            elements = []
            
            # Add title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1
            )
            elements.append(Paragraph("Textbook Order List", title_style))
            elements.append(Spacer(1, 20))
            
            # Add date
            date_style = ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=1
            )
            elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", date_style))
            elements.append(Spacer(1, 30))
            
            # Group books by grade
            grade_books = {}
            for row in self.sample_data:
                if row[3] != "Good":
                    # Extract grade from title
                    grade = "Unknown"
                    for g in ["Nursery", "LKG", "UKG"] + [f"Grade {i}" for i in range(1, 11)]:
                        if g in row[0]:
                            grade = g
                            break
                    
                    if grade not in grade_books:
                        grade_books[grade] = []
                    grade_books[grade].append(row)
            
            if not grade_books:
                elements.append(Paragraph("No textbooks currently need ordering.", styles['Normal']))
            else:
                # Add each grade's books
                for grade in sorted(grade_books.keys()):
                    # Add grade header
                    elements.append(Paragraph(f"{grade} Textbooks", styles['Heading2']))
                    elements.append(Spacer(1, 10))
                    
                    # Create table for this grade
                    grade_data = [["Title", "Current Quantity", "Condition", "Required Quantity"]]
                    for row in grade_books[grade]:
                        grade_data.append([
                            row[0],  # Title
                            row[2],  # Current Quantity
                            row[3],  # Condition
                            str(int(int(row[2]) * 1.5))  # Required Quantity (50% more than current)
                        ])
                    
                    table = Table(grade_data, colWidths=[250, 100, 100, 100])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
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
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 20))
            
            # Add summary
            elements.append(Spacer(1, 20))
            summary_text = [
                Paragraph("Order Summary:", styles['Heading3']),
                Paragraph(f"Total Grades Needing Books: {len(grade_books)}", styles['Normal']),
                Paragraph(f"Total Books to Order: {sum(len(books) for books in grade_books.values())}", styles['Normal'])
            ]
            elements.extend(summary_text)
            
            # Build PDF
            doc.build(elements)
            
            # Show success message with file location
            QMessageBox.information(
                self,
                "Success",
                f"Order list PDF generated successfully!\nSaved as: {file_name}"
            )
            
            # Open the containing folder
            if sys.platform == 'win32':
                os.startfile(os.path.dirname(file_name))
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{os.path.dirname(file_name)}"')
            else:  # Linux
                os.system(f'xdg-open "{os.path.dirname(file_name)}"')
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error generating PDF: {str(e)}"
            )

class AddEquipmentDialog(QDialog):
    def __init__(self, parent=None, equipment_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Equipment")
        self.setModal(True)
        self.equipment_data = equipment_data
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.equipment_name = QLineEdit()
        self.quantity = QSpinBox()
        self.quantity.setRange(1, 1000)
        self.condition = QComboBox()
        self.condition.addItems(["Good", "Needs Batteries", "Needs Replacement"])
        self.notes = QLineEdit()

        # Add fields to form
        layout.addRow("Equipment Name:", self.equipment_name)
        layout.addRow("Quantity:", self.quantity)
        layout.addRow("Condition:", self.condition)
        layout.addRow("Notes:", self.notes)

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
        if self.equipment_data:
            self.equipment_name.setText(self.equipment_data[0])
            self.quantity.setValue(int(self.equipment_data[1]))
            self.condition.setCurrentText(self.equipment_data[3])
            self.notes.setText(self.equipment_data[4])

    def get_equipment_data(self):
        return [
            self.equipment_name.text(),
            str(self.quantity.value()),
            datetime.now().strftime("%Y-%m-%d"),
            self.condition.currentText(),
            self.notes.text()
        ]

class TeachingEquipmentPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Teaching Equipment")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage mathematics teaching tools and equipment")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Stats Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
        
        # Common style for all cards
        card_style = """
            QFrame {
                background-color: white;
                border-radius: 6px;
                padding: 6px;
                margin: 2px;
                max-width: 150px;
                min-width: 150px;
            }
        """
        
        # Common layout settings for all cards
        def setup_card_layout(layout):
            layout.setSpacing(2)
            layout.setContentsMargins(6, 4, 6, 4)
        
        # Common style for icons, values, and labels
        icon_style = "font-size: 14px;"
        value_style = "font-size: 16px; font-weight: bold;"
        label_style = "color: gray; font-size: 10px;"

        # Total Equipment Card
        total_card = QFrame()
        total_card.setStyleSheet(card_style)
        total_layout = QVBoxLayout(total_card)
        setup_card_layout(total_layout)
        
        total_icon = QLabel("📊")
        total_icon.setStyleSheet(icon_style)
        self.total_value = QLabel("285")
        self.total_value.setStyleSheet(value_style)
        total_label = QLabel("Total Equipment")
        total_label.setStyleSheet(label_style)
        
        total_layout.addWidget(total_icon)
        total_layout.addWidget(self.total_value)
        total_layout.addWidget(total_label)
        
        # Categories Card
        categories_card = QFrame()
        categories_card.setStyleSheet(card_style)
        categories_layout = QVBoxLayout(categories_card)
        setup_card_layout(categories_layout)
        
        categories_icon = QLabel("🔄")
        categories_icon.setStyleSheet(icon_style)
        self.categories_value = QLabel("7")
        self.categories_value.setStyleSheet(value_style)
        categories_label = QLabel("Categories")
        categories_label.setStyleSheet(label_style)
        
        categories_layout.addWidget(categories_icon)
        categories_layout.addWidget(self.categories_value)
        categories_layout.addWidget(categories_label)
        
        # Need Attention Card
        attention_card = QFrame()
        attention_card.setStyleSheet(card_style)
        attention_layout = QVBoxLayout(attention_card)
        setup_card_layout(attention_layout)
        
        attention_icon = QLabel("⚠️")
        attention_icon.setStyleSheet(icon_style)
        self.attention_value = QLabel("2")
        self.attention_value.setStyleSheet(value_style)
        attention_label = QLabel("Need Attention")
        attention_label.setStyleSheet(label_style)
        
        attention_layout.addWidget(attention_icon)
        attention_layout.addWidget(self.attention_value)
        attention_layout.addWidget(attention_label)
        
        stats_layout.addWidget(total_card)
        stats_layout.addWidget(categories_card)
        stats_layout.addWidget(attention_card)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Search and Action section
        search_layout = QHBoxLayout()
        
        # Search bar with icon
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
        """)
        search_layout_inner = QHBoxLayout(search_container)
        search_layout_inner.setContentsMargins(10, 5, 10, 5)
        
        search_icon = QLabel("🔍")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search equipment...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_equipment)
        
        search_layout_inner.addWidget(search_icon)
        search_layout_inner.addWidget(self.search_box)

        # Add and Delete Equipment buttons
        buttons_container = QFrame()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)

        add_btn = QPushButton("Add Equipment")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        add_btn.clicked.connect(self.add_equipment)

        delete_btn = QPushButton("Delete Equipment")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(self.delete_equipment)

        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(delete_btn)

        search_layout.addWidget(search_container)
        search_layout.addWidget(buttons_container)
        layout.addLayout(search_layout)

        # Equipment table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Equipment", "Quantity", "Last Checked", "Condition", "Notes", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data
        self.sample_data = [
            ["Geometry Kits", "60", "2023-09-15", "Good", "Complete sets"],
            ["Graph Papers (Pack of 100)", "25", "2023-09-15", "Good", "All sizes available"],
            ["Rulers & Set Squares", "70", "2023-09-15", "Good", "Various sizes"],
            ["Compasses", "55", "2023-09-15", "Good", "Metal quality"],
            ["Scientific Calculators", "40", "2023-08-20", "Needs Batteries", "TI-84 Models"],
            ["3D Geometry Models", "15", "2023-08-25", "Good", "Various shapes"],
            ["Mathematical Manipulatives", "20", "2023-08-25", "Good", "For algebra teaching"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.table)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col == 1:  # Quantity column
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
                
                # Color code the condition
                if col == 3:
                    if value == "Good":
                        item.setForeground(Qt.GlobalColor.darkGreen)
                    else:
                        item.setForeground(Qt.GlobalColor.darkYellow)
            
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
            update_btn.clicked.connect(lambda checked, row=row: self.update_equipment(row))
            self.table.setCellWidget(row, 5, update_btn)

        # Update stats
        self.update_stats()

    def update_stats(self):
        total_items = sum(int(row[1]) for row in self.sample_data)
        self.total_value.setText(str(total_items))
        
        categories = len(self.sample_data)
        self.categories_value.setText(str(categories))
        
        need_attention = sum(1 for row in self.sample_data if row[3] != "Good")
        self.attention_value.setText(str(need_attention))

    def search_equipment(self):
        search_text = self.search_box.text().lower()
        
        for row in range(self.table.rowCount()):
            equipment = self.table.item(row, 0).text().lower()
            notes = self.table.item(row, 4).text().lower()
            
            should_show = search_text in equipment or search_text in notes
            self.table.setRowHidden(row, not should_show)

    def add_equipment(self):
        dialog = AddEquipmentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_equipment = dialog.get_equipment_data()
            self.sample_data.append(new_equipment)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Equipment added successfully!")

    def update_equipment(self, row):
        current_data = [
            self.table.item(row, col).text()
            for col in range(self.table.columnCount() - 1)
        ]
        
        dialog = AddEquipmentDialog(self, current_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_equipment_data()
            self.sample_data[row] = updated_data
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Equipment updated successfully!")

    def delete_equipment(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select equipment to delete.")
            return

        row = selected_rows[0].row()
        equipment_name = self.table.item(row, 0).text()

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{equipment_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            del self.sample_data[row]
            self.update_stats()
            QMessageBox.information(self, "Success", f"'{equipment_name}' has been deleted successfully.")

class CreateLessonPlanDialog(QDialog):
    def __init__(self, parent=None, lesson_data=None):
        super().__init__(parent)
        self.setWindowTitle("Create/Update Lesson Plan")
        self.setModal(True)
        self.lesson_data = lesson_data
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.title = QLineEdit()
        self.resource_book = QLineEdit()
        self.grade = QComboBox()
        self.grade.addItems(["Nursery", "LKG", "UKG"] + [f"{i}th" for i in range(1, 11)])
        self.teacher = QLineEdit()
        
        # Topics covered
        topics_group = QGroupBox("Topics Covered")
        topics_layout = QVBoxLayout()
        self.topics = QLineEdit()
        self.topics.setPlaceholderText("Enter topics separated by commas")
        topics_layout.addWidget(self.topics)
        topics_group.setLayout(topics_layout)
        
        # Learning objectives
        objectives_group = QGroupBox("Learning Objectives")
        objectives_layout = QVBoxLayout()
        self.objectives = QLineEdit()
        self.objectives.setPlaceholderText("Enter objectives separated by commas")
        objectives_layout.addWidget(self.objectives)
        objectives_group.setLayout(objectives_layout)

        # Add fields to form
        layout.addRow("Title:", self.title)
        layout.addRow("Resource Book:", self.resource_book)
        layout.addRow("Grade:", self.grade)
        layout.addRow("Teacher:", self.teacher)
        layout.addRow(topics_group)
        layout.addRow(objectives_group)

        # If editing, populate fields with existing data
        if self.lesson_data:
            self.title.setText(self.lesson_data[0])
            self.resource_book.setText(self.lesson_data[1])
            self.grade.setCurrentText(self.lesson_data[2])
            self.teacher.setText(self.lesson_data[3])
            if len(self.lesson_data) > 6:  # If we have topics and objectives
                self.topics.setText(self.lesson_data[6])
                self.objectives.setText(self.lesson_data[7])

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_lesson_plan_data(self):
        return [
            self.title.text(),
            self.resource_book.text(),
            self.grade.currentText(),
            self.teacher.text(),
            datetime.now().strftime("%Y-%m-%d %H:%M"),  # Current date and time
            self.topics.text(),
            self.objectives.text()
        ]

class LessonPlansPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Lesson Plans & Syllabi")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        subtitle = QLabel("Manage curriculum materials and teaching plans")
        subtitle.setStyleSheet("color: gray;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Search and Action section
        search_layout = QHBoxLayout()
        
        # Search bar with icon
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
        """)
        search_layout_inner = QHBoxLayout(search_container)
        search_layout_inner.setContentsMargins(10, 5, 10, 5)
        
        search_icon = QLabel("🔍")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search lesson plans...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 5px;
                min-width: 300px;
            }
        """)
        self.search_box.textChanged.connect(self.search_lessons)
        
        search_layout_inner.addWidget(search_icon)
        search_layout_inner.addWidget(self.search_box)

        # Grade filter
        self.grade_filter = QComboBox()
        self.grade_filter.addItems(["All Grades", "Nursery", "LKG", "UKG"] + [f"{i}th" for i in range(1, 11)])
        self.grade_filter.currentTextChanged.connect(self.filter_by_grade)
        self.grade_filter.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-width: 120px;
            }
        """)

        # Create Lesson Plan button
        create_btn = QPushButton("Create Lesson Plan")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        create_btn.clicked.connect(self.create_lesson_plan)

        # Delete Lesson Plan button
        delete_btn = QPushButton("Delete Lesson Plan")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_btn.clicked.connect(self.delete_lesson_plan)

        search_layout.addWidget(search_container)
        search_layout.addWidget(self.grade_filter)
        search_layout.addStretch()
        search_layout.addWidget(create_btn)
        search_layout.addWidget(delete_btn)
        layout.addLayout(search_layout)

        # Lesson Plans table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Title", "Resource Book", "Grade", "Teacher", "Last Updated", "Actions"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Title column stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Resource Book column stretches
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)    # Grade column fixed
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)    # Teacher column fixed
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)    # Last Updated column fixed
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)    # Actions column fixed
        
        self.table.setColumnWidth(2, 100)   # Grade
        self.table.setColumnWidth(3, 150)   # Teacher
        self.table.setColumnWidth(4, 150)   # Last Updated
        self.table.setColumnWidth(5, 200)   # Actions

        # Sample data with current timestamp and resource books
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.sample_data = [
            ["Algebra Fundamentals", "Mathematics for Class 8 - NCERT", "8th", "Ms. Johnson", current_time, "Topics covered: Algebraic Expressions, Linear Equations"],
            ["Geometry Basics", "Mathematics for Class 9 - NCERT", "9th", "Mr. Williams", current_time, "Topics covered: Lines and Angles, Triangles"],
            ["Trigonometry Introduction", "Mathematics for Class 10 - NCERT", "10th", "Mrs. Davis", current_time, "Topics covered: Trigonometric Ratios, Heights and Distances"]
        ]
        
        self.populate_table(self.sample_data)
        layout.addWidget(self.table)

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data[:5]):  # Only first 5 columns, last column is for buttons
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

            # Create button container widget
            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.setContentsMargins(5, 2, 5, 2)
            button_layout.setSpacing(5)

            # Update button
            update_btn = QPushButton("Update")
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            update_btn.clicked.connect(lambda checked, row=row: self.update_lesson_plan(row))

            # View button
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
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
            view_btn.clicked.connect(lambda checked, row=row: self.view_lesson_plan(row))

            # Add buttons to layout
            button_layout.addWidget(update_btn)
            button_layout.addWidget(view_btn)
            button_layout.addStretch()

            # Set the widget as the cell widget
            self.table.setCellWidget(row, 5, button_container)

    def update_lesson_plan(self, row):
        current_data = [self.table.item(row, col).text() for col in range(5)]
        current_data.extend(["", ""])  # Empty topics and objectives if not previously set
        
        dialog = CreateLessonPlanDialog(self, current_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_lesson_plan_data()
            self.sample_data[row] = updated_data
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Lesson plan updated successfully!")

    def view_lesson_plan(self, row):
        lesson_data = [self.table.item(row, col).text() for col in range(5)]
        
        msg = QMessageBox()
        msg.setWindowTitle("Lesson Plan Details")
        msg.setText(f"Title: {lesson_data[0]}\n"
                   f"Resource Book: {lesson_data[1]}\n"
                   f"Grade: {lesson_data[2]}\n"
                   f"Teacher: {lesson_data[3]}\n"
                   f"Last Updated: {lesson_data[4]}\n\n"
                   f"This lesson plan was last modified on {lesson_data[4]}.\n"
                   f"The timestamp shows when the plan was created or last updated.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def search_lessons(self):
        search_text = self.search_box.text().lower()
        grade_filter = self.grade_filter.currentText()
        
        for row in range(self.table.rowCount()):
            title = self.table.item(row, 0).text().lower()
            grade = self.table.item(row, 2).text()
            teacher = self.table.item(row, 3).text().lower()
            
            title_match = search_text in title or search_text in teacher
            grade_match = grade_filter == "All Grades" or grade_filter == grade
            
            self.table.setRowHidden(row, not (title_match and grade_match))

    def filter_by_grade(self, grade):
        self.search_lessons()

    def create_lesson_plan(self):
        dialog = CreateLessonPlanDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_lesson = dialog.get_lesson_plan_data()
            self.sample_data.append(new_lesson)
            self.populate_table(self.sample_data)
            QMessageBox.information(self, "Success", "Lesson plan created successfully!")

    def delete_lesson_plan(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a lesson plan to delete.")
            return

        row = selected_items[0].row()
        lesson_title = self.table.item(row, 0).text()

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the lesson plan '{lesson_title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            del self.sample_data[row]
            QMessageBox.information(self, "Success", f"Lesson plan '{lesson_title}' has been deleted successfully.")

class AddEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Event")
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Create form fields
        self.title = QLineEdit()
        self.event_type = QComboBox()
        self.event_type.addItems(["Competition", "Workshop", "Celebration"])
        self.organizer = QLineEdit()
        self.participants = QLineEdit()
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())
        
        # Time fields
        time_layout = QHBoxLayout()
        self.start_time = QLineEdit()
        self.start_time.setPlaceholderText("HH:MM")
        self.end_time = QLineEdit()
        self.end_time.setPlaceholderText("HH:MM")
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(QLabel("-"))
        time_layout.addWidget(self.end_time)
        
        self.location = QLineEdit()

        # Add fields to form
        layout.addRow("Title:", self.title)
        layout.addRow("Event Type:", self.event_type)
        layout.addRow("Organizer:", self.organizer)
        layout.addRow("Participants:", self.participants)
        layout.addRow("Date:", self.date)
        layout.addRow("Time:", time_layout)
        layout.addRow("Location:", self.location)

        # Add buttons
        button_box = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        button_box.addWidget(save_btn)
        button_box.addWidget(cancel_btn)
        layout.addRow("", button_box)

    def get_event_data(self):
        time_str = f"{self.start_time.text()} - {self.end_time.text()}" if self.start_time.text() else "All Day"
        return [
            self.title.text(),
            self.event_type.currentText(),
            self.organizer.text(),
            self.participants.text(),
            self.date.date().toString("yyyy-MM-dd"),
            time_str,
            self.location.text()
        ]

class EventsRecordsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header text
        subtitle = QLabel("Track mathematics competitions, events, and activities")
        subtitle.setStyleSheet("color: gray;")
        layout.addWidget(subtitle)

        # Search and Filter Bar
        top_bar = QHBoxLayout()
        
        # Search box with icon
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(10, 5, 10, 5)
        
        search_icon = QLabel("🔍")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search events...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 5px;
                min-width: 300px;
            }
        """)
        self.search_input.textChanged.connect(self.filter_events)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input)

        # Event type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(["Celebrations", "All Events", "Competitions", "Workshops"])
        self.type_filter.setStyleSheet("""
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                min-width: 150px;
            }
        """)
        self.type_filter.currentTextChanged.connect(self.filter_events)

        # Add Event button
        add_btn = QPushButton("Add Event")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        add_btn.clicked.connect(self.add_event)

        top_bar.addWidget(search_frame)
        top_bar.addWidget(self.type_filter)
        top_bar.addStretch()
        top_bar.addWidget(add_btn)
        layout.addLayout(top_bar)

        # Events List
        self.events_list = QVBoxLayout()
        self.events_list.setSpacing(10)
        
        # Sample events
        self.events = [
            {
                "type": "Competition",
                "title": "Math Olympiad Training",
                "organizer": "Dr. Smith",
                "participants": "Selected students",
                "date": "2023-10-15",
                "time": "14:00 - 16:00",
                "location": "Math Lab"
            },
            {
                "type": "Celebration",
                "title": "Pi Day Celebration",
                "organizer": "Math Department",
                "participants": "All Students",
                "date": "2024-03-14",
                "time": "All Day",
                "location": "School Auditorium"
            }
        ]
        
        # Create event cards
        self.refresh_events()
        layout.addLayout(self.events_list)
        layout.addStretch()

    def create_event_card(self, event):
        # Main card frame
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        # Main layout
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        
        # Event type badge
        type_label = QLabel(event["type"])
        type_label.setStyleSheet("""
            QLabel {
                background-color: #e9ecef;
                color: #495057;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                max-width: fit-content;
            }
        """)
        card_layout.addWidget(type_label)
        
        # Event title
        title = QLabel(event["title"])
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(title)
        
        # Info section
        info_layout = QHBoxLayout()
        
        # Left column
        left_col = QVBoxLayout()
        
        # Organizer
        organizer_layout = QHBoxLayout()
        organizer_label = QLabel("Organizer")
        organizer_label.setStyleSheet("color: gray;")
        organizer_value = QLabel(event["organizer"])
        organizer_layout.addWidget(organizer_label)
        organizer_layout.addWidget(organizer_value)
        organizer_layout.addStretch()
        left_col.addLayout(organizer_layout)
        
        # Participants
        participants_layout = QHBoxLayout()
        participants_label = QLabel("Participants")
        participants_label.setStyleSheet("color: gray;")
        participants_value = QLabel(event["participants"])
        participants_layout.addWidget(participants_label)
        participants_layout.addWidget(participants_value)
        participants_layout.addStretch()
        left_col.addLayout(participants_layout)
        
        # Event details
        details_layout = QVBoxLayout()
        details_layout.addWidget(QLabel(f"Date: {event['date']}"))
        details_layout.addWidget(QLabel(f"Time: {event['time']}"))
        details_layout.addWidget(QLabel(f"Location: {event['location']}"))
        left_col.addLayout(details_layout)
        
        # Right column
        right_col = QVBoxLayout()
        right_col.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Event Materials
        materials_label = QLabel("Event Materials")
        materials_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_col.addWidget(materials_label)
        
        # Material buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        
        for btn_text in ["Photos", "Documents", "Records"]:
            btn = QPushButton(btn_text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    padding: 5px 15px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #f8f9fa;
                }
            """)
            buttons_layout.addWidget(btn)
        
        right_col.addLayout(buttons_layout)
        
        # Add columns to info layout
        info_layout.addLayout(left_col)
        info_layout.addLayout(right_col)
        card_layout.addLayout(info_layout)
        
        # Manage Event button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        manage_btn = QPushButton("Manage Event")
        manage_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a73e8;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """)
        bottom_layout.addWidget(manage_btn)
        card_layout.addLayout(bottom_layout)
        
        return card

    def refresh_events(self):
        # Clear existing events
        while self.events_list.count():
            item = self.events_list.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Filter events based on search and type
        search_text = self.search_input.text().lower()
        selected_type = self.type_filter.currentText()

        filtered_events = []
        for event in self.events:
            if selected_type in ["All Events", event["type"] + "s"]:
                if (search_text in event["title"].lower() or 
                    search_text in event["organizer"].lower()):
                    filtered_events.append(event)

        # Add filtered events
        for event in filtered_events:
            self.events_list.addWidget(self.create_event_card(event))

    def filter_events(self):
        self.refresh_events()

    def add_event(self):
        dialog = AddEventDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_event_data = dialog.get_event_data()
            new_event = {
                "type": new_event_data[1],
                "title": new_event_data[0],
                "organizer": new_event_data[2],
                "participants": new_event_data[3],
                "date": new_event_data[4],
                "time": new_event_data[5],
                "location": new_event_data[6]
            }
            self.events.append(new_event)
            self.refresh_events()
            QMessageBox.information(self, "Success", "Event added successfully!")

class MathDepartment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math Department - School Management System")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menubar
        menubar = self.menuBar()
        departments_menu = menubar.addMenu("Departments")
        
        # Add Math Department action
        math_action = QAction("Math Department", self)
        departments_menu.addAction(math_action)
        
        # Add separator and exit action
        departments_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        departments_menu.addAction(exit_action)

        # Create tab buttons
        tab_layout = QHBoxLayout()
        self.tab_buttons = []
        tabs = ["Textbooks", "Teaching Equipment", "Lesson Plans", "Events & Records"]
        
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
        self.textbooks_page = TextbooksPage()
        self.teaching_equipment_page = TeachingEquipmentPage()
        self.lesson_plans_page = LessonPlansPage()
        self.events_records_page = EventsRecordsPage()
        
        self.stack.addWidget(self.textbooks_page)
        self.stack.addWidget(self.teaching_equipment_page)
        self.stack.addWidget(self.lesson_plans_page)
        self.stack.addWidget(self.events_records_page)

    def switch_tab(self, index):
        # Update button states
        for i, btn in enumerate(self.tab_buttons):
            btn.setChecked(i == index)
        
        # Switch page
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MathDepartment()
    window.show()
    sys.exit(app.exec())
