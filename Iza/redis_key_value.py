import redis
import pandas as pd
import json
import time

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_client.flushdb()

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

    def to_redis_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != 'Salesperson'}


class SalespersonData:
    def __init__(self, salesperson_key, salesperson):
        self.SalespersonKey = salesperson_key
        self.Salesperson = salesperson

    def to_redis_dict(self):
        return self.__dict__


df = pd.read_excel('SalesData.xlsx')

sales_count = 0

for index, row in df.iterrows():
    unit_price = row['UnitPrice']
    if isinstance(unit_price, str):
        unit_price = float(unit_price.replace('$', ''))
        
    sales_data = SalesData(
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
    redis_client.set(f"Sales_original{index}", json.dumps(sales_data.__dict__))

    redis_client.set(f"sales:{index}", json.dumps(sales_data.to_redis_dict()))
    
    sales_count += row['Quantity']

    salesperson_data = SalespersonData(
        salesperson_key=row['SalespersonKey'],
        salesperson=row['Salesperson']
    )
    redis_client.set(f"salesperson:{salesperson_data.SalespersonKey}", json.dumps(salesperson_data.to_redis_dict()))



start_time = time.time()
keys = redis_client.keys('Sales_original*')
results = []
for key in keys:
    doc = json.loads(redis_client.get(key))
    if "Salesperson" in doc and doc["Salesperson"] == "Julio Lima":
        results.append(doc)
end_time = time.time()


# 1. WHERE feltétel jellegű keresések
print(f"WHERE feltétel keresés (Salesperson = Julio Lima) ideje: {end_time-start_time:.4f} másodperc, találatok száma: {len(results)}")


#2. Táblák kapcsolása,
# Keresés Julio Lima eladásai között
julio_salesperson_key = None

# Keresés SalespersonData táblában Julio Lima alapján
start_time = time.time()
keys = redis_client.keys('salesperson:*')
for key in keys:
    data = json.loads(redis_client.get(key))
    if data['Salesperson'] == 'Julio Lima':
        julio_salesperson_key = data['SalespersonKey']

if julio_salesperson_key:
    total_sales = 0
 
    keys = redis_client.keys('sales:*')
    for key in keys:
        data = json.loads(redis_client.get(key))
        if data['SalespersonKey'] == julio_salesperson_key:
            total_sales += data['Quantity']
    end_time=time.time()
    print(f"Julio Lima összesen {total_sales} darabot értékesített. ideje: {end_time-start_time:.4f} másodperc")
else:
    print(f"Julio Lima nem található a SalespersonData táblában.")


