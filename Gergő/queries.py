from neo4j import GraphDatabase
import time

URI = "bolt://localhost:7687"  
USERNAME = "neo4j"  
PASSWORD = "password"

def create_connection(uri, username, password):
    return GraphDatabase.driver(uri, auth=(username, password))

def delete_query():
    driver = create_connection(URI, USERNAME, PASSWORD)
    start = time.time()
    with driver.session() as session:
        query = """
        MATCH (n)-[r]-()
        DELETE r
        DELETE n
        """
        session.run(query)

    driver.close()
    end = time.time()
    print("Time taken to delete all nodes and relationships: ", end - start, " seconds.")

def where_kind_query():
    driver = create_connection(URI, USERNAME, PASSWORD)
    start = time.time()
    with driver.session() as session:
        query = """
        MATCH (n:Salesperson)
        WHERE n.name = $name
        RETURN n
        """
        result = session.run(query, name="Julio Lima")
        for record in result:
            print(record['n']['name'])

    end = time.time()
    driver.close()
    print("Time taken to run WHERE query: ", end - start, " seconds.")

def relation_query():
    driver = create_connection(URI, USERNAME, PASSWORD)
    start = time.time()
    with driver.session() as session:
        query = """
        MATCH (m:Manager)-[:Manager]->(s:Supervisor)-[:Supervisor]->(sp:Salesperson)
        RETURN m, s, sp
        """
        result = session.run(query)
        for record in result:
            print(f"Manager: {record['m']['name']}")
            print(f"  Supervisor: {record['s']['name']}")
            print(f"    Salesperson: {record['sp']['name']}\n")
    driver.close()
    end = time.time()

    print("Time taken to run relation query: ", end - start, " seconds.")


"""
A gráf adatbázisban nem kulcsokat használtam, hanem a salesperson, ordernumber, manager és a supervisor lett mind egy csúcs. 
Minden OrderNumber is egy csúcs, a duplikálást elkerülve. 
Ezen csúcsok között vannak a realációk, amelyek így néznek ki:
OrderNumber -CONTAINS-> Product (Azaz egy megrendelés tartalmaz egy vagy több Productot)
Salesperson -PLACED-> OrderNumber (Azaz egy Salesperson kezdeményezett el egy megrendelést)
Manager -Manager-> Salesperson (Azaz egy Manager felügyel egy Salespersonra)
Manager -Manager-> Supervisor (Azaz egy Manager felügyel egy Supervisorra)
Supervisor -Supervisor-> Salesperson (Azaz egy Supervisor felügyel egy Salespersonra)
"""

if __name__ == "__main__":
    where_kind_query()
    relation_query()
    delete_query()