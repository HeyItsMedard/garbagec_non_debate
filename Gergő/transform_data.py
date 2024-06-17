import pandas as pd
import json


df = pd.read_excel('../SalesData.xlsx')

transformed_data = {}

for _, row in df.iterrows():
    order_number = str(row['OrderNumber'])
    if order_number not in transformed_data:
        transformed_data[order_number] = {
            'channel': row['Channel'],
            'order_date': row['OrderDate'].strftime('%Y-%m-%d'),
            'salesperson': row['Salesperson'],
            'supervisor': row['Supervisor'],
            'manager': row['Manager'],
            'products': [{ 'product_key': row['ProductKey'], 'quantity': row['Quantity'], 'unit_price': row['UnitPrice'] }]
        }
    else:
        transformed_data[order_number]['products'].append({
            'product_key': row['ProductKey'],
            'quantity': row['Quantity'],
            'unit_price': row['UnitPrice']
        })

with open('transformed_data.json', 'w') as f:
    json.dump(transformed_data, f)
    
