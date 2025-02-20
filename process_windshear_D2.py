import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

ref_folder = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024\Raw_Data'

output_folder = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024\transient_data'

run_number = '0003'

# Get the list of all files in the folder:
folders = os.listdir(ref_folder)

# Loop through the files and find the one ending with the run number:
target_file = None
for folder in folders:
    if folder.endswith(run_number):
        target_folder = os.path.join(ref_folder, folder)
        target_file = os.path.join(target_folder, 'D2.asc')

# Read the file as a pandas dataframe:
print('Reading file:', target_file)
f = open(target_file, 'r')

# Remove the first three rows:
f.readline()
f.readline()
f.readline()

# Convert the rest of the file to a dataframe:
df = pd.read_csv(f, sep='\t')

# Remove the first row:
df = df.iloc[1:]

# Retain only colums LF, LR, L, D, DYNPR, RRS Speed Feedback and Air Velocity:
df = df[['LF', 'LR', 'L', 'D', 'DYNPR', 'RRS Speed Feedback', 'Air Velocity', 
         'DYNPR', 'YAW', 'Test Time', 'Point Number', 'Ride-Height-Number', 'Tunnel_Air_Temp', 
         'Relative_Humidity', 'WSI-Scaled-AI03', 'WSI-Scaled-AI04', 
         'WSI-Scaled-AI07', 'WSI-Scaled-AI08', 'FRH', 'RRH', 'RH-Roll', 'Move-Complete', 'SCS_TS_DATA_STG_STATUS']]

# Convert all values to float:
df = df.astype(float)

# Loop through the point numbers from zero to max:
point_numbers_to_remove = []
for i in range(int(df['Point Number'].max())+1):
    # Remove all the rows with the point number i if one of them has air velocity below 10:
    if df[df['Point Number'] == i]['Air Velocity'].min() < 10:
        point_numbers_to_remove.append(i)
        print('Removing point number:', i)
        
# Remove the rows with the point numbers in point_numbers_to_remove:
df = df[~df['Point Number'].isin(point_numbers_to_remove)]
        
# Loop through the point numbers:
for i in range(int(df['Point Number'].max())+1):
    # If i is not in the point_numbers_to_remove list, plot subplots of L, D, LF, LR as a function of time:
    #if i not in point_numbers_to_remove:
        df_point = df[df['Point Number'] == i]
        fig, ax = plt.subplots(4, 1, figsize=(10, 10))
        ax[0].plot(df_point['Test Time'], df_point['L'])
        ax[0].set_title('L')
        ax[1].plot(df_point['Test Time'], df_point['D'])
        ax[1].set_title('D')
        ax[2].plot(df_point['Test Time'], df_point['LF'])
        ax[2].set_title('LF')
        ax[3].plot(df_point['Test Time'], df_point['LR'])
        ax[3].set_title('LR')
        
        #plt.tight_layout
        
        plot_title = 'Run ' + run_number + ' Point ' + str(i)
        plt.suptitle(plot_title)
        
        # Save the plot:
        output_file = os.path.join(output_folder, plot_title.replace(' ', '_') + '.png')
        plt.savefig(output_file)
        
        
    
    



