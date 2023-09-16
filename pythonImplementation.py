import pandas as pd
import sqlite3
import xml.etree.ElementTree as ET
import openpyxl
import os

class Framework:
    def __init__(self):
        self.data = None
        self.db_conn = None
        self.xml_tree = None
        self.excel_data = None

    def load_data_from_database(self):
        # Connect to a database (e.g., SQLite)
        self.db_conn = sqlite3.connect('sample.db')
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM my_table")
        self.data = cursor.fetchall()

    def load_data_from_excel(self):
        # Load data from an Excel file
        self.excel_data = []
        self.excel_file = openpyxl.load_workbook('sample.xlsx')
        sheet = self.excel_file.active
        for row in sheet.iter_rows(values_only=True):
            self.excel_data.append(row)

    def load_data_from_xml(self):
        # Parse an XML file
        self.xml_tree = ET.parse('sample.xml')
        root = self.xml_tree.getroot()
        self.data = []
        for element in root.findall('.//record'):
            record = {}
            for child in element:
                record[child.tag] = child.text
            self.data.append(record)

    def process_data(self):
        # Data processing using pandas
        df = pd.DataFrame(self.data)
        # Example: Calculate the mean of a numeric column
        if 'numeric_column' in df.columns:
            mean = df['numeric_column'].mean()
            print(f"Mean of 'numeric_column': {mean}")

    def save_to_database(self):
        # Save processed data to the database
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS processed_data (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
        for row in self.data:
            cursor.execute("INSERT INTO processed_data (name, value) VALUES (?, ?)", (row['name'], row['value']))
        self.db_conn.commit()

    def save_to_excel(self):
        # Save processed data to a new Excel file
        df = pd.DataFrame(self.data)
        df.to_excel('processed_data.xlsx', index=False)

    def perform_common_python_functions(self):
        # Common Python functions
        # Example 1: List comprehensions
        numbers = [1, 2, 3, 4, 5]
        squared_numbers = [x ** 2 for x in numbers]
        print("Squared numbers:", squared_numbers)

        # Example 2: File operations
        with open('example.txt', 'w') as file:
            file.write("Hello, world!")

        # Example 3: OS functions
        current_directory = os.getcwd()
        print("Current directory:", current_directory)

    def run(self):
        self.load_data_from_database()
        self.load_data_from_excel()
        self.load_data_from_xml()
        self.process_data()
        self.save_to_database()
        self.save_to_excel()
        self.perform_common_python_functions()

if __name__ == "__main__":
    framework = Framework()
    framework.run()
