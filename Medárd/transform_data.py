import pandas as pd
from pyravendb.store import document_store
import time

# Definiáljuk az adatok osztályát
class SalesData:
    def __init__(self, order_date, order_number, product_key, salesperson_key, salesperson, supervisor, manager, channel, quantity, unit_price):
        self.OrderDate = order_date
        self.OrderNumber = order_number
        self.ProductKey = product_key
        self.SalespersonKey = salesperson_key
        self.Salesperson = salesperson
        self.Supervisor = supervisor
        self.Manager = manager
        self.Channel = channel
        self.Quantity = quantity
        self.UnitPrice = unit_price

# RavenDB inicializálása
store = document_store.DocumentStore(urls=['http://127.0.0.1:58712'], database='TestDatabase')
store.initialize()

# Adatok betöltése
df = pd.read_excel('SalesData.xlsx')

# Adatok átalakítása RavenDB formátumra
documents = []
for index, row in df.iterrows():
    unit_price = row['UnitPrice']
    if isinstance(unit_price, str):
        unit_price = float(unit_price.replace('$', ''))
        
    document = SalesData(
        order_date=row['OrderDate'].strftime('%Y-%m-%d'),
        order_number=row['OrderNumber'],
        product_key=row['ProductKey'],
        salesperson_key=row['SalespersonKey'],
        salesperson=row['Salesperson'],
        supervisor=row['Supervisor'],
        manager=row['Manager'],
        channel=row['Channel'],
        quantity=row['Quantity'],
        unit_price=unit_price
    )
    documents.append(document)

# Adatok elmentése RavenDB-be
start_time = time.time()
with store.open_session() as session:
    for document in documents:
        session.store(document)
    session.save_changes()
end_time = time.time()

execution_time = end_time - start_time
print("Execution time:", execution_time, "seconds")
print("Adatok sikeresen feltöltve RavenDB-be.")
