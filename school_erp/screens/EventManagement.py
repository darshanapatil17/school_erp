from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QFrame, QMessageBox, QDialog, QFormLayout,
    QDateEdit, QTimeEdit, QSpinBox, QTextEdit, QApplication, QSizePolicy,
    QStackedWidget, QCalendarWidget, QScrollArea, QGroupBox, QGridLayout,
    QHeaderView, QFileDialog
)
from PyQt6.QtCore import (
    Qt, QDate, QTime, QSize, QRect
)
from PyQt6.QtGui import (
    QFont, QColor, QPainter, QTextCharFormat
)
import sys
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
import os

class AddEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Class")
        self.setModal(True)
        self.setFixedSize(300, 400)
        self.setStyleSheet("""
            QDialog {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 8px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 12px;
            }
            QLineEdit, QDateEdit, QTimeEdit, QComboBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-height: 20px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton#closeButton {
                background: transparent;
                border: none;
                padding: 4px;
                font-size: 16px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with close button
        header_layout = QHBoxLayout()
        title = QLabel("Schedule Class")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        close_btn = QPushButton("×")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.reject)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        layout.addLayout(header_layout)

        # Form fields
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_input)

        # Day (read-only, updates based on date)
        self.day_label = QLineEdit()
        self.day_label.setReadOnly(True)
        form_layout.addRow("Day:", self.day_label)

        # Time
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        form_layout.addRow("Time:", self.time_input)

        # Lab
        self.lab_input = QComboBox()
        self.lab_input.addItems(["Lab 1", "Lab 2", "Lab 3"])
        form_layout.addRow("Lab:", self.lab_input)

        # Class
        self.class_input = QComboBox()
        self.class_input.addItems(["Class A", "Class B", "Class C"])
        form_layout.addRow("Class:", self.class_input)

        # Subject
        self.subject_input = QComboBox()
        self.subject_input.addItems(["Mathematics", "Physics", "Chemistry"])
        form_layout.addRow("Subject:", self.subject_input)

        # Teacher
        self.teacher_input = QComboBox()
        self.teacher_input.addItems(["Mr. Smith", "Mrs. Johnson", "Dr. Brown"])
        form_layout.addRow("Teacher:", self.teacher_input)

        layout.addLayout(form_layout)

        # Add some spacing
        layout.addStretch()

        # Buttons at the bottom
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet("""
            background: #2196F3;
            color: white;
        """)
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            background: #e74c3c;
            color: white;
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect date change to day update
        self.date_input.dateChanged.connect(self.update_day)
        self.update_day(self.date_input.date())

    def update_day(self, date):
        day_name = date.toString("dddd")
        self.day_label.setText(day_name)

class ManageEventsDialog(QDialog):
    def __init__(self, events, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Events")
        self.setModal(True)
        self.setMinimumWidth(800)
        self.setMinimumHeight(500)
        self.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        self.setup_ui(events)

    def setup_ui(self, events):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Manage Events")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)

        # Events Section
        events_section = QHBoxLayout()
        events_section.setSpacing(20)

        # Completed Events List
        completed_events = {d: e for d, e in events.items() 
                          if QDate.fromString(d, "yyyy-MM-dd") < QDate.currentDate()}
        completed_list = EventListWidget("Completed Events", completed_events, True)
        events_section.addWidget(completed_list)

        # Upcoming Events List
        upcoming_events = {d: e for d, e in events.items() 
                         if QDate.fromString(d, "yyyy-MM-dd") >= QDate.currentDate()}
        upcoming_list = EventListWidget("Upcoming Events", upcoming_events)
        events_section.addWidget(upcoming_list)

        layout.addLayout(events_section)

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        close_btn.clicked.connect(self.accept)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, events=None):
        super().__init__()
        self.events = events if events else {}
        self.setStyleSheet("""
            QCalendarWidget {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 8px;
            }
            QCalendarWidget QWidget {
                alternate-background-color: transparent;
            }
            /* Navigation bar styling */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #2196F3;
                min-height: 50px;
                max-height: 50px;
            }
            /* Month/Year labels */
            QCalendarWidget QToolButton {
                color: white;
                background: transparent;
                border: none;
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
                padding: 4px 20px;
                min-width: 150px;
            }
            QCalendarWidget QToolButton::menu-indicator {
                image: none;
            }
            /* Navigation arrows */
            QCalendarWidget QToolButton#qt_calendar_prevmonth {
                qproperty-icon: none;
                qproperty-text: "<";
                font-size: 20px;
                padding: 0px 10px;
            }
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                qproperty-icon: none;
                qproperty-text: ">";
                font-size: 20px;
                padding: 0px 10px;
            }
            QCalendarWidget QSpinBox {
                color: white;
                background: transparent;
                border: none;
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
            }
            /* Month header styling */
            QCalendarWidget QWidget#qt_calendar_calendarview {
                background: white;
                selection-background-color: #2196F3;
                selection-color: white;
            }
            /* Days of week header */
            QCalendarWidget QTableView {
                background-color: white;
                outline: 0;
            }
            QCalendarWidget QTableView::item:hover {
                background-color: #e3f2fd;
            }
            QCalendarWidget QTableView::item:selected {
                background-color: #2196F3;
                color: white;
            }
            /* Header row (days) */
            QCalendarWidget QHeaderView {
                background-color: white;
            }
            QCalendarWidget QHeaderView::section {
                color: black;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                background: white;
            }
            /* Grid */
            QCalendarWidget QTableView {
                border: none;
                gridline-color: #dcdde1;
            }
            /* Date cells */
            QCalendarWidget QTableView::item {
                padding: 10px;
                font-size: 16px;
            }
        """)
        # Set current year and month
        self.setSelectedDate(QDate.currentDate())
        # Remove week numbers
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        # Set grid visible
        self.setGridVisible(True)
        # Set the size to be larger
        self.setFixedSize(800, 600)
        # Customize the navigation bar
        self.setNavigationBarVisible(True)
        # Set first day of week to Monday
        self.setFirstDayOfWeek(Qt.DayOfWeek.Monday)

    def paintCell(self, painter, rect, date):
        painter.save()
        
        # Draw the background
        painter.fillRect(rect, QColor("white"))
        
        # Set text color based on whether it's a weekend or current month
        if date.month() != self.selectedDate().month():
            painter.setPen(QColor("#BBBBBB"))  # Gray for other month dates
        elif date.dayOfWeek() in [Qt.DayOfWeek.Saturday, Qt.DayOfWeek.Sunday]:
            painter.setPen(QColor("#FF0000"))  # Red for weekends
        else:
            painter.setPen(QColor("#000000"))  # Black for weekdays
            
        # Draw the date number
        painter.setFont(QFont("Arial", 14))  # Increased font size
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(date.day()))
        
        # Draw event indicator if there's an event on this date
        if date.toString("yyyy-MM-dd") in self.events:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#2196F3"))
            indicatorRect = QRect(
                rect.center().x() - 3,
                rect.bottom() - 8,
                6,
                6
            )
            painter.drawEllipse(indicatorRect)
        
        painter.restore()

    def minimumSizeHint(self):
        return QSize(800, 600)

    def sizeHint(self):
        return QSize(800, 600)

class EventListWidget(QWidget):
    def __init__(self, title, events, is_completed=False):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 5px;
            }
            QLabel {
                border: none;
            }
            QScrollArea {
                border: none;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Title with blue background
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: #2196F3;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
        """)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(5, 5, 5, 5)
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; padding: 5px;")
        title_layout.addWidget(title_label)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)

        # Scroll Area for Events
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent;")
        
        # Container for events
        events_widget = QWidget()
        events_layout = QVBoxLayout()
        events_layout.setSpacing(5)
        events_layout.setContentsMargins(5, 5, 5, 5)
        events_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add events
        for date, event in events.items():
            event_card = QFrame()
            event_card.setStyleSheet("""
                QFrame {
                    background: #f8f9fa;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            card_layout = QHBoxLayout()
            card_layout.setContentsMargins(5, 5, 5, 5)
            card_layout.setSpacing(5)

            # Status icon (checkmark for completed, clock for upcoming)
            status_label = QLabel("✓" if is_completed else "🕒")
            status_label.setStyleSheet(f"color: {'#27ae60' if is_completed else '#f39c12'}; font-size: 12px;")
            card_layout.addWidget(status_label)

            # Event details
            details_layout = QVBoxLayout()
            details_layout.setSpacing(2)
            
            name_label = QLabel(event["name"])
            name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            details_layout.addWidget(name_label)
            
            date_obj = QDate.fromString(date, "yyyy-MM-dd")
            date_label = QLabel(date_obj.toString("MMM d, yyyy"))
            date_label.setStyleSheet("color: #7f8c8d; font-size: 9px;")
            details_layout.addWidget(date_label)
            
            time_location = QLabel(f"{event['time']} | {event['location']}")
            time_location.setStyleSheet("color: #7f8c8d; font-size: 9px;")
            details_layout.addWidget(time_location)
            
            card_layout.addLayout(details_layout)
            event_card.setLayout(card_layout)
            events_layout.addWidget(event_card)

        events_widget.setLayout(events_layout)
        scroll.setWidget(events_widget)
        layout.addWidget(scroll)
        self.setLayout(layout)
        self.setMaximumWidth(250)  # Make the widget more compact

class EventManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.events = {
            "2024-03-01": {"name": "School Assembly", "time": "08:00", "location": "Main Hall"},
            "2024-03-10": {"name": "Parent Meeting", "time": "14:00", "location": "Conference Room"},
            "2024-03-15": {"name": "Annual Day", "time": "09:00", "location": "Auditorium"},
            "2024-03-20": {"name": "Sports Meet", "time": "10:00", "location": "Ground"},
            "2024-03-25": {"name": "Science Fair", "time": "14:00", "location": "Labs"},
            "2024-04-05": {"name": "Art Exhibition", "time": "11:00", "location": "Art Gallery"},
            "2024-04-15": {"name": "Music Concert", "time": "16:00", "location": "Auditorium"},
            "2024-04-20": {"name": "Math Olympiad", "time": "09:00", "location": "Classrooms"}
        }
        self.initUI()

    def initUI(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Department Label
        dept_label = QLabel("Departments")
        dept_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 10px 20px;
                font-size: 14px;
            }
        """)
        layout.addWidget(dept_label)

        # Tabs Layout
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(0)
        tabs_layout.setContentsMargins(20, 0, 20, 20)

        # Create tab buttons
        self.tab_buttons = []
        tabs = ["School Calendar", "Planning", "Volunteer", "Inventory", "Event Records"]  # Removed Budgets
        
        for i, tab in enumerate(tabs):
            btn = QPushButton(tab)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setMinimumWidth(100)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, index=i: self.switch_tab(index))
            
            if i == 0:
                btn.setChecked(True)
                btn.setStyleSheet("""
                    QPushButton {
                        background: #2196F3;
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        font-weight: bold;
                        text-align: center;
                        min-width: 100px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        color: #2c3e50;
                        border: none;
                        padding: 15px 30px;
                        font-weight: bold;
                        text-align: center;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        color: #2196F3;
                    }
                    QPushButton:checked {
                        background: #2196F3;
                        color: white;
                    }
                """)
            
            self.tab_buttons.append(btn)
            tabs_layout.addWidget(btn)

        layout.addLayout(tabs_layout)

        # Content Area with Stacked Widget
        self.stacked_widget = QStackedWidget()
        
        # Create all pages first
        self.calendar_page = self.create_calendar_page()
        self.planning_page = self.create_planning_page()
        self.volunteer_page = self.create_page("Volunteer")
        self.inventory_page = self.create_page("Inventory")
        self.event_records_page = self.create_page("Event Records")

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.calendar_page)
        self.stacked_widget.addWidget(self.planning_page)
        self.stacked_widget.addWidget(self.volunteer_page)
        self.stacked_widget.addWidget(self.inventory_page)
        self.stacked_widget.addWidget(self.event_records_page)

        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def switch_tab(self, index):
        # Update tab button styles
        for i, btn in enumerate(self.tab_buttons):
            if i == index:
                btn.setChecked(True)
                btn.setStyleSheet("""
                    QPushButton {
                        background: #2196F3;
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        font-weight: bold;
                        text-align: center;
                        min-width: 100px;
                    }
                """)
            else:
                btn.setChecked(False)
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        color: #2c3e50;
                        border: none;
                        padding: 15px 30px;
                        font-weight: bold;
                        text-align: center;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        color: #2196F3;
                    }
                    QPushButton:checked {
                        background: #2196F3;
                        color: white;
                    }
                """)
        
        # Switch to the selected page
        self.stacked_widget.setCurrentIndex(index)

    def create_calendar_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 20)
        layout.setSpacing(20)

        # Title and Description
        title = QLabel("School Calendar")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)

        description = QLabel("Manage school events and schedules")
        description.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        layout.addWidget(description)

        # Action Buttons in the right corner
        action_buttons = QHBoxLayout()
        action_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        manage_event_btn = QPushButton("Manage Events")
        manage_event_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        manage_event_btn.clicked.connect(self.show_manage_events_dialog)
        
        delete_event_btn = QPushButton("Delete Event")
        delete_event_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        delete_event_btn.clicked.connect(self.show_delete_event_dialog)
        
        add_event_btn = QPushButton("Add Event")
        add_event_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        add_event_btn.clicked.connect(self.show_planning_form)
        
        action_buttons.addWidget(manage_event_btn)
        action_buttons.addWidget(delete_event_btn)
        action_buttons.addWidget(add_event_btn)
        layout.addLayout(action_buttons)

        # Calendar Container
        calendar_container = QWidget()
        calendar_container.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        calendar_layout = QVBoxLayout()
        self.calendar = CustomCalendarWidget(self.events)
        calendar_layout.addWidget(self.calendar)
        calendar_container.setLayout(calendar_layout)
        layout.addWidget(calendar_container)

        page.setLayout(layout)
        return page

    def show_manage_events_dialog(self):
        dialog = ManageEventsDialog(self.events, self)
        dialog.exec()

    def show_planning_form(self):
        dialog = PlanningFormDialog(self)
        dialog.exec()

    def show_delete_event_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete Event")
        dialog.setModal(True)
        dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #2c3e50;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                background: white;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Event selection
        event_combo = QComboBox()
        for date, event in self.events.items():
            event_combo.addItem(f"{event['name']} - {date}")
        layout.addWidget(QLabel("Select Event to Delete:"))
        layout.addWidget(event_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_event(event_combo.currentText(), dialog))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()

    def delete_event(self, event_text, dialog):
        # Extract date from the event text
        date = event_text.split(" - ")[-1]
        if date in self.events:
            del self.events[date]
            self.calendar.events = self.events
            self.calendar.updateCells()
            dialog.accept()
            # Refresh the page to update the lists
            self.stacked_widget.setCurrentWidget(self.create_calendar_page())

    def create_page(self, title):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 0, 20, 20)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)

        if title == "Planning":
            layout.addWidget(self.create_planning_page())
        elif title == "Volunteer":
            layout.addWidget(self.create_volunteer_tab())
        elif title == "Inventory":
            layout.addWidget(self.create_inventory_tab())
        elif title == "Event Records":
            layout.addWidget(self.create_event_records_tab())
        
        page.setLayout(layout)
        return page

    def create_planning_page(self):
        container = QWidget()
        layout = QVBoxLayout()

        # Search and Filter Section with buttons
        search_section = QWidget()
        search_section.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 8px;
                padding: 15px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                font-size: 12px;
                min-width: 300px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                color: white;
            }
        """)

        search_layout = QVBoxLayout()
        
        # Top row with search and buttons
        top_row = QHBoxLayout()
        
        # Search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search plans...")
        
        # Add Event button
        add_event_btn = QPushButton("Add Event")
        add_event_btn.setStyleSheet("background: #2196F3;")
        add_event_btn.setFixedWidth(100)
        add_event_btn.clicked.connect(self.show_planning_form)  # Connect to show planning form
        
        # Delete Event button
        delete_event_btn = QPushButton("Delete")
        delete_event_btn.setStyleSheet("background: #e74c3c;")
        delete_event_btn.setFixedWidth(80)
        
        top_row.addWidget(search_box)
        top_row.addWidget(add_event_btn)
        top_row.addWidget(delete_event_btn)
        
        search_layout.addLayout(top_row)
        search_section.setLayout(search_layout)
        
        layout.addWidget(search_section)
        layout.addStretch()  # Push everything to the top
        
        container.setLayout(layout)
        return container

    def create_volunteer_tab(self):
        container = QWidget()
        layout = QVBoxLayout()

        # Search and Action Buttons Section
        search_section = QHBoxLayout()
        
        # Filter combo box
        self.event_filter = QComboBox()
        self.event_filter.addItems(["All Events", "Today's Events"])
        self.event_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 150px;
                margin-right: 10px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #2196F3;
                margin-right: 8px;
            }
        """)
        self.event_filter.currentIndexChanged.connect(self.filter_events)

        search_box = QLineEdit()
        search_box.setPlaceholderText("Search volunteers...")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 400px;
            }
        """)
        search_box.textChanged.connect(self.filter_volunteers)

        # Add Volunteer button
        add_volunteer_btn = QPushButton("Add Volunteer")
        add_volunteer_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        add_volunteer_btn.clicked.connect(self.show_add_volunteer_form)

        # Generate PDF button
        generate_pdf_btn = QPushButton("Generate PDF")
        generate_pdf_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        generate_pdf_btn.clicked.connect(self.generate_pdf)

        # Delete Volunteer button
        delete_volunteer_btn = QPushButton("Delete Volunteer")
        delete_volunteer_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        delete_volunteer_btn.clicked.connect(self.delete_selected_volunteer)

        search_section.addWidget(self.event_filter)
        search_section.addWidget(search_box)
        search_section.addStretch()
        search_section.addWidget(add_volunteer_btn)
        search_section.addWidget(generate_pdf_btn)
        search_section.addWidget(delete_volunteer_btn)
        layout.addLayout(search_section)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)  # Updated columns
        self.table.setHorizontalHeaderLabels([
            "Name", "Grade", "Event", "Date", "Time", 
            "Contact", "Duty", "Actions"
        ])
        self.table.setStyleSheet("""
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
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setMinimumHeight(400)

        # Set specific column widths
        self.table.setColumnWidth(7, 100)  # Action column

        # Sample Data with today's events
        today = QDate.currentDate().toString("yyyy-MM-dd")
        volunteer_data = [
            ["Alex Wilson", "9th", "Sports Day", today, "9:00 AM - 1:00 PM", "alex@email.com", "Registration"],
            ["Emma Davis", "10th", "Science Exhibition", today, "10:00 AM - 2:00 PM", "emma@email.com", "Information Desk"],
            ["Tom Brown", "8th", "Cultural Festival", "2024-03-25", "2:00 PM - 6:00 PM", "tom@email.com", "Stage Management"],
            ["Sarah Lee", "9th", "Sports Day", "2024-03-15", "8:00 AM - 12:00 PM", "sarah@email.com", "Equipment Setup"]
        ]

        self.table.setRowCount(len(volunteer_data))
        for row, data in enumerate(volunteer_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)
            
            # Add action button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            edit_btn = QPushButton("Update")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background: #2196F3;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-weight: bold;
                    min-width: 60px;
                    max-width: 60px;
                    font-size: 11px;
                    height: 32px;
                }
                QPushButton:hover {
                    background: #1976D2;
                }
                QPushButton:pressed {
                    background: #1565C0;
                }
            """)
            
            # Store the row number in the button's property
            edit_btn.setProperty("row", row)
            edit_btn.clicked.connect(self.handle_update_click)
            
            actions_layout.addWidget(edit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(row, 7, actions_widget)

        layout.addWidget(self.table)
        container.setLayout(layout)
        return container

    def filter_events(self, index):
        try:
            if index == 0:  # All Events
                # Show all rows
                for row in range(self.table.rowCount()):
                    self.table.setRowHidden(row, False)
            else:  # Today's Events
                today = QDate.currentDate().toString("yyyy-MM-dd")
                for row in range(self.table.rowCount()):
                    date_item = self.table.item(row, 3)  # Date column
                    if date_item and date_item.text() == today:
                        self.table.setRowHidden(row, False)
                    else:
                        self.table.setRowHidden(row, True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to filter events: {str(e)}")

    def filter_volunteers(self, text):
        try:
            for row in range(self.table.rowCount()):
                match = False
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item and text.lower() in item.text().lower():
                        match = True
                        break
                self.table.setRowHidden(row, not match)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def generate_pdf(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
            if file_path:
                from reportlab.lib.pagesizes import letter, landscape
                from reportlab.lib import colors
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch

                # Create the PDF document
                doc = SimpleDocTemplate(
                    file_path,
                    pagesize=landscape(letter),
                    rightMargin=30,
                    leftMargin=30,
                    topMargin=30,
                    bottomMargin=30
                )
                
                elements = []
                styles = getSampleStyleSheet()
                
                # Add title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30,
                    alignment=1  # Center alignment
                )
                title = Paragraph("Volunteer List", title_style)
                elements.append(title)
                elements.append(Spacer(1, 20))

                # Collect visible data from table
                headers = ["Name", "Grade", "Event", "Date", "Time", "Contact", "Duty"]
                data = [headers]
                
                for row in range(self.table.rowCount()):
                    if not self.table.isRowHidden(row):
                        row_data = []
                        for col in range(7):  # Exclude Actions column
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else "")
                        data.append(row_data)

                # Create table with specific column widths
                col_widths = [2*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch]
                table = Table(data, colWidths=col_widths)
                
                # Add table style
                table.setStyle(TableStyle([
                    # Header style
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    
                    # Cell style
                    ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -2), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('PADDING', (0, 0), (-1, -1), 8),
                    
                    # Total row style
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f5f5f5')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ]))

                elements.append(table)
                doc.build(elements)
                QMessageBox.information(self, "Success", f"PDF saved at: {file_path}")
            else:
                QMessageBox.warning(self, "PDF Generation", "No file path selected.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF: {str(e)}")

    def show_add_volunteer_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Volunteer")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 200px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Form fields
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Name
        name_input = QLineEdit()
        form_layout.addRow("Name:", name_input)
        
        # Grade (only 8th, 9th, 10th)
        grade_input = QComboBox()
        grade_input.addItems(["8th", "9th", "10th"])
        form_layout.addRow("Grade:", grade_input)
        
        # Event (user-defined)
        event_input = QLineEdit()
        event_input.setPlaceholderText("Enter event name")
        form_layout.addRow("Event:", event_input)
        
        # Date
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        form_layout.addRow("Date:", date_input)
        
        # Time (user-defined)
        time_input = QLineEdit()
        time_input.setPlaceholderText("e.g., 9:00 AM - 1:00 PM")
        form_layout.addRow("Time:", time_input)
        
        # Contact
        contact_input = QLineEdit()
        contact_input.setPlaceholderText("Email or Phone")
        form_layout.addRow("Contact:", contact_input)
        
        # Duty
        duty_input = QComboBox()
        duty_input.addItems([
            "Registration",
            "Information Desk",
            "Stage Management",
            "Equipment Setup",
            "Crowd Control",
            "Refreshments"
        ])
        form_layout.addRow("Duty:", duty_input)
        
        layout.addLayout(form_layout)
        
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
                min-width: 100px;
            }
        """)
        save_btn.clicked.connect(lambda: self.save_volunteer(
            name_input.text(),
            grade_input.currentText(),
            event_input.text(),
            date_input.date().toString("yyyy-MM-dd"),
            time_input.text(),
            contact_input.text(),
            duty_input.currentText(),
            dialog
        ))
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec()

    def save_volunteer(self, name, grade, event, date, time, contact, duty, dialog):
        if not all([name, grade, event, date, time, contact, duty]):
            QMessageBox.warning(dialog, "Error", "Please fill in all fields")
            return
        
        # Here you would typically save to database
        # For now, we'll just close the dialog
        dialog.accept()
        QMessageBox.information(self, "Success", "Volunteer added successfully")

    def delete_selected_volunteer(self):
        reply = QMessageBox.question(
            self,
            "Delete Volunteer",
            "Are you sure you want to delete the selected volunteer?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Here you would typically delete from database
            QMessageBox.information(self, "Success", "Volunteer deleted successfully")

    def create_inventory_tab(self):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Search and Action Buttons Section
        search_section = QHBoxLayout()
        
        # Search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search inventory...")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 250px;
            }
        """)

        # Action buttons container
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(15)  # Increased spacing between buttons
        buttons_layout.setContentsMargins(10, 0, 10, 0)

        # Add Inventory button
        add_inventory_btn = QPushButton("Add Inventory")
        add_inventory_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 130px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        add_inventory_btn.clicked.connect(self.show_add_inventory_form)

        # Delete Inventory button
        delete_inventory_btn = QPushButton("Delete Inventory")
        delete_inventory_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 130px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        delete_inventory_btn.clicked.connect(self.delete_inventory)

        # Order Supply button
        order_supply_btn = QPushButton("Order Supply")
        order_supply_btn.setStyleSheet("""
            QPushButton {
                background: #FF9800;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 130px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #F57C00;
            }
        """)
        order_supply_btn.clicked.connect(self.show_order_supply)

        buttons_layout.addWidget(add_inventory_btn)
        buttons_layout.addWidget(delete_inventory_btn)
        buttons_layout.addWidget(order_supply_btn)

        search_section.addWidget(search_box)
        search_section.addStretch()
        search_section.addWidget(buttons_widget)
        layout.addLayout(search_section)

        # Table setup with smaller update button
        table_container = QWidget()
        table_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 20, 0, 0)

        # Table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels([
            "Item Name", "Category", "Quantity", "Available", "Condition", "Actions"
        ])
        self.inventory_table.setStyleSheet("""
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
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.inventory_table.setMinimumHeight(500)

        # Set a fixed width for the Actions column
        self.inventory_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.inventory_table.setColumnWidth(5, 80)  # Set Actions column width to 80px

        # Sample Data
        inventory_data = [
            ["Microphones", "Audio/Visual", "10", "8", "Good"],
            ["Chairs", "Furniture", "200", "180", "Need Supply"],
            ["Sports Balls", "Sports Equipment", "50", "45", "Good"],
            ["Banners", "Decorations", "20", "15", "Need Supply"]
        ]

        self.inventory_table.setRowCount(len(inventory_data))
        for row, data in enumerate(inventory_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.inventory_table.setItem(row, col, item)
            
            # Add update button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(0)
            
            edit_btn = QPushButton("Update")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background: #2196F3;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-weight: bold;
                    min-width: 60px;
                    max-width: 60px;
                    font-size: 11px;
                    height: 32px;
                }
                QPushButton:hover {
                    background: #1976D2;
                }
                QPushButton:pressed {
                    background: #1565C0;
                }
            """)
            
            # Store the row number in the button's property
            edit_btn.setProperty("row", row)
            edit_btn.clicked.connect(self.handle_update_click)
            
            actions_layout.addWidget(edit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
            self.inventory_table.setCellWidget(row, 5, actions_widget)

        table_layout.addWidget(self.inventory_table)
        table_container.setLayout(table_layout)
        layout.addWidget(table_container)
        
        container.setLayout(layout)
        return container

    def handle_update_click(self):
        # Get the row number from the button's property
        button = self.sender()
        if button:
            row = button.property("row")
            self.update_inventory_item(row)

    def update_inventory_item(self, row):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Update Inventory Item")
            dialog.setModal(True)
            dialog.setMinimumWidth(400)
            dialog.setStyleSheet("""
                QDialog {
                    background: white;
                }
                QLabel {
                    color: #2c3e50;
                    font-size: 12px;
                }
                QLineEdit, QComboBox {
                    padding: 8px;
                    border: 1px solid #dcdde1;
                    border-radius: 4px;
                    background: white;
                    min-width: 200px;
                }
            """)
            
            layout = QVBoxLayout()
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)
            
            form_layout = QFormLayout()
            form_layout.setSpacing(10)
            
            # Get current values
            name = self.inventory_table.item(row, 0).text()
            category = self.inventory_table.item(row, 1).text()
            quantity = self.inventory_table.item(row, 2).text()
            available = self.inventory_table.item(row, 3).text()
            condition = self.inventory_table.item(row, 4).text()
            
            # Create input fields with current values
            name_input = QLineEdit(name)
            category_input = QLineEdit(category)
            quantity_input = QLineEdit(quantity)
            available_input = QLineEdit(available)
            condition_input = QComboBox()
            condition_input.addItems(["Good", "Fair", "Poor", "Need Supply"])
            condition_input.setCurrentText(condition)
            
            form_layout.addRow("Item Name:", name_input)
            form_layout.addRow("Category:", category_input)
            form_layout.addRow("Quantity:", quantity_input)
            form_layout.addRow("Available:", available_input)
            form_layout.addRow("Condition:", condition_input)
            
            layout.addLayout(form_layout)
            
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
            
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background: #95a5a6;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background: #7f8c8d;
                }
            """)
            
            button_layout.addStretch()
            button_layout.addWidget(save_btn)
            button_layout.addWidget(cancel_btn)
            layout.addLayout(button_layout)
            
            dialog.setLayout(layout)
            
            # Connect buttons
            save_btn.clicked.connect(lambda: self.save_updated_inventory(
                row,
                name_input.text(),
                category_input.text(),
                quantity_input.text(),
                available_input.text(),
                condition_input.currentText(),
                dialog
            ))
            cancel_btn.clicked.connect(dialog.reject)
            
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def save_updated_inventory(self, row, name, category, quantity, available, condition, dialog):
        try:
            if not all([name, category, quantity, available]):
                QMessageBox.warning(dialog, "Error", "Please fill in all fields")
                return
            
            # Update the table
            self.inventory_table.item(row, 0).setText(name)
            self.inventory_table.item(row, 1).setText(category)
            self.inventory_table.item(row, 2).setText(quantity)
            self.inventory_table.item(row, 3).setText(available)
            self.inventory_table.item(row, 4).setText(condition)
            
            dialog.accept()
            QMessageBox.information(self, "Success", "Inventory item updated successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update inventory: {str(e)}")

    def show_add_inventory_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Inventory Item")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
                min-width: 200px;
            }
        """)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Item Name
        name_input = QLineEdit()
        form_layout.addRow("Item Name:", name_input)
        
        # Category (user input)
        category_input = QLineEdit()
        category_input.setPlaceholderText("Enter category")
        form_layout.addRow("Category:", category_input)
        
        # Quantity (user input)
        quantity_input = QLineEdit()
        quantity_input.setPlaceholderText("Enter quantity")
        form_layout.addRow("Quantity:", quantity_input)
        
        # Condition
        condition_input = QComboBox()
        condition_input.addItems(["Good", "Fair", "Poor", "Need Supply"])
        form_layout.addRow("Condition:", condition_input)
        
        # Cost in INR
        cost_input = QLineEdit()
        cost_input.setPlaceholderText("Enter cost in ₹")
        form_layout.addRow("Cost (₹):", cost_input)
        
        layout.addLayout(form_layout)
        
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
        """)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # Connect buttons
        save_btn.clicked.connect(lambda: self.save_inventory(
            name_input.text(),
            category_input.text(),
            quantity_input.text(),
            condition_input.currentText(),
            cost_input.text(),
            dialog
        ))
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()

    def save_inventory(self, name, category, quantity, condition, cost, dialog):
        if not name:
            QMessageBox.warning(dialog, "Error", "Please enter item name")
            return
            
        row = self.inventory_table.rowCount()
        self.inventory_table.insertRow(row)
        
        today = QDate.currentDate().toString("yyyy-MM-dd")
        
        items = [
            name,
            category,
            quantity,
            quantity,  # Available same as quantity for new items
            condition,
            today,
            "Available"
        ]
        
        for col, value in enumerate(items):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.inventory_table.setItem(row, col, item)
            
        # Add action button
        actions_widget = QWidget()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(4, 4, 4, 4)
        
        edit_btn = QPushButton("Update")
        edit_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 60px;
                font-size: 11px;
                height: 32px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        
        actions_layout.addWidget(edit_btn)
        actions_widget.setLayout(actions_layout)
        self.inventory_table.setCellWidget(row, 5, actions_widget)
        
        dialog.accept()
        QMessageBox.information(self, "Success", "Inventory item added successfully")

    def delete_inventory(self):
        selected_rows = set(item.row() for item in self.inventory_table.selectedItems())
        if not selected_rows:
            QMessageBox.warning(self, "Error", "Please select items to delete")
            return
            
        reply = QMessageBox.question(
            self,
            "Delete Inventory",
            f"Are you sure you want to delete {len(selected_rows)} selected items?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            for row in sorted(selected_rows, reverse=True):
                self.inventory_table.removeRow(row)
            QMessageBox.information(self, "Success", "Selected items deleted successfully")

    def show_order_supply(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Order Supply List")
        dialog.setModal(True)
        dialog.setMinimumWidth(800)
        dialog.setMinimumHeight(600)
        dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Create table for needed supplies
        supply_table = QTableWidget()
        supply_table.setColumnCount(6)
        supply_table.setHorizontalHeaderLabels([
            "Item Name", "Category", "Current Stock", "Required", "Unit Cost (₹)", "Total Cost (₹)"
        ])
        
        # Get items that need supply
        needed_items = []
        total_cost = 0
        for row in range(self.inventory_table.rowCount()):
            condition = self.inventory_table.item(row, 4)  # Condition column
            if condition and condition.text() == "Need Supply":
                item_data = []
                # Get basic info
                for col in [0, 1, 3]:  # Name, Category, Available
                    cell = self.inventory_table.item(row, col)
                    item_data.append(cell.text() if cell else "")
                
                # Calculate required quantity (20% more than current)
                current_stock = int(self.inventory_table.item(row, 3).text())
                required = int(current_stock * 1.2) - current_stock
                item_data.append(str(required))
                
                # Add costs (sample costs - in real app, would come from database)
                unit_cost = 1000  # Sample cost in INR
                total_item_cost = unit_cost * required
                total_cost += total_item_cost
                
                item_data.append(f"₹{unit_cost:,}")
                item_data.append(f"₹{total_item_cost:,}")
                needed_items.append(item_data)
        
        supply_table.setRowCount(len(needed_items))
        for row, data in enumerate(needed_items):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                supply_table.setItem(row, col, item)
        
        # Add total cost label
        total_cost_label = QLabel(f"Total Order Cost: ₹{total_cost:,}")
        total_cost_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
        """)
        
        layout.addWidget(supply_table)
        layout.addWidget(total_cost_label)
        
        # Add buttons
        button_layout = QHBoxLayout()
        generate_pdf_btn = QPushButton("Generate PDF")
        generate_pdf_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
        """)
        
        button_layout.addWidget(generate_pdf_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # Connect buttons
        generate_pdf_btn.clicked.connect(lambda: self.generate_order_pdf(needed_items, total_cost, dialog))
        close_btn.clicked.connect(dialog.reject)
        
        dialog.exec()

    def generate_order_pdf(self, items, total_cost, dialog):
        try:
            file_path, _ = QFileDialog.getSaveFileName(dialog, "Save PDF", "", "PDF Files (*.pdf)")
            if file_path:
                from reportlab.lib.pagesizes import letter, landscape
                from reportlab.lib import colors
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch

                # Create the PDF document
                doc = SimpleDocTemplate(
                    file_path,
                    pagesize=landscape(letter),
                    rightMargin=30,
                    leftMargin=30,
                    topMargin=30,
                    bottomMargin=30
                )
                
                elements = []
                styles = getSampleStyleSheet()
                
                # Add title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30,
                    alignment=1  # Center alignment
                )
                title = Paragraph("Supply Order List", title_style)
                elements.append(title)
                elements.append(Spacer(1, 20))

                # Create table
                headers = ["Item Name", "Category", "Current Stock", "Required", "Unit Cost (₹)", "Total Cost (₹)"]
                data = [headers] + [[str(item) for item in row] for row in items]
                
                # Add total row
                data.append(["Total", "", "", "", "", f"₹{total_cost:,}"])

                # Create table with specific column widths
                col_widths = [2*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch]
                table = Table(data, colWidths=col_widths)
                
                # Add table style
                table.setStyle(TableStyle([
                    # Header style
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    
                    # Cell style
                    ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -2), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('PADDING', (0, 0), (-1, -1), 8),
                    
                    # Total row style
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f5f5f5')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ]))

                elements.append(table)
                doc.build(elements)
                QMessageBox.information(dialog, "Success", f"PDF saved at: {file_path}")
                dialog.accept()
            else:
                QMessageBox.warning(dialog, "PDF Generation", "No file path selected.")
        except Exception as e:
            QMessageBox.critical(dialog, "Error", f"Failed to generate PDF: {str(e)}")

    def create_event_records_tab(self):
        container = QWidget()
        layout = QVBoxLayout()

        # Search and Filter Section
        search_section = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Search records...")
        search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
            }
        """)
        year_filter = QComboBox()
        year_filter.addItems(["All Years", "2024", "2023", "2022"])
        year_filter.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background: white;
            }
        """)
        search_section.addWidget(search_box)
        search_section.addWidget(year_filter)
        layout.addLayout(search_section)

        # Table
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["Event Name", "Date", "Attendance", "Budget Used", "Rating", "Status", "Actions"])
        table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #dcdde1;
                border-radius: 4px;
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

        # Sample Data
        records_data = [
            ["Winter Concert", "2023-12-15", "500", "$5000", "4.5/5", "Completed"],
            ["Science Fair", "2024-01-20", "300", "$3000", "4.8/5", "Completed"],
            ["Sports Day", "2024-02-10", "800", "$8000", "4.7/5", "Completed"],
            ["Art Exhibition", "2024-03-05", "250", "$2500", "4.6/5", "Completed"]
        ]

        table.setRowCount(len(records_data))
        for row, data in enumerate(records_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, item)
            
            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background: #2196F3;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
            """)
            
            report_btn = QPushButton("Report")
            report_btn.setStyleSheet("""
                QPushButton {
                    background: #27ae60;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
            """)
            
            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(report_btn)
            actions_widget.setLayout(actions_layout)
            table.setCellWidget(row, 6, actions_widget)

        table.resizeColumnsToContents()
        layout.addWidget(table)
        container.setLayout(layout)
        return container

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EventManagementPage()
    window.show()
    sys.exit(app.exec())
