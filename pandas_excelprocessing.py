import pandas as pd

class SuperstoreDataProcessor:
    def __init__(self, excel_file):
        self.excel_file = excel_file

    def read_data(self):
        xls = pd.ExcelFile(self.excel_file)
        self.data = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

    def transform_data(self):
        employee_data = self.data.get('employee')
        if employee_data is not None:
            employee_data['YearsWithSuperstore'] = pd.to_datetime('now') - pd.to_datetime(employee_data['JoiningDate'])
            employee_data['YearsWithSuperstore'] = employee_data['YearsWithSuperstore'].apply(lambda x: x.days // 365)
            employee_data['NextYearSalary'] = employee_data.apply(self.calculate_next_year_salary, axis=1)

    def calculate_next_year_salary(self, row):
        age_factor = 1.02
        experience_factor = 1.03
        sales_factor = 1.01

        next_year_salary = row['CurrentSalary']
        next_year_salary *= age_factor ** row['Age']
        next_year_salary *= experience_factor ** row['YearsOfExperience']
        next_year_salary *= sales_factor ** (row['TotalSales'] / 1000)

        return next_year_salary

    def generate_report(self, output_csv):
        employee_data = self.data.get('employee')
        if employee_data is not None:
            employee_data.to_csv(output_csv, index=False)

excel_file_path = 'superstore_data.xlsx'
output_csv_path = 'superstore_salary_report.csv'

data_processor = SuperstoreDataProcessor(excel_file_path)
data_processor.read_data()
data_processor.transform_data()
data_processor.generate_report(output_csv_path)

print("Salary report generated successfully and saved as", output_csv_path)
