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


wt_dir = r'Z:\homologation\WT_data\SAUBER-LMH-LMDh\Alpine 2023'
file_name = 'E9216_c01_SessionData_Extern_v008.xlsm'
title = '033'
groups = ['Yaw Sensitivity']
wt_file = os.path.join(wt_dir, file_name)

# Load wt data into a dataframe:
wt_data = pd.read_excel(wt_file, sheet_name=title, skiprows=[0])
wt_data.rows = wt_data.iloc[0]
wt_data = wt_data[2:]

target_columns = ['Group', 'WindSpeed', 'RoadSpeed', 'UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll', 'UUTPitch',
                  'Cx', 'Cz', 'Czf', 'Czr', 'Pzf', 'Eff']

wt_data = wt_data[target_columns]
wt_data = wt_data.dropna(axis='rows')

# Sort the dataframe by yaw angle:
wt_data = wt_data.sort_values(by=['UUTYaw'])


for group in groups:

    # Filter based on condition:
    df_target = wt_data[(wt_data['Group'] == group)]

    fig, ax = plt.subplots(1, 3, figsize=(16, 7))
    plt.subplot(131)
    plt.plot(df_target['UUTYaw'], df_target['Cz'], '-o', linewidth=2)
    plt.gca().invert_xaxis()
    plt.title('Cz')
    plt.xlabel('yaw [deg]')
    plt.ylabel('Cz')
    #plt.ylim((-4.5, -3.8))

    plt.subplot(132)
    plt.plot(df_target['UUTYaw'], df_target['Cx'], '-o', linewidth=2)
    plt.gca().invert_xaxis()
    plt.title('Cx')
    plt.xlabel('yaw [deg]')
    plt.ylabel('Cx')
    #plt.ylim((1, 1.1))

    plt.subplot(133)
    plt.plot(df_target['UUTYaw'], df_target['Pzf'], '-o', linewidth=2)
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


