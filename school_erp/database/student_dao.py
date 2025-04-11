from .db_config import db_config
from datetime import datetime
import sqlite3
import os

class StudentDAO:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'school_erp.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            class TEXT NOT NULL,
            section TEXT,
            dob TEXT,
            gender TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            parent_name TEXT,
            admission_date TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS exam_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            exam_name TEXT,
            subject TEXT,
            marks REAL,
            max_marks REAL,
            exam_date TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            date TEXT,
            status TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
        ''')
        
        self.conn.commit()

    def add_student(self, student_data):
        query = '''
        INSERT INTO students (
            student_id, name, roll_no, class, section, dob, gender,
            address, phone, email, parent_name, admission_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (
            student_data['student_id'],
            student_data['name'],
            student_data['roll_no'],
            student_data['class'],
            student_data['section'],
            student_data['dob'],
            student_data['gender'],
            student_data['address'],
            student_data['phone'],
            student_data['email'],
            student_data['parent_name'],
            student_data['admission_date']
        ))
        self.conn.commit()

    def get_student(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        result = self.cursor.fetchone()
        if result:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, result))
        return None

    def update_student(self, student_id, student_data):
        query = '''
        UPDATE students SET
            name = ?, roll_no = ?, class = ?, section = ?, dob = ?,
            gender = ?, address = ?, phone = ?, email = ?,
            parent_name = ?, admission_date = ?
        WHERE student_id = ?
        '''
        self.cursor.execute(query, (
            student_data['name'],
            student_data['roll_no'],
            student_data['class'],
            student_data['section'],
            student_data['dob'],
            student_data['gender'],
            student_data['address'],
            student_data['phone'],
            student_data['email'],
            student_data['parent_name'],
            student_data['admission_date'],
            student_id
        ))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.conn.commit()

    def add_exam_result(self, result_data):
        query = '''
        INSERT INTO exam_results (
            student_id, exam_name, subject, marks, max_marks, exam_date
        ) VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (
            result_data['student_id'],
            result_data['exam_name'],
            result_data['subject'],
            result_data['marks'],
            result_data['max_marks'],
            result_data['exam_date']
        ))
        self.conn.commit()

    def get_exam_results(self, student_id):
        self.cursor.execute('''
        SELECT * FROM exam_results 
        WHERE student_id = ? 
        ORDER BY exam_date DESC
        ''', (student_id,))
        return self.cursor.fetchall()

    def mark_attendance(self, attendance_data):
        query = '''
        INSERT INTO attendance (student_id, date, status)
        VALUES (?, ?, ?)
        '''
        self.cursor.execute(query, (
            attendance_data['student_id'],
            attendance_data['date'],
            attendance_data['status']
        ))
        self.conn.commit()

    def get_attendance(self, student_id):
        self.cursor.execute('''
        SELECT * FROM attendance 
        WHERE student_id = ? 
        ORDER BY date DESC
        ''', (student_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    @staticmethod
    def add_student(name, roll_number, grade, student_id, academic_year):
        """Add a new student to the database"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (name, roll_number, grade, student_id, academic_year)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, roll_number, grade, student_id, academic_year))
            student_id = cursor.lastrowid
            conn.commit()
            return student_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def add_exam_results(student_id, subject_results):
        """Add exam results for a student"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            for subject, scores in subject_results.items():
                cursor.execute('''
                    INSERT INTO exam_results 
                    (student_id, subject, unit_test1, unit_test2, midterm, final, total_score, grade)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    student_id,
                    subject,
                    scores['unit_test1'],
                    scores['unit_test2'],
                    scores['midterm'],
                    scores['final'],
                    scores['total_score'],
                    scores['grade']
                ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding exam results: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_attendance(student_id, present_days, total_days):
        """Update student attendance"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            percentage = (present_days / total_days) * 100 if total_days > 0 else 0
            cursor.execute('''
                INSERT OR REPLACE INTO attendance 
                (student_id, present_days, total_days, percentage)
                VALUES (?, ?, ?, ?)
            ''', (student_id, present_days, total_days, percentage))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating attendance: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_students():
        """Get all students from database"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT s.*, a.percentage as attendance
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id
                ORDER BY s.roll_number
            ''')
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_student_by_roll(roll_number):
        """Get student details by roll number"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT s.*, a.percentage as attendance
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id
                WHERE s.roll_number = ?
            ''', (roll_number,))
            return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_student_results(student_id):
        """Get exam results for a student"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM exam_results
                WHERE student_id = ?
                ORDER BY subject
            ''', (student_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def delete_student(roll_number):
        """Delete a student and their related records"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            # Get student ID first
            cursor.execute('SELECT id FROM students WHERE roll_number = ?', (roll_number,))
            student = cursor.fetchone()
            if not student:
                return False

            student_id = student[0]

            # Delete related records
            cursor.execute('DELETE FROM exam_results WHERE student_id = ?', (student_id,))
            cursor.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def search_students(query):
        """Search students by name or roll number"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT s.*, a.percentage as attendance
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id
                WHERE s.name LIKE ? OR s.roll_number LIKE ?
                ORDER BY s.roll_number
            ''', (f'%{query}%', f'%{query}%'))
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def calculate_exam_statistics(student_id):
        """Calculate exam statistics for a student"""
        conn = db_config.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 
                    AVG(total_score) as avg_score,
                    MIN(total_score) as min_score,
                    MAX(total_score) as max_score,
                    COUNT(*) as total_subjects
                FROM exam_results
                WHERE student_id = ?
            ''', (student_id,))
            return cursor.fetchone()
        finally:
            conn.close()

# Create an instance of StudentDAO
student_dao = StudentDAO()
