from cassandra.cluster import Cluster
from prettytable import PrettyTable
import json
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

## pip install docker
## >>> docker run --name cassandra-container -p 9042:9042 -d cassandra:latest

with open("data.json", "r") as f:
    data = json.load(f)

users_list = []
for i in range(5000):
    user = {"id": i, "name": data["names"][i], "email": data["emails"][i], "age": data["ages"][i]}
    users_list.append(user)

cluster = Cluster(['localhost'], port=9042) 
session = cluster.connect() 

session.execute("CREATE KEYSPACE IF NOT EXISTS mykeyspace WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}")
session.execute("USE mykeyspace")
session.execute("DROP TABLE IF EXISTS user_profiles")
session.execute("CREATE TABLE IF NOT EXISTS user_profiles (id INT PRIMARY KEY, name TEXT, email TEXT, age INT)")

def write_to_cassandra():
    times = []
    delete_times = []
    for _ in range(10):

        start = time.time()

        # hozzáadás
        insert_query = session.prepare("INSERT INTO user_profiles (id, name, email, age) VALUES (?, ?, ?, ?)")
        for user in users_list:
            session.execute(insert_query, (user["id"], user['name'], user['email'], user['age']))
        
        end = time.time()
        times.append(end - start)
        print('\nVége a hozzáadásnak\n')

        delete_start = time.time()

        # törlés
        session.execute("TRUNCATE user_profiles")
        
        delete_end = time.time()
        delete_times.append(delete_end - delete_start)
        print('\nVége a törlésnek\n')


    avg_write_time = np.mean(times)
    max_write_time = max(times)
    min_write_time = min(times)

    avg_delete_time = np.mean(delete_times)
    max_delete_time = max(delete_times)
    min_delete_time = min(delete_times)
    
    return [avg_write_time, max_write_time, min_write_time], [avg_delete_time, max_delete_time, min_delete_time]    

def plots(time_list_write, time_list_delete, time_list_query):
    x = ["Mean", "Max", "Min"]

    plt.subplot(1, 3, 1)
    plt.bar(x, time_list_write, color="blue", alpha=0.5, label="Write")
    plt.title("Write")
    plt.xlabel("Time")
    plt.ylabel("Duration")

    plt.subplot(1, 3, 2)
    plt.bar(x, time_list_delete, color="red", alpha=0.5, label="Delete")
    plt.title("Delete")
    plt.xlabel("Time")
    plt.ylabel("Duration")

    plt.subplot(1, 3, 3)
    plt.bar(x, time_list_query, color="green", alpha=0.5, label="Query")
    plt.title("Query")
    plt.xlabel("Time")
    plt.ylabel("Duration")

    plt.tight_layout()
    plt.show()

def do_query():
    insert_query = session.prepare("INSERT INTO user_profiles (id, name, email, age) VALUES (?, ?, ?, ?)")
    for user in users_list:
        session.execute(insert_query, (user['id'], user['name'], user['email'], user['age']))

    times = []
    for _ in range(10):
        start = time.time()
        result = session.execute("SELECT * FROM user_profiles")
        end = time.time()
        times.append(end - start)

    avg_query_time = np.mean(times)
    max_query_time = max(times)
    min_query_time = min(times)
    
    df = pd.DataFrame(result, columns=result.column_names)
    df.drop(columns=["id"], inplace=True)

    table = PrettyTable()
    table.field_names = df.columns
    for row in df.itertuples(index=False):
        table.add_row(row)
    print(table)


    
    return df, [avg_query_time, max_query_time, min_query_time]


time_list_write, time_list_delete = write_to_cassandra()

result_df, time_list_query = do_query()
plots(time_list_write, time_list_delete, time_list_query)