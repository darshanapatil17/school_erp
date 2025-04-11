import pandas as pd
import os

def create_sample_data():
    # Sample data for teachers
    data = {
        'Employee ID': [
            'T001', 'T002', 'T003', 'T004', 'T005', 'T006',
            'T007', 'T008', 'T009', 'T010', 'T011', 'T012'
        ],
        'Employee Name': [
            'Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Sneha Gupta',
            'Anita Desai', 'Suresh Verma', 'Rajesh sharma', 'Priya Patel',
            'Amit Patel', 'Sneha Singh', 'Anita Gupta', 'Suresh Desai'
        ],
        'Designation': [
            'Senior Mathematics Teacher', 'Senior Science Teacher', 'English Teacher',
            'Physics Teacher', 'Chemistry Teacher', 'Hindi Teacher',
            'Senior Mathematics Teacher', 'Senior Science Teacher', 'English Teacher',
            'Physics Teacher', 'Chemistry Teacher', 'Hindi Teacher'
        ],
        'Department': [
            'Mathematics', 'Science', 'English', 'Science', 'Science', 'Hindi',
            'Mathematics', 'Science', 'English', 'Science', 'Science', 'Hindi'
        ],
        'Date of Joining': [
            '01-04-2018', '15-06-2019', '01-07-2020', '01-08-2019',
            '15-07-2018', '01-04-2021', '01-04-2018', '15-06-2019',
            '01-07-2020', '01-08-2019', '15-07-2018', '01-04-2021'
        ],
        'Bank Account': [
            '1234567890', '2345678901', '3456789012', '4567890123',
            '5678901234', '6789012345', '1234567890', '2345678901',
            '3456789012', '4567890123', '5678901234', '6789012345'
        ],
        'PF Number': [
            'PF123456', 'PF234567', 'PF345678', 'PF456789',
            'PF567890', 'PF678901', 'PF123456', 'PF234567',
            'PF345678', 'PF456789', 'PF567890', 'PF678901'
        ],
        'Basic Salary': [
            45000, 42000, 38000, 40000, 41000, 35000,
            45000, 42000, 38000, 40000, 41000, 35000
        ],
        'DA Percent': [15] * 12,  # 15% for all employees
        'HRA Percent': [20] * 12,  # 20% for all employees
        'Conveyance': [
            3000, 3000, 2500, 3000, 3000, 2500,
            3000, 3000, 2500, 3000, 3000, 2500
        ],
        'Medical': [
            2500, 2500, 2000, 2500, 2500, 2000,
            2500, 2500, 2000, 2500, 2500, 2000
        ],
        'Other Allowances': [
            2000, 1800, 1500, 1800, 1900, 1500,
            2000, 1800, 1500, 1800, 1900, 1500
        ],
        'PF Deduction': [
            5400, 5040, 4560, 4800, 4920, 4200,
            5400, 5040, 4560, 4800, 4920, 4200
        ],
        'Professional Tax': [200] * 12,  # 200 for all employees
        'Income Tax': [
            3500, 3200, 2800, 3000, 3100, 2500,
            3500, 3200, 2800, 3000, 3100, 2500
        ],
        'Other Deductions': [
            1000, 800, 700, 800, 850, 600,
            1000, 800, 700, 800, 850, 600
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Get the absolute path to the database directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(current_dir, 'teachers_data.xlsx')
    
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(excel_path), exist_ok=True)
        
        # Save to Excel file
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"Excel file created successfully at: {excel_path}")
        print("\nEmployee Details:")
        print("-" * 120)
        print(f"{'ID':<8} {'Name':<20} {'Designation':<30} {'Department':<15} {'Basic Salary':>12} {'DA%':>6} {'HRA%':>6}")
        print("-" * 120)
        for i in range(len(data['Employee ID'])):
            print(f"{data['Employee ID'][i]:<8} {data['Employee Name'][i]:<20} {data['Designation'][i]:<30} "
                  f"{data['Department'][i]:<15} {data['Basic Salary'][i]:>12} {data['DA Percent'][i]:>6} "
                  f"{data['HRA Percent'][i]:>6}")
        print("-" * 120)
        return True
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")
        return False

if __name__ == "__main__":
    create_sample_data()
