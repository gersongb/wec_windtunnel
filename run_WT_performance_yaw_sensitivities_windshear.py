# This is a python script to analyse data from the Sauber wt
# Author: Gerson Garsed-Brand
# Date: Feb 202"
import os.path

import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import rbf
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Convertion values:
PSF_to_Newtons = 47.88125
LBF_to_Newtons= 4.44822

wt_dir = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024'
file_name = 'sensitivity.csv'
groups = ['Yaw Sensitivity']
wt_file = os.path.join(wt_dir, file_name)
title = 'Sensitivity'
print(wt_file)

# Load the data into a dataframe:
f = open(wt_file, 'r')
df = pd.read_csv(f, skiprows=0)

df = df.iloc[1:]
print(df.head())
# Retain only colums LF, LR, L, D, DYNPR, RRS Speed Feedback and Air Velocity:
df = df[['group', 'FRH','RRH','RH-Roll','YAW','LF', 'LR', 'L', 'D', 'DYNPR', 'RRS Speed Feedback', 'Air Velocity']]

# Convert all values to float apart from the group column:
df = df.astype({'group': str, 'FRH': float, 'RRH': float, 'RH-Roll': float, 'YAW': float, 'LF': float, 'LR': float, 'L': float, 'D': float, 'DYNPR': float, 'RRS Speed Feedback': float, 'Air Velocity': float})



# Find the tare values:

hs_drag_tare_133 = df[(df['RRS Speed Feedback'] > 100) & (df['RRS Speed Feedback'] < 135) & (abs(df['Air Velocity']) < 1)].iloc[-1]


hs_lift_tare_133 = df[(df['RRS Speed Feedback'] < 5) & (abs(df['Air Velocity']) < 1)].iloc[-1]

# Create a copy of df and retain only the wind on data:
df_133 = df[(abs(df['Air Velocity']) > 1) & (abs(df['Air Velocity']) < 150)]

# Subtract the tare values from the wind on data for all columns:
results = pd.DataFrame()
results['Cx'] = (df_133['D']-hs_drag_tare_133['D'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
results['Cz'] = (df_133['L']-hs_lift_tare_133['L'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
results['Czf'] = (df_133['LF']-hs_lift_tare_133['LF'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
results['Czr'] = (df_133['LR']-hs_lift_tare_133['LR'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
results['AB'] = 100*results['Czf']/results['Cz']
results['FRH'] = df_133['FRH']
results['RRH'] = df_133['RRH']
results['Roll'] = df_133['RH-Roll']
results['yaw'] = df_133['YAW']
results['Eff'] = results['Cz']/results['Cx']
results['group'] = df_133['group']


# Re-index the dataframe:
results = results.reset_index(drop=True)

print(results)

for group in groups:

    # Filter based on condition:
    df_target = results[(results['group'] == group)]

    fig, ax = plt.subplots(1, 3, figsize=(16, 7))
    plt.subplot(131)
    plt.plot(df_target['yaw'], df_target['Cz'], '-o', linewidth=2)
    plt.gca().invert_xaxis()
    plt.title('Cz')
    plt.xlabel('yaw [deg]')
    plt.ylabel('Cz')
    #plt.ylim((-4.5, -3.8))

    plt.subplot(132)
    plt.plot(df_target['yaw'], df_target['Cx'], '-o', linewidth=2)
    plt.gca().invert_xaxis()
    plt.title('Cx')
    plt.xlabel('yaw [deg]')
    plt.ylabel('Cx')
    #plt.ylim((1, 1.1))

    plt.subplot(133)
    plt.plot(df_target['yaw'], df_target['AB'], '-o', linewidth=2)
    plt.gca().invert_xaxis()
    plt.title('AB')
    plt.xlabel('yaw [deg]')
    plt.ylabel('AB')
    #plt.ylim((45, 55))


    fig.suptitle("Run: " + title + ' / Group: ' + group)
    fig.tight_layout()

    fig_path = os.path.join(wt_dir, title + '_' + group.replace(' ', '') + ".png")
    plt.savefig(fig_path)
    plt.close()


