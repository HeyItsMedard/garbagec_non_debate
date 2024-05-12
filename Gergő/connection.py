import json
from neo4j import GraphDatabase
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

with open("data.json", "r") as f:
    data = json.load(f)

users_list = []
for i in range(10000):
    user = {"name": data["names"][i], "email": data["emails"][i], "age": data["ages"][i], "id": data["ids"][i]}
    users_list.append(user)

def write_to_neo4j(users_list):
    times = []
    database_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "comparegraph"))
    session = database_connection.session()
    query = """
    UNWIND $users as user
    CREATE (u:User {name: user.name})
    CREATE (e:Email {address: user.email})
    CREATE (a:Age {value: user.age})
    CREATE (i:Id {value: user.id})
    CREATE (u)-[:ID]->(i)
    CREATE (u)-[:EMAIL]->(e)
    CREATE (u)-[:AGE]->(a)
    """
    time_list = []
    delete_list = []
    delete_time = []
    delete_query = """
    MATCH (n)
    DETACH DELETE n
    """ 
    for _ in range(10):
        del_start = time.time()
        session.run(delete_query)
        del_end = time.time()
        start = time.time()
        session.run(query, users=users_list)
        end = time.time()
        times.append(end-start)
        delete_list.append(del_end-del_start)
    session.close()

    time_list.append(np.mean(times))
    time_list.append(max(times))
    time_list.append(min(times))

    delete_time.append(np.mean(delete_list))
    delete_time.append(max(delete_list))
    delete_time.append(min(delete_list))
    return time_list, delete_time

def do_query():
    database_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "comparegraph"))
    session = database_connection.session()
    times = []
    query = """
    MATCH (u:User)-[:EMAIL]->(e:Email), (u)-[:AGE]->(a:Age), (u)-[:ID]->(i:Id)
    RETURN u.name AS Name, e.address AS Email, a.value AS Age, i.value AS Id
    """
    time_list = []
    for _ in range(10):
        start = time.time()
        result = session.run(query)
        end = time.time()
        times.append(end-start)
    time_list.append(np.mean(times))
    time_list.append(max(times))
    time_list.append(min(times))

    data = []
    for record in result:
        data.append((record["Name"], record["Email"], record["Age"], record["Id"]))
    
    session.close()
    
    df = pd.DataFrame(data, columns=["Name", "Email", "Age", "Id"])
    return df, time_list

def plots(time_list_write, time_list_delete, time_list_query):
    x = ["Mean", "Max", "Min"]
    #Writing time
    plt.subplot(1, 3, 1)
    plt.bar(x, time_list_write, color="blue", alpha=0.5, label="Write")
    plt.title("Write")
    plt.xlabel("Time")
    plt.ylabel("Duration")
    #Deleting time
    plt.subplot(1, 3, 2)
    plt.bar(x, time_list_delete, color="red", alpha=0.5, label="Delete")
    plt.title("Delete")
    plt.xlabel("Time")
    plt.ylabel("Duration")
    #Query time
    plt.subplot(1, 3, 3)
    plt.bar(x, time_list_query, color="green", alpha=0.5, label="Query")
    plt.title("Query")
    plt.xlabel("Time")
    plt.ylabel("Duration")

    plt.tight_layout()
    plt.show()

time_list_write, time_list_delete = write_to_neo4j(users_list)
result_df, time_list_query = do_query()
plots(time_list_write, time_list_delete, time_list_query)


