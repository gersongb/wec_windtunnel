import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import img2pdf

ref_folder = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024\Raw_Data'

output_folder = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024\transient_data'


run_number = '0009'

data_folder = os.path.join(output_folder, run_number)

# create data folder if it does not exist:
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

laserF = [-61, -8.5, 0]
laserRL = [2679, -820.81, 0]  
laserRR = [2679, 820.81, 0] 
wheelbase = 3148

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

# Calculate the roll angle:
df['Roll'] = np.arctan((df['WSI-Scaled-AI08']-df['WSI-Scaled-AI07'])/(laserRR[1]-laserRL[1]))
df['Roll Degrees'] = df['Roll']*180/np.pi

# Calculate the centerline laser measurements:
df['MLaserF'] = df['WSI-Scaled-AI04'] - np.tan(df['Roll'])*laserF[1]
df['MLaserR'] = (df['WSI-Scaled-AI08']+df['WSI-Scaled-AI07'])/2

# Calculate the pitch angle:
df['pitch'] = np.arctan((df['MLaserR'] - df['MLaserF'])/((laserRR[0]+laserRL[0])/2 - laserF[0]))

# Calculate the ride height:
df['MFRH'] = df['MLaserF'] - np.tan(df['pitch'])*laserF[0]
df['MRRH'] = df['MLaserR'] + np.tan(df['pitch'])*(wheelbase - (laserRR[0]+laserRL[0])/2)

# Create an empty dataframe to store the target, mean, delta to target and standard deviation:
columns = ['Ride-Height-Number', 'FRH', 'RRH', 'Delta FRH', 'Delta RRH', 'Stddev FRH', 'Stddev RRH']
df_summary = pd.DataFrame(columns=columns)

# Loop through the point numbers:
for i in range(int(df['Point Number'].max())+1):
        df_point = df[df['Point Number'] == i]
        
        df_point['sampling'] = df_point['SCS_TS_DATA_STG_STATUS'].diff()
        df_change = df_point[(df_point['sampling'] != 0) & (df_point['sampling'] != -1)].iloc[-1]

        start_time = df_change['Test Time']
        end_time = start_time + 30
        
        df_complete = df_point[(df_point['Test Time'] > start_time) & (df_point['Test Time'] < end_time)]
        
        # if df_complete is empty, skip the rest of the loop:
        if df_complete.empty == False:

            # Calculate the mean and standard deviation of the FRH and RRH:
            mean_FRH = df_complete['MFRH'].mean()
            mean_RRH = df_complete['MRRH'].mean()
            std_FRH = df_complete['MFRH'].std()
            std_RRH = df_complete['MRRH'].std()
            
            # Calculate the delta to the target:
            target_FRH = df_complete['FRH'].iloc[-1]
            target_RRH = df_complete['RRH'].iloc[-1]
            
            delta_FRH = mean_FRH - target_FRH
            delta_RRH = mean_RRH - target_RRH
            
            # round the values:
            target_FRH = round(target_FRH, 2)
            
            # Add the data to the summary dataframe:
            df_summary.loc[i] = [df_complete['Ride-Height-Number'].iloc[-1], round(target_FRH,1), round(target_RRH,1), round(delta_FRH,1), round(delta_RRH,1), round(std_FRH,1), round(std_RRH,1)]
            
           
            fig, ax = plt.subplots(2, 1, figsize=(10, 10))
            ax[0].plot(df_point['Test Time'], df_point['MFRH'], color='red', label='raw')
            ax[0].axhline(y=df_complete['MFRH'].mean(), color='red', linestyle='--', label='mean')
            ax[0].plot(df_complete['Test Time'], df_complete['FRH'], color='black', label='target')
            
            ax[0].set_title('FRH')
            ax[0].set_ylim([df_complete['FRH'].min()-2, df_complete['FRH'].max()+2])
            ax[0].set_xlabel('Time (s)')
            ax[0].set_ylabel('FRH (mm)')
            
            # add text to the plot with the delta between the mean and the target:
            ax[0].text(0.7, 0.1, 'Mean-Target: ' + str(round(delta_FRH, 2)) + 'mm', horizontalalignment='center', verticalalignment='center', transform=ax[0].transAxes)
            
            # add text to the plot with the standard deviation:
            std = df_point['MFRH'].std()
            ax[0].text(0.9, 0.1, 'Stddev: ' + str(round(std_FRH, 2)) + 'mm', horizontalalignment='center', verticalalignment='center', transform=ax[0].transAxes)
            
            ax[1].plot(df_point['Test Time'], df_point['MRRH'], color='red', label='raw')
            ax[1].axhline(y=df_complete['MRRH'].mean(), color='red', linestyle='--', label='mean')
            ax[1].plot(df_complete['Test Time'], df_complete['RRH'], color='black', label='target')
            ax[1].set_title('RRH')
            ax[1].set_ylim([df_complete['RRH'].min()-2, df_complete['RRH'].max()+2])
            ax[1].set_xlabel('Time (s)')
            ax[1].set_ylabel('RRH (mm)')
            
            # add text to the plot with the delta between the mean and the target:
            ax[1].text(0.7, 0.1, 'Mean-Target: ' + str(round(delta_FRH, 2)) + 'mm', horizontalalignment='center', verticalalignment='center', transform=ax[1].transAxes)
            
            # add text to the plot with the standard deviation:
            std = df_point['MRRH'].std()
            ax[1].text(0.9, 0.1, 'Stddev: ' + str(round(std_FRH, 2)) + 'mm', horizontalalignment='center', verticalalignment='center', transform=ax[1].transAxes)
            
            # show legend:
            ax[0].legend()
            ax[1].legend()
        
            # turn i into a double digit string:
            if i < 10:
                str_i = '0' + str(i)
            else:
                str_i = str(i)
    
            
            plot_title = str_i + ' Run ' + run_number + ' RH_Number ' + str(df_point['Ride-Height-Number'].iloc[-1])
            plt.suptitle(plot_title)
            
            # Save the plot:
            output_file = os.path.join(data_folder, plot_title.replace(' ', '_') + '.png')
            plt.savefig(output_file)
        
# Save the summary dataframe to a csv file:
df_summary.to_csv(os.path.join(data_folder, run_number + '_RH_summary.csv'))      

# Create a plot with a table of the df_summary dataframe:
fig, ax = plt.subplots(figsize=(10, 10))
ax.axis('off')
ax.axis('tight')
table = ax.table(cellText=df_summary.values, colLabels=df_summary.columns, cellLoc='center', loc='center')
table.set_fontsize(24)  
plot_title = '000 Run ' + run_number + 'RH summary'
plt.title('Summary')
plt.tight_layout()
output_file = os.path.join(data_folder, plot_title.replace(' ', '_') + '.png')
plt.savefig(output_file)

# create a pdf file with the images:
# Get the list of all files in the folder:
files = os.listdir(data_folder)

# Loop through the files and find the ones ending with .png:
images = []
for file in files:
    if file.endswith('.png'):
        images.append(os.path.join(data_folder, file))
        
# Create the pdf file:
with open(os.path.join(output_folder, run_number + '_RH.pdf'), 'wb') as f:
    f.write(img2pdf.convert(images))
    f.close()
    


        