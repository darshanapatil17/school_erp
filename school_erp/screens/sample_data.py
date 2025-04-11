from datetime import datetime, timedelta
import random

# Sample data generator for teachers
class SampleData:
    @staticmethod
    def generate_sample_teachers():
        teachers = [
            {
                'id': 'T001',
                'name': 'Rajesh Kumar',
                'designation': 'Senior Mathematics Teacher',
                'department': 'Mathematics',
                'joining_date': '01-04-2018',
                'bank_account': '1234567890',
                'pf_number': 'PF123456',
                'basic_salary': 45000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 3000,
                'medical': 2500,
                'other_allowances': 2000,
                'pf_deduction': 5400,
                'professional_tax': 200,
                'income_tax': 3500,
                'other_deductions': 1000
            },
            {
                'id': 'T002',
                'name': 'Priya Sharma',
                'designation': 'Senior Science Teacher',
                'department': 'Science',
                'joining_date': '15-06-2019',
                'bank_account': '2345678901',
                'pf_number': 'PF234567',
                'basic_salary': 42000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 3000,
                'medical': 2500,
                'other_allowances': 1800,
                'pf_deduction': 5040,
                'professional_tax': 200,
                'income_tax': 3200,
                'other_deductions': 800
            },
            {
                'id': 'T003',
                'name': 'Amit Patel',
                'designation': 'English Teacher',
                'department': 'English',
                'joining_date': '01-07-2020',
                'bank_account': '3456789012',
                'pf_number': 'PF345678',
                'basic_salary': 38000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1500,
                'pf_deduction': 4560,
                'professional_tax': 200,
                'income_tax': 2800,
                'other_deductions': 700
            },
            {
                'id': 'T004',
                'name': 'Sneha Gupta',
                'designation': 'Physics Teacher',
                'department': 'Science',
                'joining_date': '01-08-2019',
                'bank_account': '4567890123',
                'pf_number': 'PF456789',
                'basic_salary': 40000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 3000,
                'medical': 2500,
                'other_allowances': 1800,
                'pf_deduction': 4800,
                'professional_tax': 200,
                'income_tax': 3000,
                'other_deductions': 800
            },
            {
                'id': 'T005',
                'name': 'Anita Desai',
                'designation': 'Chemistry Teacher',
                'department': 'Science',
                'joining_date': '15-07-2018',
                'bank_account': '5678901234',
                'pf_number': 'PF567890',
                'basic_salary': 41000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 3000,
                'medical': 2500,
                'other_allowances': 1900,
                'pf_deduction': 4920,
                'professional_tax': 200,
                'income_tax': 3100,
                'other_deductions': 850
            },
            {
                'id': 'T006',
                'name': 'Suresh Verma',
                'designation': 'Hindi Teacher',
                'department': 'Hindi',
                'joining_date': '01-04-2021',
                'bank_account': '6789012345',
                'pf_number': 'PF678901',
                'basic_salary': 35000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1500,
                'pf_deduction': 4200,
                'professional_tax': 200,
                'income_tax': 2500,
                'other_deductions': 600
            },
            {
                'id': 'T007',
                'name': 'Meera Iyer',
                'designation': 'Biology Teacher',
                'department': 'Science',
                'joining_date': '01-06-2020',
                'bank_account': '7890123456',
                'pf_number': 'PF789012',
                'basic_salary': 39000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 3000,
                'medical': 2500,
                'other_allowances': 1700,
                'pf_deduction': 4680,
                'professional_tax': 200,
                'income_tax': 2900,
                'other_deductions': 750
            },
            {
                'id': 'T008',
                'name': 'Rahul Mehta',
                'designation': 'Computer Science Teacher',
                'department': 'Computer Science',
                'joining_date': '15-08-2019',
                'bank_account': '8901234567',
                'pf_number': 'PF890123',
                'basic_salary': 43000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 3000,
                'medical': 2500,
                'other_allowances': 2000,
                'pf_deduction': 5160,
                'professional_tax': 200,
                'income_tax': 3300,
                'other_deductions': 900
            },
            {
                'id': 'T009',
                'name': 'Kavita Reddy',
                'designation': 'Social Studies Teacher',
                'department': 'Social Studies',
                'joining_date': '01-07-2018',
                'bank_account': '9012345678',
                'pf_number': 'PF901234',
                'basic_salary': 37000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1600,
                'pf_deduction': 4440,
                'professional_tax': 200,
                'income_tax': 2700,
                'other_deductions': 650
            },
            {
                'id': 'T010',
                'name': 'Deepak Singh',
                'designation': 'Physical Education Teacher',
                'department': 'Physical Education',
                'joining_date': '01-04-2020',
                'bank_account': '0123456789',
                'pf_number': 'PF012345',
                'basic_salary': 36000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1500,
                'pf_deduction': 4320,
                'professional_tax': 200,
                'income_tax': 2600,
                'other_deductions': 600
            },
            # Additional 10 teachers with varied data
            {
                'id': 'T011',
                'name': 'Sanjay Joshi',
                'designation': 'Art Teacher',
                'department': 'Art',
                'joining_date': '01-08-2021',
                'bank_account': '1122334455',
                'pf_number': 'PF112233',
                'basic_salary': 34000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1400,
                'pf_deduction': 4080,
                'professional_tax': 200,
                'income_tax': 2400,
                'other_deductions': 550
            },
            {
                'id': 'T012',
                'name': 'Neha Kapoor',
                'designation': 'Music Teacher',
                'department': 'Music',
                'joining_date': '15-06-2020',
                'bank_account': '2233445566',
                'pf_number': 'PF223344',
                'basic_salary': 35000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1500,
                'pf_deduction': 4200,
                'professional_tax': 200,
                'income_tax': 2500,
                'other_deductions': 600
            },
            {
                'id': 'T013',
                'name': 'Vikram Malhotra',
                'designation': 'Mathematics Teacher',
                'department': 'Mathematics',
                'joining_date': '01-07-2019',
                'bank_account': '3344556677',
                'pf_number': 'PF334455',
                'basic_salary': 38000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1600,
                'pf_deduction': 4560,
                'professional_tax': 200,
                'income_tax': 2800,
                'other_deductions': 700
            },
            {
                'id': 'T014',
                'name': 'Ritu Sharma',
                'designation': 'English Teacher',
                'department': 'English',
                'joining_date': '01-04-2020',
                'bank_account': '4455667788',
                'pf_number': 'PF445566',
                'basic_salary': 37000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1500,
                'pf_deduction': 4440,
                'professional_tax': 200,
                'income_tax': 2700,
                'other_deductions': 650
            },
            {
                'id': 'T015',
                'name': 'Arun Kumar',
                'designation': 'Science Teacher',
                'department': 'Science',
                'joining_date': '15-07-2021',
                'bank_account': '5566778899',
                'pf_number': 'PF556677',
                'basic_salary': 36000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1500,
                'pf_deduction': 4320,
                'professional_tax': 200,
                'income_tax': 2600,
                'other_deductions': 600
            },
            {
                'id': 'T016',
                'name': 'Pooja Gupta',
                'designation': 'Hindi Teacher',
                'department': 'Hindi',
                'joining_date': '01-08-2020',
                'bank_account': '6677889900',
                'pf_number': 'PF667788',
                'basic_salary': 35000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1400,
                'pf_deduction': 4200,
                'professional_tax': 200,
                'income_tax': 2500,
                'other_deductions': 550
            },
            {
                'id': 'T017',
                'name': 'Manoj Tiwari',
                'designation': 'Sanskrit Teacher',
                'department': 'Sanskrit',
                'joining_date': '15-06-2019',
                'bank_account': '7788990011',
                'pf_number': 'PF778899',
                'basic_salary': 34000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1400,
                'pf_deduction': 4080,
                'professional_tax': 200,
                'income_tax': 2400,
                'other_deductions': 500
            },
            {
                'id': 'T018',
                'name': 'Anjali Sood',
                'designation': 'Geography Teacher',
                'department': 'Social Studies',
                'joining_date': '01-04-2021',
                'bank_account': '8899001122',
                'pf_number': 'PF889900',
                'basic_salary': 36000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1500,
                'pf_deduction': 4320,
                'professional_tax': 200,
                'income_tax': 2600,
                'other_deductions': 600
            },
            {
                'id': 'T019',
                'name': 'Rajendra Prasad',
                'designation': 'History Teacher',
                'department': 'Social Studies',
                'joining_date': '15-07-2020',
                'bank_account': '9900112233',
                'pf_number': 'PF990011',
                'basic_salary': 37000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 2500,
                'medical': 2000,
                'other_allowances': 1600,
                'pf_deduction': 4440,
                'professional_tax': 200,
                'income_tax': 2700,
                'other_deductions': 650
            },
            {
                'id': 'T020',
                'name': 'Sunita Rao',
                'designation': 'Economics Teacher',
                'department': 'Commerce',
                'joining_date': '01-08-2019',
                'bank_account': '0011223344',
                'pf_number': 'PF001122',
                'basic_salary': 39000,
                'da_percent': 15,
                'hra_percent': 20,
                'conveyance': 3000,
                'medical': 2500,
                'other_allowances': 1700,
                'pf_deduction': 4680,
                'professional_tax': 200,
                'income_tax': 2900,
                'other_deductions': 750
            }
        ]
        return teachers

    def get_sample_teachers(self):
        """Generate sample teacher data"""
        return [
            {
                'id': 'T001',
                'name': 'John Smith',
                'designation': 'Senior Teacher',
                'department': 'Mathematics',
                'joining_date': '2020-01-15',
                'bank_account': '123456789012',
                'pf_number': 'PF001',
                'basic_salary': 50000,
                'da': 25000,
                'hra': 15000,
                'conveyance': 2000,
                'medical': 2000,
                'other_allowances': 5000,
                'pf': 6000,
                'professional_tax': 2000,
                'income_tax': 5000,
                'other_deductions': 1000
            },
            {
                'id': 'T002',
                'name': 'Sarah Johnson',
                'designation': 'Assistant Teacher',
                'department': 'Science',
                'joining_date': '2021-03-20',
                'bank_account': '987654321098',
                'pf_number': 'PF002',
                'basic_salary': 40000,
                'da': 20000,
                'hra': 12000,
                'conveyance': 2000,
                'medical': 2000,
                'other_allowances': 4000,
                'pf': 4800,
                'professional_tax': 2000,
                'income_tax': 4000,
                'other_deductions': 1000
            },
            {
                'id': 'T003',
                'name': 'Michael Brown',
                'designation': 'Head Teacher',
                'department': 'English',
                'joining_date': '2019-06-10',
                'bank_account': '456789012345',
                'pf_number': 'PF003',
                'basic_salary': 60000,
                'da': 30000,
                'hra': 18000,
                'conveyance': 2000,
                'medical': 2000,
                'other_allowances': 6000,
                'pf': 7200,
                'professional_tax': 2000,
                'income_tax': 6000,
                'other_deductions': 1000
            }
        ] 