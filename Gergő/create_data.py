from random import randint
import json

class User:
    def __init__(self, name, email, age):
        self.Name = name
        self.Email = email
        self.Age = age

# Felhasználók generálása
users = []
for i in range(10000):
    user = User(name=f"User{i}", email=f"user{i}@example.com", age=randint(18, 80))
    users.append(user)

names = [each.Name for each in users]
emails = [each.Email for each in users]
ages = [each.Age for each in users]


data = {"names": names, "emails": emails, "ages": ages}
#write out data
with open("data.json", "w") as f:
    json.dump(data, f)


