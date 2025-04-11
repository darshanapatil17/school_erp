"""
School ERP System - Screens Package
This package contains all the screen modules for the School ERP system.
"""

from .database import Database, DatabaseHandler
from .SalarySlip import SalarySlip
from .login_screen import LoginScreen
from .ExamDepartment import ExamDepartment
from .main_window import MainWindow

__all__ = [
    'Database',
    'DatabaseHandler',
    'SalarySlip',
    'LoginScreen',
    'ExamDepartment',
    'MainWindow'
] 