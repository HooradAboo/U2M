from pymongo import MongoClient
import pandas as pd
from datetime import date

today = str(date.today())


client = MongoClient(
    "mongodb+srv://hoorad:h8rad@cluster0.qm6fhqa.mongodb.net/?retryWrites=true&w=majority")
db = client["U2M"]
collection = db["sensor"]

df = pd.DataFrame(list(collection.find({"date": today})))

# Save today's log in csv format
df.to_csv(f'U2M-{today}.csv')
