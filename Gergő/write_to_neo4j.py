import time
from neo4j import GraphDatabase
import json

with open('transformed_data.json') as f:
    data = json.load(f)

BATCH_SIZE = 10000

def create_test_data(batch_key, batch_data):
    uri = "bolt://localhost:7687"  
    username = "neo4j"  
    password = "password"
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        query = """
            UNWIND $keys AS key
            WITH key, $data[key] AS row
            MERGE (sp:Salesperson {name: row.salesperson})
            MERGE (sv: Supervisor {name: row.supervisor})
            MERGE (m: Manager {name: row.manager})
            MERGE (sv)-[:Supervisor]->(sp)
            MERGE (m)-[:Manager]->(sv)
            MERGE (m)-[:Manager]->(sp)
            MERGE (o:Order {number: key})
            SET o.channel = row.channel, o.order_date = row.order_date
            MERGE (sp)-[:PLACED]->(o)
            FOREACH (product IN row.products |
            MERGE (p:Product {key: product.product_key})
            MERGE (o)-[:CONTAINS]->(p)
            SET o.quantity = product.quantity, o.unit_price = product.unit_price
            )
            RETURN sp.name
            """
        session.run(query, keys=batch_key, data=batch_data)


if __name__ == '__main__':
    keys = list(data.keys())  
    full_batches = len(keys) // BATCH_SIZE
    batches = [keys[i * BATCH_SIZE:(i + 1) * BATCH_SIZE] for i in range(full_batches)]

    if len(keys) % BATCH_SIZE != 0:
        batches.append(keys[full_batches * BATCH_SIZE:])

    times = []

    for batch_keys in batches:
        batch_data = {key: data[key] for key in batch_keys}
        batch_key = list(batch_data.keys())
        start = time.time()
        create_test_data(batch_key, batch_data)
        end = time.time()
        times.append(end - start)
    
    print("Time taken to write to Neo4j: ", sum(times), " seconds.")
