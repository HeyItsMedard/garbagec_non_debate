import pandas as pd
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import time
import uuid

cluster = Cluster(['localhost'], port=9042) 
session = cluster.connect()

session.set_keyspace('mykeyspace')
session.execute("DROP TABLE IF EXISTS sales_data")
session.execute("DROP TABLE IF EXISTS sales_person")
session.execute("CREATE TABLE IF NOT EXISTS sales_data (id UUID PRIMARY KEY, ordernumber INT, orderdate DATE, productkey INT, SalesPersonKey INT, Supervisor TEXT, Manager TEXT, Channel TEXT, Quantity INT, Unit_price FLOAT)")
session.execute("CREATE TABLE IF NOT EXISTS sales_person (salespersonkey INT PRIMARY KEY, name TEXT)")
df = pd.read_excel('SalesData.xlsx')

def write_cassandra(df, size=len(df)):


    insert_data_query = "INSERT INTO sales_data (id, ordernumber, orderdate, productkey, SalesPersonKey, Supervisor, Manager, Channel, Quantity, Unit_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    insert_sales_query = "INSERT INTO sales_person (salespersonkey, name) VALUES (?, ?)"
    prepared_data = session.prepare(insert_data_query)
    prepared_sales = session.prepare(insert_sales_query)
    count = 0

    batch_size = 100

    start_time = time.time()
    batch = BatchStatement()

    for index, row in df.iterrows():

        unit_price = row['UnitPrice']
        if isinstance(unit_price, str):
            unit_price = float(unit_price.replace('$', ''))

        new_uuid = uuid.uuid4()

        batch.add(prepared_data, (
                                new_uuid,
                                row['OrderNumber'], 
                                row['OrderDate'].strftime('%Y-%m-%d'), 
                                row['ProductKey'],
                                row['SalespersonKey'],
                                row['Supervisor'],
                                row['Manager'],
                                row['Channel'],
                                row['Quantity'],
                                unit_price
                                ))
        batch.add(prepared_sales, (row['SalespersonKey'], 
                                        row['Salesperson']))
        count += 1
        print(count)

        if count % batch_size == 0:
            session.execute(batch)
            batch.clear()

        if count == size:
            break

    # A maradék batch végrehajtása, ha van
    if len(batch) > 0:
        session.execute(batch)
        
    end_time = time.time()



    execution_time = end_time - start_time
    # print("Time: ", execution_time, "seconds")
    return execution_time