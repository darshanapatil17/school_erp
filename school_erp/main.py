"""
School ERP System - Main Entry Point
This is the main entry point for the School ERP system.
"""

import sys
from PyQt6.QtWidgets import QApplication
from screens.login_screen import LoginScreen

def main():
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
