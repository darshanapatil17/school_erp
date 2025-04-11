from database import db

def view_all_data():
    print("\n=== TEACHERS DATA ===")
    print("-" * 100)
    
    # Get all teachers
    db.cursor.execute("SELECT * FROM teachers")
    teachers = db.cursor.fetchall()
    
    for teacher in teachers:
        print("\nTeacher Details:")
        print(f"Name: {teacher[1]}")
        print(f"ID: {teacher[0]}")
        print(f"Mother's Name: {teacher[2]}")
        print(f"DOB: {teacher[3]}")
        print(f"Department: {teacher[13]}")
        print(f"Designation: {teacher[12]}")
        print(f"Contact: {teacher[11]}")
        print(f"Aadhar: {teacher[10]}")
        print("-" * 50)
        
        # Get salary structure for this teacher
        db.cursor.execute("SELECT * FROM salary_structure WHERE teacher_id = ?", (teacher[0],))
        salary = db.cursor.fetchone()
        if salary:
            print("Salary Structure:")
            print(f"Basic Salary: ₹{salary[1]}")
            print(f"DA: ₹{salary[2]}")
            print(f"HRA: ₹{salary[3]}")
            print(f"Conveyance: ₹{salary[4]}")
            print(f"Medical: ₹{salary[5]}")
            print(f"Other Allowances: ₹{salary[6]}")
            print("\nDeductions:")
            print(f"PF: ₹{salary[7]}")
            print(f"Professional Tax: ₹{salary[8]}")
            print(f"Income Tax: ₹{salary[9]}")
            print(f"Other Deductions: ₹{salary[10]}")
        print("=" * 100)
        
        # Get payment history
        db.cursor.execute("SELECT * FROM salary_payments WHERE teacher_id = ?", (teacher[0],))
        payments = db.cursor.fetchall()
        if payments:
            print("\nPayment History:")
            for payment in payments:
                print(f"\nMonth/Year: {payment[3]}")
                print(f"Payment Date: {payment[2]}")
                print(f"Working Days: {payment[4]}")
                print(f"Holidays: {payment[5]}")
                print(f"Total Earnings: ₹{payment[6]}")
                print(f"Total Deductions: ₹{payment[7]}")
                print(f"Net Salary: ₹{payment[8]}")
                print(f"Payment Method: {payment[9]}")
                print(f"Status: {payment[10]}")
        print("\n" + "=" * 100)

if __name__ == "__main__":
    print("Viewing Database Contents...")
    view_all_data()
    print("\nDone viewing data!") 