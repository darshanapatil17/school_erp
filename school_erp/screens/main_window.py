import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from .SalarySlip import SalarySlip
from .ExamDepartment import ExamDepartment

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School ERP System")
        self.setFixedSize(1200, 800)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Add tabs
        self.salary_slip_tab = SalarySlip()
        self.exam_department_tab = ExamDepartment()

        self.tab_widget.addTab(self.salary_slip_tab, "Salary Slip")
        self.tab_widget.addTab(self.exam_department_tab, "Exam Department")

        # Set tab styles
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #cccccc;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #2980B9;
                color: white;
            }
        """) 