import glob
import os
import datetime
import pandas as pd
from utility import pid_status


# Calculate the start day and end day of the week
start_date = pd.to_datetime(datetime.date(2023, 4, 23)).date()
end_date = pd.to_datetime(start_date + pd.DateOffset(days=6)).date()
# print(type(start_date), type(end_date))

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
    Fill Annotations and Self Report Assassments columns.
'''
# List all Qualtrics surveys
all_surveys = glob.glob('*.csv')
# print(all_surveys)

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
    # print(filtered_df)

    # Iterate the rows through the surveys
    for index, row in filtered_df.iterrows():

        # Iterate morning, evining, or hourly surveys
        if survey.startswith('Tech'):

            # Add participant ID if it is not in the dataframe
            participation_tracking = pid_status(row['Q1'], participation_tracking)

            # Find the row index where the participant ID is equal to row['Q1'] and col index where the date is equal to row['StartDate']
            # Then increase the number of completed survey for the participant on the that day
            row_index = participation_tracking.index[participation_tracking['Participant'] == row['Q1']][0]
            column_index = (row['StartDate'] - start_date).days + 1
            participation_tracking.iloc[row_index, column_index] += 1

        # Iterate MHealth survey
        elif survey.startswith('MHealth'):
            # print(filtered_df.iloc[0, :])

            # Add participant ID if it is not in the dataframe
            participation_tracking = pid_status(row['Q3'], participation_tracking)

            # Find the row index where the participant ID is equal to row['Q3'] and col index of Self Report Assessments (MHealth)
            # Then assign the 'Progress' entries to the cell
            row_index = participation_tracking.index[participation_tracking['Participant'] == row['Q3']][0]
            column_index = 17
            participation_tracking.iloc[row_index, column_index] = int(row['Progress'])
        
        # Iterate Diagnostic survey
        elif survey.startswith('Diagnostic'):

            # Add participant ID if it is not in the dataframe
            participation_tracking = pid_status(row['Q61'], participation_tracking)

            # Find the row index where the participant ID is equal to row['Q61'] and col index of Self Report Assessments (DSQ)
            # Then assign the 'Progress' entries to the cell
            row_index = participation_tracking.index[participation_tracking['Participant'] == row['Q61']][0]
            column_index = 18
            participation_tracking.iloc[row_index, column_index] = int(row['Progress'])

# Calculate the sum of all surveys for a week
participation_tracking['Total Surveys'] = participation_tracking.iloc[:, 1:8].sum(axis=1)

# pd.set_option('display.max_columns', None)
print(participation_tracking)

