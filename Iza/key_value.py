import json
import redis
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt


with open("data.json", "r") as f:
    data = json.load(f)


users_list = []
for i in range(10000):
    user = {"id": data["ids"][i], "name": data["names"][i], "email": data["emails"][i], "age": data["ages"][i]}
    users_list.append(user)


redis_host = 'localhost'
redis_port = 6379
client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def write_to_redis(users_list):
    times = []
    delete_times = []
    for _ in range(10):
        
        delete_start = time.time()
        client.flushdb()  
        delete_end = time.time()
        delete_times.append(delete_end - delete_start)
        
        
        start = time.time()
        for user in users_list:
            client.set(user['id'], json.dumps(user))  
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
    result = []
    for _ in range(10):
        start = time.time()
        
        keys = client.keys("*")
        users = [json.loads(client.get(key)) for key in keys]
        result = users
      
        end = time.time()
        times.append(end - start)
    
    avg_query_time = np.mean(times)
    max_query_time = max(times)
    min_query_time = min(times)
    
    df = pd.DataFrame(result, columns=["name", "email", "age"])
    
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

time_list_write, time_list_delete = write_to_redis(users_list)
result_df, time_list_query = do_query()
plots(time_list_write, time_list_delete, time_list_query)