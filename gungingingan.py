import time
from pyravendb.store import document_store

# MINDEN ALKALOMMAL ÁT KELL ÍRNI A PORTOT, MERT RANDOM GENERÁLJA
# Path: D:\External Drive Folders\de\RavenDB-6.0.102-windows-x64\Server\Raven.Server.exe
# RavenDB inicializálása
store = document_store.DocumentStore(urls=['http://127.0.0.1:51396'], database='TestDatabase')
store.initialize()

class User:
    def __init__(self, name, email, age):
        self.Id = None
        self.Name = name
        self.Email = email
        self.Age = age

# Felhasználók generálása
users = []
for i in range(10000):
    user = User(name="User" + str(i), email="user{}@example.com".format(i), age=30)
    users.append(user)

# Az írási idő mérésének kezdete
start_time = time.time()

# Felhasználók mentése az adatbázisba
with store.open_session() as session:
    for user in users:
        session.store(user)
    session.save_changes()

# Az írási idő mérésének vége
write_time = time.time() - start_time
print("Írás ideje:", write_time)

# Az olvasási idő mérésének kezdete
start_time = time.time()

# Felhasználók kiolvasása az adatbázisból
with store.open_session() as session:
    fetched_users = list(session.query(User))

# Az olvasási idő mérésének vége
read_time = time.time() - start_time
print("Olvasás ideje:", read_time)

# A törlési idő mérésének kezdete
start_time = time.time()

# Felhasználók törlése az adatbázisból
with store.open_session() as session:
    for user in fetched_users:
        session.delete(user.Id)  
    session.save_changes()
    
# A törlési idő mérésének vége
delete_time = time.time() - start_time
print("Törlés ideje:", delete_time)
