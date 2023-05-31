import pandas as pd
import glob
import os


# If the pid does not exists in the df, it will add it to it
def pid_status(pid, df):
    if not pid in df['Participant'].values:
        # print(f'Adding {pid} to the table.')
        new_row = [pid] + [0] * (df.shape[1] - 1)
        df.loc[len(df)] = new_row
    # else:
    #     print(f'{pid} alredy exists in the table.')
    return df


# Calculate the start day and end day of the week
start_date = pd.to_datetime(input('Enter the start date of the week (e.g. 2023-04-23): ')).date()
end_date = pd.to_datetime(start_date + pd.DateOffset(days=6)).date()

# Create a dataframe for participation tracking
dates = pd.date_range(start=start_date, end=end_date)
participation_tracking = pd.DataFrame(columns=['Participant'] + 
                                              [str(date.date()) + ' Annotation Surveys' for date in dates] +
                                              [str(date.date()) + ' Sensor Uploads' for date in dates] +
                                              ['Total Surveys'] +
                                              ['Total Uploads'] +
                                              ['Self Report Assessments (MHealth)'] +
                                              ['Self Report Assessments (DSQ)'])

'''
    Fill Annotation Surveys columns
'''
# List all Qualtrics surveys
all_surveys = glob.glob('./surveys/*.csv')

# Iterate through each survey results
for survey in all_surveys:

    # Read the .CSV files
    survey_df = pd.read_csv(survey)

    # Preprocess the dataframe
    survey_df = survey_df.drop([0, 1])
    survey_df['StartDate'] = pd.to_datetime(survey_df['StartDate']).dt.date
    
    # Filter dataframe based on the start and end date of the week
    filtered_df = survey_df[(start_date <= survey_df['StartDate']) 
                            & (survey_df['StartDate'] <= end_date)]

    # Get the participant ID from the folder name
    survey = os.path.basename(survey)

    # Iterate the rows through the surveys
    for index, row in filtered_df.iterrows():

        # Iterate morning, evining, or hourly surveys
        if survey.startswith('Tech'):

            # Add participant ID if it is not in the dataframe
            participation_tracking = pid_status(row['Q1'], participation_tracking)

            # Find the row index where the participant ID is equal to row['Q1'] and column index where the date is equal to row['StartDate']
            # Then increase the number of completed survey for the participant on the that day
            row_index = participation_tracking.index[participation_tracking['Participant'] == row['Q1']][0]
            column_index = (row['StartDate'] - start_date).days + 1
            participation_tracking.iloc[row_index, column_index] += 1

        # Iterate MHealth survey
        elif survey.startswith('MHealth'):
            # print(filtered_df.iloc[0, :])

            # Add participant ID if it is not in the dataframe
            participation_tracking = pid_status(row['Q3'], participation_tracking)

            # Find the row index where the participant ID is equal to row['Q3'] and column index of Self Report Assessments (MHealth)
            # Then assign the 'Progress' entries to the cell
            row_index = participation_tracking.index[participation_tracking['Participant'] == row['Q3']][0]
            column_index = 17
            participation_tracking.iloc[row_index, column_index] = int(row['Progress'])
        
        # Iterate Diagnostic survey
        elif survey.startswith('Diagnostic'):

            # Add participant ID if it is not in the dataframe
            participation_tracking = pid_status(row['Q61'], participation_tracking)

            # Find the row index where the participant ID is equal to row['Q61'] and column index of Self Report Assessments (DSQ)
            # Then assign the 'Progress' entries to the cell
            row_index = participation_tracking.index[participation_tracking['Participant'] == row['Q61']][0]
            column_index = 18
            participation_tracking.iloc[row_index, column_index] = int(row['Progress'])


'''
    Fill Sensor Upload columns
'''
# List all Participants folders
all_participants = glob.glob('../P0*')

# Iterate through all participants folder
for participant in all_participants:

    # Get the participant ID from the folder name
    pid = os.path.basename(participant)[:5]

    # Get the name of each .zip folder for participant
    sensor_folder = os.listdir(os.path.join(participant, 'Sensor Data'))
    
    # Iterate all zip files in sensor folder of the participant
    for zip in sensor_folder:

        # Convert folder name to date format
        folder_date = pd.to_datetime(zip[:10]).date()

        # Check wheather folder date is in the week or not
        if 0 <= (folder_date - start_date).days < 7:
            # Add participant ID if it is not in the dataframe
            participation_tracking = pid_status(pid, participation_tracking)
            
            # Find the row index where the participant ID is equal to pid and column index where the date is equal to folder_date
            # Then increase the number of completed survey for the participant on the that day
            row_index = participation_tracking.index[participation_tracking['Participant'] == pid][0]
            column_index = (folder_date - start_date).days + 8
            participation_tracking.iloc[row_index, column_index] += 1


''' 
    Fill Total Surveys and Total Uploads columns
'''   
# Calculate the sum of all surveys for a week
participation_tracking['Total Surveys'] = participation_tracking.iloc[:, 1:8].sum(axis=1)

# Calculate the sum of all uploads for a week
participation_tracking['Total Uploads'] = participation_tracking.iloc[:, 8:15].sum(axis=1)


'''
    Save the Results
'''
# Save the result in a csv file
if not os.path.exists(f'./participation_tracking'):
    os.mkdir(f'./participation_tracking')
participation_tracking.to_csv(f'./participation_tracking/{start_date}_to_{end_date}.csv')

