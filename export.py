from pymongo import MongoClient
import pandas as pd
from datetime import date

today = str(date.today())


client = MongoClient(
    "mongodb+srv://hoorad:h8rad@cluster0.qm6fhqa.mongodb.net/?retryWrites=true&w=majority")
db = client["U2M"]
collection = db["sensor"]

today_df = pd.DataFrame(list(collection.find({"date": today})))

# Get the list of today's participant
pids = set(today_df["participantId"])
# print(pids)

for pid in pids:
    df = today_df[today_df.participantId == pid]
    # print(df["participantId"])

    # Save today's log in csv format for each participant
    df.to_csv(f'U2M-{today}-{pid}.csv')
