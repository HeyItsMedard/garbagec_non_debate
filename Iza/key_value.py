import json
from pymongo import MongoClient
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

with open("data.json", "r") as f:
    data = json.load(f)

users_list = []
user_dict={}
user_dict = {}
for i in range(10000):
    user_dict[str(data["ids"][i])] = {"_id": data["ids"][i], "name": data["names"][i], "email": data["emails"][i], "age": data["ages"][i]}

uri = "mongodb+srv://skribaizabella:qByd1uBlOIrcvXIC@probacluster.ukmitfl.mongodb.net/?retryWrites=true&w=majority"
database_name = "uj_adatbázis_proba"
collection_name ="uj_collection_proba"

client = MongoClient(uri)

db = client[database_name]
collection = db[collection_name]

def write_to_mongodb(users_dict):
    times = []
    delete_times = []
    for _ in range(10):
        delete_start = time.time()
        db[collection_name].delete_many({})
        delete_end = time.time()
        delete_times.append(delete_end - delete_start)
        
        start = time.time()
        db[collection_name].insert_one(users_dict)
        end = time.time()
        times.append(end - start)
    
    avg_write_time = np.mean(times)
    max_write_time = max(times)
    min_write_time = min(times)

    avg_delete_time = np.mean(delete_times)
    max_delete_time = max(delete_times)
    min_delete_time = min(delete_times)
    
    return [avg_write_time, max_write_time, min_write_time], [avg_delete_time, max_delete_time, min_delete_time]

def do_query():
    times = []
    for _ in range(10):
        start = time.time()
        result = list(collection.find({}, {"_id": 0, "name": 1, "email": 1, "age": 1}))
        end = time.time()
        times.append(end - start)

    avg_query_time = np.mean(times)
    max_query_time = max(times)
    min_query_time = min(times)
    
    df = pd.DataFrame(result, columns=["Name", "Email", "Age"])
    
    return df, [avg_query_time, max_query_time, min_query_time]

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


time_list_write, time_list_delete = write_to_mongodb(user_dict)

result_df, time_list_query = do_query()
plots(time_list_write, time_list_delete, time_list_query)
