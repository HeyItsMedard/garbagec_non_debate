from cassandra.cluster import Cluster
import time

cluster = Cluster(['localhost'], port=9042) 
session = cluster.connect()

session.set_keyspace('mykeyspace')

def measure_query_time(field, value) -> int:
    where_query = f"SELECT * FROM sales_data WHERE {field} = ? ALLOW FILTERING"
    prepared = session.prepare(where_query)

    start_time = time.time()
    session.execute(prepared, (value,))
    end_time = time.time()

    return end_time - start_time

def total_sales(name):
    start_time = time.time()
    salesperson_query = "SELECT salespersonkey FROM sales_person WHERE name = ? ALLOW FILTERING"
    salesperson_prepared = session.prepare(salesperson_query)
    salesperson_rows = session.execute(salesperson_prepared, (name,))
    salesperson_key = None

    for row in salesperson_rows:
        salesperson_key = row.salespersonkey

    if salesperson_key is None:
        print("Salesperson not found.")
        return None
    
    sales_count_query = "SELECT COUNT(*) FROM sales_data WHERE salespersonkey = ? ALLOW FILTERING"
    sales_count_prepared = session.prepare(sales_count_query)

    sales_count_rows = session.execute(sales_count_prepared, (salesperson_key,))
    sales_count = sales_count_rows.one()[0]
    end_time = time.time()

    return sales_count, end_time - start_time

def get_all_sales():
    salespersons_query = "SELECT salespersonkey, name FROM sales_person"
    salespersons_prepared = session.prepare(salespersons_query)
    salespersons_rows = session.execute(salespersons_prepared)

    sales_data = {}
    for row in salespersons_rows:
        salesperson_key = row.salespersonkey
        name = row.name

        sales_count_query = "SELECT COUNT(*) FROM sales_data WHERE salespersonkey = ? ALLOW FILTERING"
        sales_count_prepared = session.prepare(sales_count_query)
        sales_count_rows = session.execute(sales_count_prepared, (salesperson_key,))
        sales_count = sales_count_rows.one()[0]

        sales_data[name] = sales_count

    return sales_data

# ez meg csak úgy jól nézett ki eskü
# sales_data = get_all_sales()
# for name, count in sales_data.items():
#     print(f"{name}: {count} sales")

# # 1. rész
# field = "Manager"
# value = "Victor Castro"
# print(f"1.)  measure_query_time() \nField: {field}, Value: {value} \nTime: {measure_query_time(field,value)}\n")

# # 2. rész
# print("2.) total_sales()")
# name = 'Julio Lima'
# count, t = total_sales(name)
# if count:
#     print(f'{name} total sales: {count}')
# else:
#     print(f'{name} no longer works for us')

# print("Time:", t)


