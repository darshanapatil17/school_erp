import sys
import os
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .main_window import MainWindow

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("School ERP - Admin & Teacher Login")
        self.setFixedSize(750, 500)

        self.main_layout = QHBoxLayout()

        # Create Login Frames (Admin & Teacher) with Borders
        self.admin_frame = self.create_login_frame("Admin Login")
        self.teacher_frame = self.create_login_frame("Teacher Login")

        # Add Frames to Layout
        self.main_layout.addWidget(self.admin_frame)
        self.main_layout.addWidget(self.teacher_frame)

        self.setLayout(self.main_layout)

        # Apply Light Mode Styling
        self.dark_mode = False
        self.light_mode_styles()

        # Dark Mode Toggle Button
        self.toggle_button = QPushButton("🌙 Dark Mode", self)
        self.toggle_button.setGeometry(600, 20, 130, 40)
        self.toggle_button.setStyleSheet("background-color: #2980B9; color: white; font-size: 14px; border-radius: 8px;")
        self.toggle_button.clicked.connect(self.toggle_dark_mode)

    def create_login_frame(self, title):
        """Creates the login UI sections with borders"""
        frame = QFrame()
        frame.setFixedSize(340, 400)
        frame.setStyleSheet("""
            QFrame {
                border: 2px solid #3498DB;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        label = QLabel(title)
        label.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        username_input = QLineEdit()
        username_input.setPlaceholderText("Enter Username")
        username_input.setFixedHeight(45)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Enter Password")
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setFixedHeight(45)

        show_password = QCheckBox("Show Password")
        show_password.setFont(QFont("Poppins", 12))
        show_password.clicked.connect(lambda: self.toggle_password(password_input, show_password))

        options_layout = QHBoxLayout()
        remember_me = QCheckBox("Remember Me")
        remember_me.setFont(QFont("Poppins", 12))
        forgot_password = QPushButton("Forgot Password?")
        forgot_password.setFont(QFont("Poppins", 12))
        forgot_password.setStyleSheet("border: none; color: #3498DB;")
        forgot_password.clicked.connect(lambda: self.forgot_password_message(title))

        options_layout.addWidget(remember_me)
        options_layout.addWidget(forgot_password)

        login_button = QPushButton("Login")
        login_button.setFixedHeight(50)
        login_button.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        login_button.clicked.connect(lambda: self.verify_login(username_input.text(), password_input.text(), title))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(20)
        layout.addWidget(username_input)
        layout.addWidget(password_input)
        layout.addWidget(show_password)
        layout.addLayout(options_layout)
        layout.addSpacing(15)
        layout.addWidget(login_button)

        frame.setLayout(layout)
        return frame

    def forgot_password_message(self, user_type):
        """Show forgot password message"""
        QMessageBox.information(self, "Forgot Password", f"Reset password link sent to {user_type.lower()} email.")

    def verify_login(self, username, password, role):
        """Verify login credentials from SQLite database"""
        # Get the absolute path to the database
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screens", "users.db")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ? AND role = ?", 
                         (username, password, role.lower().replace(' login', '')))
            user = cursor.fetchone()

            conn.close()

            if user:
                QMessageBox.information(self, "Login Successful", f"Welcome {role.replace(' Login', '')}!")
                self.open_main_application(role)
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error accessing database: {str(e)}")

    def open_main_application(self, role):
        """Open the main application based on user role"""
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def toggle_password(self, password_field, checkbox):
        """Toggle password visibility"""
        if checkbox.isChecked():
            password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            password_field.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        if self.dark_mode:
            self.light_mode_styles()
            self.toggle_button.setText("🌙 Dark Mode")
            self.dark_mode = False
        else:
            self.dark_mode_styles()
            self.toggle_button.setText("☀ Light Mode")
            self.dark_mode = True

    def light_mode_styles(self):
        """Apply light mode styles"""
        self.setStyleSheet("""
            background-color: white;
            color: black;
        """)

    def dark_mode_styles(self):
        """Apply dark mode styles and change border color"""
        self.setStyleSheet("""
            background-color: #2C3E50;
            color: white;
        """)
        self.admin_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #E74C3C; /* Red border for dark mode */
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.teacher_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #F39C12; /* Orange border for dark mode */
                border-radius: 10px;
                padding: 15px;
            }
        """)

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec())