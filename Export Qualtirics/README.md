Copy the code in a folder based on the data structure of folder below:

    Project Root
    ├── Participant A
    │   ├── Subfolder A1
    │   │   ├── File A1.1
    │   │   └── File A1.2
    │   └── Data Sensor
    │       ├── Data_1.zip
    │       └── Data_2.zip
    ├── Participant B
    │   ├── Subfolder B1
    │   │   ├── File B1.1
    │   │   └── File B1.2
    │   └── Data Sensor
    │       ├── 20**-**-**.zip
    │       └── 20**-**-**.zip
    └── Export Qualtircs
        ├── Qualtrics Surveys
        │   ├── Survey_1.csv
        │   └── Survey_2.csv
        ├── Participation Tracking
        │   ├── Week_1.csv
        │   └── Week_2.csv
        └── main.py

This code will save the number of updated sensor data and completed qualtircs survey in CSV format during a week.
Save the exported qualtircs in the same directory as the code in a subfolder called "surveys".
Run "main.py" and then enter the first day of the desired week to filtered the captured data. The results will save in participation_tracking folder.

Important:
The name of sensor data (zipped file) has to include a date with "20**-\**-**" format.