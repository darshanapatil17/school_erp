from database import db

# Add a test teacher
teacher_data = {
    'teacher_id': 'T001',
    'name': 'John Smith',
    'mother_name': 'Mary Smith',
    'dob': '1985-05-15',
    'age': 38,
    'cast_category': 'General',
    'place': 'Mumbai',
    'tal': 'Mumbai',
    'dist': 'Mumbai',
    'state': 'Maharashtra',
    'adar_no': '123456789012',
    'contact_no': '9876543210',
    'designation': 'Senior Teacher',
    'department': 'Mathematics',
    'joining_date': '2020-01-01',
    'bank_account': 'SBI123456789',
    'pf_no': 'PF123456'
}

# Add salary structure
salary_data = {
    'basic_salary': 50000.0,
    'da_amount': 5000.0,
    'hra_amount': 7500.0,
    'conveyance': 2000.0,
    'medical': 1500.0,
    'other_allowances': 3000.0,
    'pf_deduction': 6000.0,
    'professional_tax': 200.0,
    'income_tax': 5000.0,
    'other_deductions': 1000.0
}

try:
    # Add teacher
    db.add_teacher(teacher_data)
    print("Teacher added successfully!")
    
    # Add salary structure
    db.update_salary_structure('T001', salary_data)
    print("Salary structure added successfully!")
    
except Exception as e:
    print(f"Error: {str(e)}")

print("\nYou can now use Teacher ID: T001 in the salary slip generator.") 