#!/usr/bin/python
# -*- coding: utf-8 -*-
from zipfile import ZipFile, BadZipFile
import os
import shutil
import filecmp


# ANSI escape sequences for text colors
RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"


# List all directories in CBT Smartphone Sensing Study/

all_directories = os.listdir('..')

# iterate through each folder in CBT Smartphone Sensing Study/

for each_directory in all_directories:

    # if each_directory's name contains P0 and Group, then it is a
    # participant's folder

    if 'P0' and 'Group' in each_directory:

        # Create directory to store all sensor data without mic data
        os.makedirs(os.path.join('..', each_directory, 'Sensor Data - backup'), exist_ok=True)

        print (GREEN + 'Checking %s for .MP4 data' % each_directory + RESET)

        # Open Sensor Data folder in participant's directory

        sensor_folder = os.path.join('..', each_directory, 'Sensor Data')
        # print('Make a copy of Sensor Data folder...')
        # shutil.copytree(sensor_folder, os.path.join('..', each_directory, 'Sensor Data - backup'))
        sensor_folder = os.listdir(sensor_folder)

        # Iterate through each zipped folder in the Sensor Data folder

        for zippedFile in sensor_folder:
            print ('\tChecking %s for .MP4 data' % zippedFile)

            # Create directory to store sensor data without mic data

            os.mkdir('new_archive')

            # Create directory to store a backup

            os.mkdir('backup')

            # Unzip each sensor data folder upload
            try:
                with ZipFile(os.path.join('..', each_directory,
                            'Sensor Data', zippedFile), 'r') as archive:

                    # if mic data is there (i.e., it hasn't been deleted yet)

                    if 'Microphone.mp4' in archive.namelist():

                        print ('\t\tFound .MP4 data in %s.\n\t\tFolder size pre-deletion: %d' \
                            % (zippedFile, os.path.getsize(os.path.join('..'
                            , each_directory, 'Sensor Data', zippedFile,
                            ))))
                        
                        shutil.copy2(os.path.join('..', each_directory, 'Sensor Data', zippedFile), 
                            os.path.join('..', each_directory, 'Sensor Data - backup', zippedFile))

                        # extract the folder and place it in new_archive

                        archive.extractall('new_archive')

                        # extract the folder and place it in backup

                        archive.extractall('backup')

                        # remove mic data from new_archive

                        print ('\t\tRemoving .MP4 data')
                        os.remove('new_archive/Microphone.mp4')

                        # make sure nothing else was changed in the process of
                        # deleting mic data

                        print ('\t\tValidity check...')
                        saveFlag = True
                        same = True

                        # for each file in the old archive

                        for filename in archive.namelist():  # skip over mic data as it should only exist in the old archive
                            if filename == 'Microphone.mp4':
                                continue
                            else:

                                # check that the file in new_archive and backup are the same

                                f1 = os.path.join('backup', filename)
                                f2 = os.path.join('new_archive', filename)
                                same = filecmp.cmp(f1, f2, shallow=False)

                                # this will print that something happened
                                # that changed one of the data files
                                # during the process of deleting the mic data

                                if same == False:
                                    print ('\t\tValidity check failed.')
                                    print ('\t\tFile altered: %s vs %s' \
                                        % (f1, f2))
                                    print ('\t\tNo .MP4 data deleted')
                                    saveFlag = False

                        # as long as all other files remained intact, save new_archive

                        if saveFlag:
                            print ("\t\tValidity check passed. Updating participant's zipped folder.")

                            # shutil.rmtree(os.path.join("..", each_directory, "Sensor Data", zippedFile))

                            shutil.make_archive('../' + each_directory
                                    + '/Sensor Data - backup/'
                                    + zippedFile.replace('.zip', ''),
                                    format='zip', root_dir='new_archive')
                            print ('\t\tMicrophone.MP4 deleted from %s/%s' \
                                % (each_directory, zippedFile))
                            print ('\t\tFolder size post-deletion: %d' \
                                % os.path.getsize(os.path.join('..',
                                    each_directory, 'Sensor Data - backup',
                                    zippedFile)))
                    else:
                        print ('\t\tMicrophone.MP4 already deleted from %s/%s/%s' \
                            % (each_directory, 'Sensor Data', zippedFile))
                        # shutil.copy2(os.path.join('..', each_directory, 'Sensor Data', zippedFile), 
                        #      os.path.join('..', each_directory, 'Sensor Data - No Mic', zippedFile))
            except BadZipFile:
                print(RED + "\t\tThe zip file is invalid or corrupted." + RESET)

            shutil.rmtree('new_archive')
            shutil.rmtree('backup')
