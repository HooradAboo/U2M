from pymongo import MongoClient
import pandas as pd
from datetime import date
import os


def mkfile(dir, pid, date, sensors: list):
    adr = f'{dir}/{pid}/{date}'
    os.makedirs(adr)
    for sensor in sensors:
        f = open(f'{adr}/{sensor}.csv', 'x')



dir = './'
today = str(date.today())

client = MongoClient(
    'mongodb+srv://hoorad:h8rad@cluster0.qm6fhqa.mongodb.net/?retryWrites=true&w=majority')
db = client['U2M']
collection = db['sensor']

today_df = pd.DataFrame(list(collection.find({'date': today})))

# Get the list of today's participant
pids = set(today_df['participantId'])

for pid in pids:
    payloads = today_df.loc[today_df['participantId'] == pid, 'payload']

    # Get the name of all sensor names for an specific participant with ID=pid
    sensor_names = sorted({d['name'] for packet in payloads for d in packet})

    # Create bunch of .csv files for each sensor in dir/pid/date
    mkfile(dir, pid, today, sensor_names)

    # Get the content of each recieved packet for participantId = pid
    # A packet is a list of the data from all sensors in one single message
    for packet in payloads:
        # print(packet)
        for sensor_data in packet:
            sensor_name = sensor_data['name']
            with open(f'{dir}/{pid}/{today}/{sensor_name}.csv', 'a') as csv:
                csv.write(f'{sensor_data}')
            # print(sensor_data)

    # print(df['participantId'])

    '''remove the list from the payload and create a .csv for each sensor'''

    # Save today's log in csv format for each participant
    # df.to_csv(f'U2M-{today}-{pid}.csv')
