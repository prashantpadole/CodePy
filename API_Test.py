import requests
import json
import openpyxl

api_url = 'https://superstore.com/api/your_endpoint'
output_excel_file = 'transaction_details.xlsx'

try:
    response = requests.get(api_url)
    response_data = response.json()

    successful_transactions = []
    failed_transactions = []

    for item in response_data:
        if 'response_code' in item:
            if item['response_code'] == 'success':
                successful_transactions.append(item)
            elif item['response_code'] == 'failure':
                failed_transactions.append(item)

    workbook = openpyxl.Workbook()

    sheet_success = workbook.active
    sheet_success.title = "Successful Transition"
    sheet_success.append(["TransactionDate", "CustomerName", "ProductName", "Quantity", "UnitPrice", "TotalPrice"])

    for transaction in successful_transactions:
        sheet_success.append([transaction['TransactionDate'], transaction['CustomerName'], transaction['ProductName'], 
                              transaction['Quantity'], transaction['UnitPrice'], transaction['TotalPrice']])

    sheet_failure = workbook.create_sheet("Failed Transition")
    sheet_failure.append(["TransactionDate", "CustomerName", "ProductName", "Quantity", "UnitPrice", "TotalPrice"])

    for transaction in failed_transactions:
        sheet_failure.append([transaction['TransactionDate'], transaction['CustomerName'], transaction['ProductName'], 
                              transaction['Quantity'], transaction['UnitPrice'], transaction['TotalPrice']])

    workbook.save(output_excel_file)

    print(f'Data saved to {output_excel_file}')
except requests.exceptions.RequestException as e:
    print(f'An error occurred while making the API request: {e}')
except json.JSONDecodeError as e:
    print(f'Error decoding JSON response: {e}')
