from pymongo import MongoClient
import pandas as pd
from datetime import date
import os


'''add the condition for handling when the folder is already created'''
# Pass directory, participantID, today date, and a list of sensor names.
# Then it will create a bunch of csv files for each senosr name in dir/pid/date.
def mkfile(dir, pid, date, sensors: list):
    adr = f'{str(dir)}/{str(pid)}/{str(date)}'
    os.makedirs(adr, exist_ok=True)
    for sensor in sensors:
        if os.path.exists(f'{adr}/{sensor}.csv'):
            os.remove(f'{adr}/{sensor}.csv')
        with open(f'{adr}/{sensor}.csv', 'x'):
            pass



dir = '.'
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
            # print(sensor_data)
            sensor_name = sensor_data.pop('name')

            # Add the values dictionary as a nested dictionary
            sensor_data.update(sensor_data.pop('values'))
            # print(sensor_data)

            # Convert the dictionary to a DataFrame
            sensor_data = pd.DataFrame.from_dict(sensor_data, orient='index').T
            # print(sensor_data)

            '''add the header for the csv files'''
            # if os.path.getsize(f'{dir}/{pid}/{today}/{sensor_name}.csv') == 0:
            #     # sensor_data.columns.to_series().to_csv(f'{dir}/{pid}/{today}/{sensor_name}.csv', index=False, header=True)
            #     print(type(sensor_data.columns))


            # print(sensor_data)

            # Read the data in csv file
            # with open(f'{dir}/{pid}/{today}/{sensor_name}.csv', 'a') as csv:
            #     csv.write(f'{sensor_data}')
            sensor_data.to_csv(f'{dir}/{pid}/{today}/{sensor_name}.csv', header=False, index=False, mode='a')
            

    