import time
from pymongo import MongoClient
import couchdb
from pyravendb.store import document_store
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_user():
    user = {
        "id": generate_random_string(10),
        "name": generate_random_string(8).capitalize(),
        "email": generate_random_string(6) + "@example.com",
        "age": random.randint(18, 65),
        "country": random.choice(["USA", "UK", "Canada", "Germany", "France"]),
        # Tetszőlegesen további tulajdonságok
    }
    return user

# Generáljunk például 100 felhasználót
documents = [generate_user() for _ in range(100)]

# # MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client.test_database
# collection = db.test_collection

# start_time = time.time()
# # MongoDB írás
# for document in documents:
#     collection.insert_one(document)
# write_time_mongodb = time.time() - start_time

# start_time = time.time()
# # MongoDB olvasás
# for document in collection.find():
#     pass
# read_time_mongodb = time.time() - start_time

# print("MongoDB írás ideje:", write_time_mongodb)
# print("MongoDB olvasás ideje:", read_time_mongodb)

# # CouchDB
# couch = couchdb.Server()
# db = couch['test_database']

# start_time = time.time()
# # CouchDB írás
# for document in documents:
#     db.save(document)
# write_time_couchdb = time.time() - start_time

# start_time = time.time()
# # CouchDB olvasás
# for document_id in db:
#     doc = db[document_id]
# read_time_couchdb = time.time() - start_time
# print("CouchDB írás ideje:", write_time_couchdb)
# print("CouchDB olvasás ideje:", read_time_couchdb)

# RavenDB
store = document_store.DocumentStore(urls=['http://127.0.0.1:51396'], database='TestDatabase')
store.initialize()

session = store.open_session()

start_time = time.time()
# RavenDB írás
for document in documents:
    session.store(document)
session.save_changes()
write_time_ravendb = time.time() - start_time

start_time = time.time()
# RavenDB olvasás
results = session.query(object).all()
read_time_ravendb = time.time() - start_time

print("RavenDB írás ideje:", write_time_ravendb)
print("RavenDB olvasás ideje:", read_time_ravendb)
