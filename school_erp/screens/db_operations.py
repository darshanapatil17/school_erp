from database import db
from datetime import datetime

class TeacherOperations:
    @staticmethod
    def get_teacher(teacher_id):
        """Get teacher details by ID"""
        return db.get_teacher_details(teacher_id)
    
    @staticmethod
    def add_teacher(teacher_data):
        """Add a new teacher"""
        try:
            db.add_teacher(teacher_data)
            return True, "Teacher added successfully"
        except Exception as e:
            return False, f"Error adding teacher: {str(e)}"
    
    @staticmethod
    def update_salary(teacher_id, salary_data):
        """Update teacher's salary structure"""
        try:
            db.update_salary_structure(teacher_id, salary_data)
            return True, "Salary structure updated successfully"
        except Exception as e:
            return False, f"Error updating salary: {str(e)}"

class PayrollOperations:
    @staticmethod
    def process_salary(teacher_id, month_year, working_days, holidays):
        """Process salary for a teacher"""
        try:
            # Get teacher details with salary structure
            teacher = db.get_teacher_details(teacher_id)
            if not teacher:
                return False, "Teacher not found"
            
            # Calculate earnings
            total_earnings = sum([
                float(teacher.get('basic_salary', 0)),
                float(teacher.get('da_amount', 0)),
                float(teacher.get('hra_amount', 0)),
                float(teacher.get('conveyance', 0)),
                float(teacher.get('medical', 0)),
                float(teacher.get('other_allowances', 0))
            ])
            
            # Calculate deductions
            total_deductions = sum([
                float(teacher.get('pf_deduction', 0)),
                float(teacher.get('professional_tax', 0)),
                float(teacher.get('income_tax', 0)),
                float(teacher.get('other_deductions', 0))
            ])
            
            # Calculate net salary
            net_salary = total_earnings - total_deductions
            
            return True, {
                'teacher_name': teacher['name'],
                'total_earnings': total_earnings,
                'total_deductions': total_deductions,
                'net_salary': net_salary,
                'month_year': month_year,
                'working_days': working_days,
                'holidays': holidays
            }
        except Exception as e:
            return False, f"Error processing salary: {str(e)}"
    
    @staticmethod
    def record_payment(payment_data):
        """Record a salary payment"""
        try:
            payment_id = db.record_salary_payment(payment_data)
            return True, f"Payment recorded with ID: {payment_id}"
        except Exception as e:
            return False, f"Error recording payment: {str(e)}"
    
    @staticmethod
    def get_payment_history(teacher_id):
        """Get payment history for a teacher"""
        try:
            history = db.get_payment_history(teacher_id)
            return True, history
        except Exception as e:
            return False, f"Error fetching payment history: {str(e)}"

class ReportOperations:
    @staticmethod
    def generate_salary_slip(teacher_id, month_year):
        """Generate salary slip data"""
        try:
            # Get teacher details
            teacher = db.get_teacher_details(teacher_id)
            if not teacher:
                return False, "Teacher not found"
            
            # Get payment record for the month
            payments = db.get_payment_history(teacher_id)
            payment = next((p for p in payments if p[3] == month_year), None)
            
            if not payment:
                return False, "Payment record not found for the specified month"
            
            slip_data = {
                'teacher': teacher,
                'payment': {
                    'payment_date': payment[2],
                    'month_year': payment[3],
                    'working_days': payment[4],
                    'holidays': payment[5],
                    'total_earnings': payment[6],
                    'total_deductions': payment[7],
                    'net_salary': payment[8],
                    'payment_method': payment[9],
                    'payment_status': payment[10]
                }
            }
            
            return True, slip_data
        except Exception as e:
            return False, f"Error generating salary slip: {str(e)}"
    
    @staticmethod
    def get_monthly_payroll_summary(month_year):
        """Get summary of all payments for a month"""
        try:
            query = '''
            SELECT 
                t.name,
                t.department,
                p.total_earnings,
                p.total_deductions,
                p.net_salary,
                p.payment_status
            FROM salary_payments p
            JOIN teachers t ON p.teacher_id = t.teacher_id
            WHERE p.month_year = ?
            '''
            db.cursor.execute(query, (month_year,))
            results = db.cursor.fetchall()
            
            summary = {
                'month_year': month_year,
                'total_payments': len(results),
                'total_amount': sum(r[4] for r in results),
                'payments': [{
                    'name': r[0],
                    'department': r[1],
                    'earnings': r[2],
                    'deductions': r[3],
                    'net_salary': r[4],
                    'status': r[5]
                } for r in results]
            }
            
            return True, summary
        except Exception as e:
            return False, f"Error generating monthly summary: {str(e)}" 