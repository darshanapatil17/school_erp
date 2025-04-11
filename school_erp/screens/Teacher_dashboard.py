from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QTextEdit
from PyQt6.QtGui import QFont

class TeacherDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard - School ERP")
        self.setGeometry(100, 100, 1200, 750)
        
        self.initUI()
    
    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left Section - Sidebar
        sidebar = QListWidget()
        modules = [
            "Dashboard",
            "Class Management",
            "Department Details",
            "Library Access",
            "Computer Lab Schedule",
            "Attendance Management",
            "Class Schedule & Timetable",
            "Student Progress Reports",
            "Assignments & Homework",
            "Exam & Result Management",
            "Notice Board & Communication",
            "Document Management",
            "Student Awards & Achievements",
            "Lesson Plans & Curriculum",
            "School Events & Activities",
            "Exit"
        ]
        
        for module in modules:
            sidebar.addItem(module)
        
        sidebar.setFixedWidth(350)  # Increased width for better readability
        sidebar.setFont(QFont("Arial", 16))
        sidebar.setStyleSheet("background-color: #2C3E50; color: white; padding: 15px; border-radius: 10px;")
        
        # Right Section - Content Area
        content_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Teacher Dashboard - School ERP", self)
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #333; margin-bottom: 20px;")
        content_layout.addWidget(title)
        
        # Buttons for different features
        features = [
            ("Class Management", "#3498DB"),
            ("Department Details", "#E74C3C"),
            ("Library Access", "#F39C12"),
            ("Computer Lab Schedule", "#9B59B6"),
            ("Attendance Management", "#1ABC9C"),
            ("Class Schedule & Timetable", "#D35400"),
            ("Student Progress Reports", "#27AE60"),
            ("Assignments & Homework", "#2980B9"),
            ("Exam & Result Management", "#C0392B"),
            ("Notice Board & Communication", "#8E44AD"),
            ("Document Management", "#16A085"),
            ("Student Awards & Achievements", "#F1C40F"),
            ("Lesson Plans & Curriculum", "#2ECC71"),
            ("School Events & Activities", "#E67E22")
        ]
        
        feature_section = QHBoxLayout()
        column1 = QVBoxLayout()
        column2 = QVBoxLayout()
        
        for index, (text, color) in enumerate(features):
            btn = QPushButton(text, self)
            btn.setFont(QFont("Arial", 18, QFont.Weight.Bold))  # Increased font size for better visibility
            btn.setStyleSheet(f"""
                padding: 15px;
                margin: 10px;
                background-color: {color};
                color: white;
                border-radius: 10px;
                text-align: center;
            """)
            btn.setFixedHeight(70)  # Increased height for better text fit
            btn.setFixedWidth(400)  # Increased width for better text fit
            
            if index % 2 == 0:
                column1.addWidget(btn)
            else:
                column2.addWidget(btn)
        
        feature_section.addLayout(column1)
        feature_section.addLayout(column2)
        content_layout.addLayout(feature_section)
        
        # AI Chatbot Section
        chatbot_section = QVBoxLayout()
        
        chatbot_label = QLabel("AI Chatbot", self)
        chatbot_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        chatbot_label.setStyleSheet("color: #333; margin-top: 20px;")
        chatbot_section.addWidget(chatbot_label)
        
        chatbot_box = QTextEdit(self)
        chatbot_box.setPlaceholderText("Ask me anything...")
        chatbot_box.setFixedHeight(170)
        chatbot_box.setStyleSheet("background-color: #ECF0F1; padding: 18px; border-radius: 10px; font-size: 18px;")
        chatbot_section.addWidget(chatbot_box)
        
        content_layout.addLayout(chatbot_section)
        
        # Combine Sidebar and Content Layouts
        main_layout.addWidget(sidebar)
        main_layout.addLayout(content_layout)
        
        # Central Widget Setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = TeacherDashboard()
    window.show()
    app.exec()



