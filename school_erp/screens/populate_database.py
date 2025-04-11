from database import db

def populate_teachers():
    # Sample teacher data from the image
    teachers = [
        {
            'teacher_id': '2348458527',  # Using Adar No as teacher ID
            'name': 'Jaid Athim Ankush',
            'mother_name': 'SEENA',
            'dob': '15-09-2010',
            'age': 13,
            'cast_category': 'HINDU MARATHA',
            'place': 'CHAKAN',
            'tal': 'KHED',
            'dist': 'PUNE',
            'state': 'MAHARASHTRA',
            'adar_no': '234845852527',
            'contact_no': '201727250817005018',
            'designation': 'Teacher',
            'department': 'Mathematics',
            'joining_date': '2024-01-01',
            'bank_account': 'XXXXXXXXXX123',
            'pf_no': 'PF123456'
        },
        # Add more teachers from your image here
    ]

    # Sample salary structure
    salary_structures = {
        '2348458527': {
            'basic_salary': 150000,
            'da_amount': 1500,
            'hra_amount': 1600,
            'conveyance': 1700,
            'medical': 1800,
            'other_allowances': 1900,
            'pf_deduction': 2000,
            'professional_tax': 2100,
            'income_tax': 2200,
            'other_deductions': 500
        }
    }

    # Add teachers to database
    for teacher in teachers:
        try:
            # Add teacher basic info
            db.add_teacher(teacher)
            
            # Add salary structure if exists
            if teacher['teacher_id'] in salary_structures:
                db.update_salary_structure(
                    teacher['teacher_id'],
                    salary_structures[teacher['teacher_id']]
                )
            print(f"Added teacher: {teacher['name']}")
        except Exception as e:
            print(f"Error adding teacher {teacher['name']}: {str(e)}")

def add_all_teachers_from_image():
    teachers = [
        {
            'teacher_id': '1',  # Using row number as teacher ID
            'name': 'Babade Ravindra Shrishail',
            'mother_name': 'JYOTI',
            'dob': '06-03-2011',
            'age': 12,
            'cast_category': 'Hindu Lingayat',
            'place': 'Alandi',
            'tal': 'Haveli',
            'dist': 'PUNE',
            'state': 'MAHARASHTRA',
            'adar_no': '554726545-11',
            'contact_no': '',
            'designation': 'Teacher',
            'department': 'Class 6th',
            'joining_date': '2024-01-01',
            'bank_account': 'XXXXXXXXXX123',
            'pf_no': 'PF001'
        },
        {
            'teacher_id': '2',
            'name': 'Bankar Soham Jitendra',
            'mother_name': 'PRAJAKTA',
            'dob': '16-02-2011',
            'age': 12,
            'cast_category': 'HINDU MALI',
            'place': 'PIMPRI',
            'tal': 'HAVELI',
            'dist': 'PUNE',
            'state': 'MAHARASHTRA',
            'adar_no': '554721654519',
            'contact_no': '201727250817005009',
            'designation': 'Teacher',
            'department': 'Class 6th',
            'joining_date': '2024-01-01',
            'bank_account': 'XXXXXXXXXX124',
            'pf_no': 'PF002'
        },
        # Add more teachers from the image...
    ]

    # Default salary structure template
    default_salary = {
        'basic_salary': 150000,
        'da_amount': 1500,
        'hra_amount': 1600,
        'conveyance': 1700,
        'medical': 1800,
        'other_allowances': 1900,
        'pf_deduction': 2000,
        'professional_tax': 2100,
        'income_tax': 2200,
        'other_deductions': 500
    }

    # Add each teacher and their salary structure
    for teacher in teachers:
        try:
            # Add teacher basic info
            db.add_teacher(teacher)
            
            # Add default salary structure
            db.update_salary_structure(teacher['teacher_id'], default_salary)
            
            print(f"Successfully added teacher: {teacher['name']}")
        except Exception as e:
            print(f"Error adding teacher {teacher['name']}: {str(e)}")

if __name__ == "__main__":
    print("Starting database population...")
    add_all_teachers_from_image()
    print("Database population completed!") 