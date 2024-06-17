from cassandra.cluster import Cluster
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from cassandra_db import df, write_cassandra

cluster = Cluster(['localhost'], port=9042) 
session = cluster.connect()
session.set_keyspace('mykeyspace')

def measure_write_and_delete_times():
    times = []
    delete_times = []

    for _ in range(10):
        # ÍRÁS
        times.append(write_cassandra(df, 1000))

        #TÖRLÉS
        delete_start = time.time()

        session.execute("TRUNCATE sales_data")
        session.execute("TRUNCATE sales_person")

        delete_end = time.time()
        delete_times.append(delete_end - delete_start)


    avg_write_time = np.mean(times)
    max_write_time = max(times)
    min_write_time = min(times)

    avg_delete_time = np.mean(delete_times)
    max_delete_time = max(delete_times)
    min_delete_time = min(delete_times)
    
    return [avg_write_time, max_write_time, min_write_time], [avg_delete_time, max_delete_time, min_delete_time]    

def plots(time_list_write, time_list_delete):
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

    plt.tight_layout()
    plt.show()


time_list_write, time_list_delete = measure_write_and_delete_times()
plots(time_list_write, time_list_delete)