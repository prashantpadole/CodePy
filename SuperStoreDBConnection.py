import pyodbc
import pandas as pd
from datetime import datetime, timedelta

server_name = 'your_server_name'
database_name = 'your_database_name'
username = 'your_username'
password = 'your_password'

sql_query = """
SELECT
    i.ProductName,
    SUM(t.Quantity) AS TotalQuantity
FROM
    InventoryTable AS i
INNER JOIN
    TransactionTable AS t
ON
    i.ProductID = t.ProductID
WHERE
    t.TransactionDate >= ?
GROUP BY
    i.ProductName
ORDER BY
    TotalQuantity DESC
"""

end_date = datetime.now()
start_date = end_date - timedelta(days=90)

start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

conn = pyodbc.connect(
    f'DRIVER={{Sybase ASE ODBC Driver}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
)

cursor = conn.cursor()
cursor.execute(sql_query, start_date_str)

result_df = pd.DataFrame(cursor.fetchall(), columns=['ProductName', 'TotalQuantity'])

conn.close()

result_df.to_csv('most_selling_product_last_quarter.csv', index=False)
