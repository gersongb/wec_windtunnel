# This is a python script to analyse data from the Sauber wt
# Author: Gerson Garsed-Brand
# Date: Jab 2024"
import os.path

import pandas as pd
import numpy as np
from scipy.interpolate import rbf
import matplotlib.pyplot as plt
import aco_plots as acop


wt_dir = r'Z:\homologation\WT_data\SAUBER-LMH-LMDh\Lambo 2024'
file_name = 'E9202_c01_SessionData_Extern_v008.xlsm'
title = '028'



rh_groups = [['RH Sensitivity (yaw-roll)', ['S07', 'S08', 'S09', 'S10', 'S11', 'S12', 'S13', 'S14',
                                         'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22',
                                         'S23', 'S24', 'S25', 'S26', 'S27', 'S28', 'S29', 'S30',
                                         'S31', 'S32', 'S33', 'S34', 'S35', 'S36'],
                                         [-4.2, -3.2, 21], # Cz levels
                                         [0.90, 1.10, 11], # Cx levels
                                         [20, 50, 11], # AB levels
                                         5], # Extrapolation

            ['RH Sensitivity (SL)', ['S46', 'S47', 'S48', 'S49', 'S50', 'S51', 'S52', 'S53','S54'],
                                         [-4.9, -3.9, 21], # Cz levels
                                         [0.93, 1.08, 11], # Cx levels
                                         [30, 45, 11], # AB levels
                                         2]] # Extrapolation

yaw_group = ['Yaw Sensitivity', ['S37', 'S38', 'S39', 'S40', 'S41', 'S42', 'S43', 'S44']]


roll_group = ['Roll Sensitivity', ['S01', 'S02', 'S03', 'S04', 'S05', 'S06'],
                [-4.3, -3.5], # Cz levels
                [1.0, 1.1], # Cx levels
                [35, 45]] # AB levels]]                  

wt_file = os.path.join(wt_dir, file_name)

# Load wt data into a dataframe:
wt_data = pd.read_excel(wt_file, sheet_name=title, skiprows=[0])
wt_data.rows = wt_data.iloc[0]
wt_data = wt_data[2:]

target_columns = ['StepName', 'WindSpeed', 'RoadSpeed', 'UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll', 'UUTPitch',
                  'Cx', 'Cz', 'Czf', 'Czr', 'Pzf', 'Eff']

wt_data = wt_data[target_columns]
wt_data = wt_data.dropna(axis='rows')

# Create RH contour plots:
for group, step_names, levels_Cz, levels_Cx, levels_AB, extrapolation in rh_groups:   

    # Filter wt data, retaining only the step names in the column 'StepName':
    df_target = wt_data[wt_data['StepName'].isin(step_names)]
    df_target = df_target.drop_duplicates(subset=['UUTFRh', 'UUTRRh'], keep='first')

    # Create RH grid for contour plots:
    plot = acop.ACO_Plot(df_target)
    plot.create_rh_grid(50, 50, extrapolation)

    plot_title = "Run: " + title + ' / Group: ' + group
    fig_path = os.path.join(wt_dir, title + '_' + group.replace(' ', '') + ".png")

    levels_Cz = np.linspace(levels_Cz[0], levels_Cz[1], levels_Cz[2])
    levels_Cx = np.linspace(levels_Cx[0], levels_Cx[1], levels_Cx[2])
    levels_AB = np.linspace(levels_AB[0], levels_AB[1], levels_AB[2])

    plt = plot.create_contour_plots(levels_Cz, levels_Cx, levels_AB, plot_title)
    plt.savefig(fig_path)
    plt.close()

# Create yaw sensitivity plots:
group = yaw_group[0]
step_names = yaw_group[1]
df_target = wt_data[wt_data['StepName'].isin(step_names)]
plot = acop.ACO_Plot(df_target)
plot_title = "Run: " + title + ' / Group: ' + group
fig_path = os.path.join(wt_dir, title + '_' + group.replace(' ', '') + ".png")
plt = plot.create_line_plots('UUTYaw', 'yaw [deg]', plot_title, [], [], [], False)
plt.savefig(fig_path)
plt.close()

# Create roll sensitivity plots:
group = roll_group[0]
step_names = roll_group[1]
Cz_levels = roll_group[2]
Cx_levels = roll_group[3]
AB_levels = roll_group[4]
df_target = wt_data[wt_data['StepName'].isin(step_names)]
plot = acop.ACO_Plot(df_target)
plot_title = "Run: " + title + ' / Group: ' + group
fig_path = os.path.join(wt_dir, title + '_' + group.replace(' ', '') + ".png")
plt = plot.create_line_plots('UUTRoll', 'roll [deg]', plot_title, Cz_levels, Cx_levels, AB_levels, True)
plt.savefig(fig_path)
plt.close()