import time
import matplotlib.pyplot as plt
import numpy as np
from pyravendb.store import document_store

# RavenDB initialization
store = document_store.DocumentStore(urls=['http://127.0.0.1:50993'], database='TestDatabase')
store.initialize()

class User:
    def __init__(self, name, email, age):
        self.Id = None
        self.Name = name
        self.Email = email
        self.Age = age

def run_operations():
    write_times = []
    read_times = []
    delete_times = []

    for _ in range(10):
        # Generating users
        users = [User(name="User" + str(i), email="user{}@example.com".format(i), age=30) for i in range(10000)]

        # Writing time measurement
        start_time = time.time()
        with store.open_session() as session:
            for user in users:
                session.store(user)
            session.save_changes()
        write_time = time.time() - start_time
        write_times.append(write_time)

        # Reading time measurement
        start_time = time.time()
        with store.open_session() as session:
            fetched_users = list(session.query(User))
        read_time = time.time() - start_time
        read_times.append(read_time)

        # Deleting time measurement
        start_time = time.time()
        with store.open_session() as session:
            for user in fetched_users:
                session.delete(user.Id)
            session.save_changes()
        delete_time = time.time() - start_time
        delete_times.append(delete_time)

    return write_times, read_times, delete_times

# Running the operations
write_times, read_times, delete_times = run_operations()

# Determining best, average, and worst times
best_write_time = min(write_times)
average_write_time = sum(write_times) / len(write_times)
worst_write_time = max(write_times)

best_read_time = min(read_times)
average_read_time = sum(read_times) / len(read_times)
worst_read_time = max(read_times)

best_delete_time = min(delete_times)
average_delete_time = sum(delete_times) / len(delete_times)
worst_delete_time = max(delete_times)

# Displaying the results
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

# Writing time
axes[0].bar(["Best", "Average", "Worst"], [best_write_time, average_write_time, worst_write_time], color='blue')
axes[0].set_title('Writing Time')
for i, v in enumerate([best_write_time, average_write_time, worst_write_time]):
    axes[0].text(i, v, "{:.4f} s".format(v), ha='center', va='bottom')

# Reading time
axes[1].bar(["Best", "Average", "Worst"], [best_read_time, average_read_time, worst_read_time], color='orange')
axes[1].set_title('Reading Time')
for i, v in enumerate([best_read_time, average_read_time, worst_read_time]):
    axes[1].text(i, v, "{:.4f} s".format(v), ha='center', va='bottom')

# Deleting time
axes[2].bar(["Best", "Average", "Worst"], [best_delete_time, average_delete_time, worst_delete_time], color='green')
axes[2].set_title('Deleting Time')
for i, v in enumerate([best_delete_time, average_delete_time, worst_delete_time]):
    axes[2].text(i, v, "{:.4f} s".format(v), ha='center', va='bottom')

plt.suptitle('10x10000 Objects', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Adjusting spacing between plots
plt.subplots_adjust(hspace=0.5)

# Exporting to PNG
plt.savefig('ravendb_performance.png')

plt.show()
