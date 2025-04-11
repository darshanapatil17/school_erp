import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGridLayout, QPushButton, QTextEdit, QFrame, QScrollArea
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class AdminDashboard(QMainWindow):
    def __init__(self):  # ✅ Fixed `__init__` method
        super().__init__()  # ✅ Fixed `super().__init__()`
        self.setWindowTitle("School ERP - Admin Dashboard")
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("background-color: #f8f9fa;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setStyleSheet("""
            background-color: #2C3E50; 
            color: white; 
            font-size: 16px; 
            border-radius: 10px;
            padding: 15px;
        """)
        self.sidebar.setFixedWidth(250)

        self.sidebar_container = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_container)
        self.sidebar_layout.addWidget(self.sidebar, stretch=1)

        # Sidebar Footer
        self.sidebar_footer = QLabel("📚 Empowering Education!")
        self.sidebar_footer.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.sidebar_footer.setStyleSheet("color: #ECF0F1; padding: 5px;")
        self.sidebar_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addWidget(self.sidebar_footer)

        self.sidebar_container.setLayout(self.sidebar_layout)

        self.main_modules = [
            "🏠 Dashboard", "📅 Manage Session", "📂 Account", "👨🏫 Teachers",
            "🏢 Admin Office", "👥 Staff Management", "📅 Attendance", "📚 Exams",
            "💰 Fees", "📖 Library", "🚌 Transport", "🆕 Admissions", "📊 Reports",
            "🎉 Events", "⚙ Settings", "🤖 AI Chatbot", "🚪 Exit"
        ]
        self.load_main_modules()

        # Right Section (Main Content)
        self.right_section = QWidget()
        self.right_layout = QVBoxLayout(self.right_section)

        # Header
        self.header_label = QLabel("Admin Dashboard - School ERP")
        self.header_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.header_label.setStyleSheet("background-color: #34495E; color: white; padding: 15px; border-radius: 8px;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(self.header_label)

        # Scroll Area for Content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # ✅ Kept All Features Intact (Just Fixed Errors)
        self.features_section = QWidget()
        self.features_layout = QGridLayout(self.features_section)
        self.features_layout.setSpacing(6)

        features = [
            ("📅 Smart Auto-Generated Timetable", "#9B59B6"),
            ("📧 Auto-Reply Email Assistant", "#3498DB"),
            ("📢 Digital Notice Board", "#E74C3C"),
            ("💰 Fee Payment Tracker", "#F39C12"),
            ("🎒 Lost & Found Portal", "#16A085"),
            ("📅 Automated Staff Leave Management", "#D35400"),
            ("📊 Auto-Generated Staff Work Reports", "#8E44AD"),
            ("📄 AI-Based Letter & Notice Generator", "#2980B9"),
            ("💰 One-Click Salary Slip & Payroll Generator", "#27AE60"),
            ("🎓 Instant Student Record Finder", "#1ABC9C"),
            ("📅 Staff Leave & Attendance Tracker", "#C0392B"),
            ("🏅 Auto-Generated Certificates", "#8E44AD"),
            ("📢 AI-Based Complaint & Issue Tracker", "#2C3E50"),
            ("💳 Automated Fee & Fine Collection", "#E67E22"),
            ("📅 Staff Meeting Scheduler", "#3498DB"),
            ("📊 Fee Report", "#D35400"),
            ("📑 Exam Results Manager", "#C0392B"),
            ("🎯 Goal & Achievement Tracker", "#F39C12")
        ]

        for i, (feature, color) in enumerate(features):
            feature_box = QFrame()
            feature_box.setStyleSheet(f"background-color: {color}; padding: 6px; border-radius: 6px;")
            feature_box_layout = QVBoxLayout(feature_box)
            feature_label = QLabel(feature)
            feature_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            feature_label.setStyleSheet("color: white;")
            feature_box_layout.addWidget(feature_label)
            self.features_layout.addWidget(feature_box, i // 4, i % 4)

        self.scroll_layout.addWidget(self.features_section)

        # Graph/Chart Placeholder
        self.graph_card = QFrame()
        self.graph_card.setStyleSheet("background-color: #34495E; padding: 10px; border-radius: 6px;")
        self.graph_layout = QVBoxLayout(self.graph_card)
        self.graph_label = QLabel("📊 Student Performance Analytics (Placeholder)")
        self.graph_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.graph_label.setStyleSheet("color: white;")
        self.graph_layout.addWidget(self.graph_label)
        self.scroll_layout.addWidget(self.graph_card)

        # AI Assistant Section
        self.ai_assistant_card = QFrame()
        self.ai_assistant_card.setStyleSheet("background-color: #2C3E50; padding: 6px; border-radius: 6px;")
        self.ai_assistant_layout = QVBoxLayout(self.ai_assistant_card)

        self.ai_label = QLabel("🤖 AI Assistant")
        self.ai_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.ai_label.setStyleSheet("color: white;")
        self.ai_assistant_layout.addWidget(self.ai_label)

        self.faq_ai_panel = QTextEdit()
        self.faq_ai_panel.setPlaceholderText("Ask AI about school policies, fees, or schedules...")
        self.faq_ai_panel.setStyleSheet("background-color: white; padding: 6px; border-radius: 5px; height: 50px;")
        self.ai_assistant_layout.addWidget(self.faq_ai_panel)

        self.scroll_layout.addWidget(self.ai_assistant_card)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.right_layout.addWidget(self.scroll_area)
        self.right_section.setLayout(self.right_layout)
        self.layout.addWidget(self.sidebar_container)
        self.layout.addWidget(self.right_section, 1)

    def load_main_modules(self):
        self.sidebar.clear()
        for module in self.main_modules:
            self.sidebar.addItem(module)

if __name__ == "__main__":  # ✅ Fixed `if __name__ == "__main__":`
    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.showMaximized()
    sys.exit(app.exec())



