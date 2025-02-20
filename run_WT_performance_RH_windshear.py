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
groups = ['RH Sensitivity (yaw-roll)', 'RH Sensitivity (SL)']
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

hs_drag_tare_133 = df[(df['RRS Speed Feedback'] > 110) & (df['RRS Speed Feedback'] < 135) & (abs(df['Air Velocity']) < 1)].iloc[-1]


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

    # Create RH grid for contour plots:
    frh_min = df_target['FRH'].min()
    frh_max = df_target['FRH'].max()
    rrh_min = df_target['RRH'].min()
    rrh_max = df_target['RRH'].max()

    # Create grid:
    grid_nx = 50
    grid_ny = 50
    x_new = np.linspace(frh_min-2, frh_max+2, grid_nx)
    y_new = np.linspace(rrh_min-2, rrh_max+2, grid_ny)
    x_grid, y_grid = np.meshgrid(x_new, y_new)

    # Interpolate data on grid:
    # Remove duplicate FRH/RRH pairs:
    df_target = df_target.drop_duplicates(subset=['FRH', 'RRH'], keep='first')

    print(df_target)

    points_wt = (list(df_target['FRH']), list(df_target['RRH']), list(df_target['Cz']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    cz_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    cz_wt_grid = np.reshape(cz_wt_grid, x_grid.shape)

    points_wt = (list(df_target['FRH']), list(df_target['RRH']), list(df_target['Cx']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    cx_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    cx_wt_grid = np.reshape(cx_wt_grid, x_grid.shape)

    points_wt = (list(df_target['FRH']), list(df_target['RRH']), list(df_target['Czf']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    czf_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    czf_wt_grid = np.reshape(czf_wt_grid, x_grid.shape)

    points_wt = (list(df_target['FRH']), list(df_target['RRH']), list(df_target['Czr']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    czr_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    czr_wt_grid = np.reshape(czr_wt_grid, x_grid.shape)

    points_wt = (list(df_target['FRH']), list(df_target['RRH']), list(df_target['AB']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    ab_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    ab_wt_grid = np.reshape(ab_wt_grid, x_grid.shape)

    points_wt = (list(df_target['FRH']), list(df_target['RRH']), list(df_target['Eff']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    eff_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    eff_wt_grid = np.reshape(eff_wt_grid, x_grid.shape)

    #fig, ax = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(16, 7))
    fig, ax = plt.subplots(1, 3, figsize=(16, 7))
    levels_cz = np.linspace(-5, -4, 21)
    levels_cx = np.linspace(0.9, 1.1, 11)
    levels_qb = np.linspace(40, 50, 11)

    plt.subplot(131)
    plt.contourf(x_grid, y_grid, cz_wt_grid, extend='both', levels=levels_cz)
    plt.plot(df_target['FRH'], df_target['RRH'], 'ko', ms=2)
    plt.colorbar()
    plt.title('Cz')
    plt.xlabel('FRH [mm]')
    plt.ylabel('RRH [mm]')

    plt.subplot(132)
    plt.contourf(x_grid, y_grid, cx_wt_grid, extend='both', levels=levels_cx)
    plt.plot(df_target['FRH'], df_target['RRH'], 'ko', ms=2)
    plt.colorbar()
    plt.title('Cx')
    plt.xlabel('FRH [mm]')
    plt.ylabel('RRH [mm]')

    plt.subplot(133)
    plt.contourf(x_grid, y_grid, ab_wt_grid, extend='both')
    plt.plot(df_target['FRH'], df_target['RRH'], 'ko', ms=2)
    plt.colorbar()
    plt.title('AB')
    plt.xlabel('FRH [mm]')
    plt.ylabel('RRH [mm]')

    fig.suptitle("Run: " + title + ' / Group: ' + group)
    fig.tight_layout()

    fig_path = os.path.join(wt_dir, title + '_' + group.replace(' ', '') + ".png")
    plt.savefig(fig_path)
    plt.close()


