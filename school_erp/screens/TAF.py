import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGroupBox, QTableWidget, QComboBox, QPushButton,
    QTableWidgetItem, QFileDialog, QTextEdit, QDateEdit, QTimeEdit, QStackedWidget
)
from PyQt6.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class TeacherAdmissionForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Admission Form")
        self.setGeometry(100, 100, 900, 700)
        self.stacked_widget = QStackedWidget()
        self.pages = []

        self.pages.append(self.create_documents_page())
        self.pages.append(self.create_interview_demo_page())

        for page in self.pages:
            self.stacked_widget.addWidget(page)

        self.current_page = 0
        self.stacked_widget.setCurrentIndex(self.current_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def create_documents_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        docs_group = QGroupBox("Upload Required Documents")
        docs_layout = QVBoxLayout()
        self.upload_buttons = {}
        self.uploaded_files = {}
        self.uploaded_file_labels = {}
        doc_labels = ["Resume", "Aadhaar Card", "PAN Card", "Educational Certificates"]

        for label in doc_labels:
            hbox = QHBoxLayout()
            doc_label = QLabel(label + ": ")
            uploaded_file_label = QLabel("No file uploaded")
            upload_button = QPushButton("Upload")
            upload_button.clicked.connect(lambda _, l=label: self.upload_file(l))
            hbox.addWidget(doc_label)
            hbox.addWidget(upload_button)
            hbox.addWidget(uploaded_file_label)
            docs_layout.addLayout(hbox)
            self.upload_buttons[label] = upload_button
            self.uploaded_file_labels[label] = uploaded_file_label

        docs_group.setLayout(docs_layout)
        layout.addWidget(docs_group)
        self.add_navigation_buttons(layout, back_page=True, next_page=True)
        page.setLayout(layout)
        return page

    def create_interview_demo_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        interview_group = QGroupBox("Interview Details")
        interview_layout = QFormLayout()
        self.interview_date = QDateEdit()
        self.interview_time = QTimeEdit()
        self.panel_members = QTextEdit()
        self.panel_members.setFixedHeight(30)  # Decreased size

        interview_layout.addRow("Interview Date:", self.interview_date)
        interview_layout.addRow("Interview Time:", self.interview_time)
        interview_layout.addRow("Panel Members:", self.panel_members)
        interview_group.setLayout(interview_layout)
        layout.addWidget(interview_group)

        self.add_navigation_buttons(layout, back_page=True, submit=True)
        page.setLayout(layout)
        return page

    def add_navigation_buttons(self, layout, back_page=False, next_page=False, submit=False):
        button_layout = QHBoxLayout()
        if back_page:
            back_button = QPushButton("Back")
            back_button.clicked.connect(self.go_back)
            button_layout.addWidget(back_button)
        if next_page:
            next_button = QPushButton("Next")
            next_button.clicked.connect(self.go_next)
            button_layout.addWidget(next_button)
        if submit:
            submit_button = QPushButton("Submit")
            submit_button.clicked.connect(self.submit_form)
            button_layout.addWidget(submit_button)
        layout.addLayout(button_layout)

    def go_back(self):
        self.current_page -= 1
        self.stacked_widget.setCurrentIndex(self.current_page)

    def go_next(self):
        self.current_page += 1
        self.stacked_widget.setCurrentIndex(self.current_page)

    def submit_form(self):
        pdf_path = QFileDialog.getSaveFileName(self, "Save PDF", "Teacher_Admission_Form.pdf", "PDF Files (*.pdf)")[0]
        if not pdf_path:
            return
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(200, 800, "Teacher Admission Form")
        c.setFont("Helvetica", 10)
        c.drawString(50, 770, "Interview Details:")
        c.drawString(70, 750, f"Date: {self.interview_date.text()}")
        c.drawString(70, 730, f"Time: {self.interview_time.text()}")
        c.drawString(70, 710, f"Panel Members: {self.panel_members.toPlainText()}")
        c.save()

    def upload_file(self, label):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Upload File")
        if file_path:
            self.uploaded_files[label] = file_path
            self.uploaded_file_labels[label].setText(os.path.basename(file_path))
            self.uploaded_file_labels[label].setStyleSheet("color: green;")
            self.upload_buttons[label].setText("Unload")
            self.upload_buttons[label].clicked.disconnect()
            self.upload_buttons[label].clicked.connect(lambda _, l=label: self.unload_file(l))

    def unload_file(self, label):
        self.uploaded_files[label] = None
        self.uploaded_file_labels[label].setText("No file uploaded")
        self.uploaded_file_labels[label].setStyleSheet("color: black;")
        self.upload_buttons[label].setText("Upload")
        self.upload_buttons[label].clicked.disconnect()
        self.upload_buttons[label].clicked.connect(lambda _, l=label: self.upload_file(l))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherAdmissionForm()
    window.show()
    sys.exit(app.exec())
