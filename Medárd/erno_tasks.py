from pyravendb.store import document_store
import time

# RavenDB inicializálása
store = document_store.DocumentStore(urls=['http://127.0.0.1:58712'], database='TestDatabase')
store.initialize()

# SalesData osztály definíciója (ugyanaz, mint az előző scriptben)
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

def measure_query_time(field, value):
    start_time = time.time()
    with store.open_session() as session:
        results = list(session.query(object_type=SalesData).where_equals(field, value))
    end_time = time.time()
    return end_time - start_time, len(results)

# 1. WHERE feltétel jellegű keresések
field = "Salesperson"
value = "Julio Lima"
time_taken, result_count = measure_query_time(field, value)
print(f"WHERE feltétel keresés ({field} = '{value}') ideje: {time_taken:.4f} másodperc, találatok száma: {result_count}")

# 2. Táblák kapcsolása, referencia táblában keresés (RavenDB nem támogat ilyen jellegű relációkat natív módon)
# Megvizsgálhatjuk azonban, hogy egy adott kulcs alapján történő keresés mennyi időt vesz igénybe

# field = "ProductKey"
# value = 1420
# time_taken, result_count = measure_query_time(field, value)
# print(f"Referencia táblában keresés ({field} = '{value}') ideje: {time_taken:.4f} másodperc, találatok száma: {result_count}")
