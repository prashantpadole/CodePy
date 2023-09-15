import csv
import requests
import xml.etree.ElementTree as ET
from openpyxl import Workbook

csv_file = 'superstore_transactions.csv'
server_url = 'http://your-soap-server-url-here'
output_excel_file = 'transaction_details.xlsx'

xml_requests = []
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        xml_request = f'''
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:ns1="your-namespace-here">
                <SOAP-ENV:Body>
                    <ns1:YourSOAPRequestTag>
                        <TransactionDate>{row['TransactionDate']}</TransactionDate>
                        <CustomerName>{row['CustomerName']}</CustomerName>
                        <ProductName>{row['ProductName']}</ProductName>
                        <Quantity>{row['Quantity']}</Quantity>
                        <UnitPrice>{row['UnitPrice']}</UnitPrice>
                        <TotalPrice>{row['TotalPrice']}</TotalPrice>
                    </ns1:YourSOAPRequestTag>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>
        '''
        xml_requests.append(xml_request)

xml_responses = []
for xml_request in xml_requests:
    headers = {'Content-Type': 'text/xml'}
    response = requests.post(server_url, data=xml_request, headers=headers)
    xml_responses.append(response.text)

workbook = Workbook()
sheet = workbook.active
sheet.title = "Transaction Details"

sheet.append(["TransactionDate", "ResponseData"])

for response in xml_responses:
    root = ET.fromstring(response)
    response_data = root.find('.//ResponseData').text if root.find('.//ResponseData') is not None else ''
    sheet.append([row['TransactionDate'], response_data])

workbook.save(output_excel_file)

print(f'Responses parsed and saved to {output_excel_file}')
