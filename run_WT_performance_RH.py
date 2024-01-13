# This is a python script to analyse data from the Sauber wt
# Author: Gerson Garsed-Brand
# Date: Feb 202"
import os.path

import pandas as pd
import numpy as np
from scipy.interpolate import rbf
import matplotlib.pyplot as plt


wt_dir = r'Z:\homologation\WT_data\SAUBER-LMH-LMDh\Alpine 2023'
file_name = 'E9216_c01_SessionData_Extern_v008.xlsm'
title = '033'
groups = ['RH Sensitivity (yaw-roll)', 'RH Sensitivity (SL)']
wt_file = os.path.join(wt_dir, file_name)

# Load wt data into a dataframe:
wt_data = pd.read_excel(wt_file, sheet_name=title, skiprows=[0])
wt_data.rows = wt_data.iloc[0]
wt_data = wt_data[2:]

target_columns = ['Group', 'WindSpeed', 'RoadSpeed', 'UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll', 'UUTPitch',
                  'Cx', 'Cz', 'Czf', 'Czr', 'Pzf', 'Eff']

wt_data = wt_data[target_columns]
wt_data = wt_data.dropna(axis='rows')

for group in groups:

    # Filter based on condition:
    df_target = wt_data[(wt_data['Group'] == group)]


    # Create RH grid for contour plots:
    frh_min = df_target['UUTFRh'].min()
    frh_max = df_target['UUTFRh'].max()
    rrh_min = df_target['UUTRRh'].min()
    rrh_max = df_target['UUTRRh'].max()

    # Create grid:
    grid_nx = 50
    grid_ny = 50
    x_new = np.linspace(frh_min-2, frh_max+2, grid_nx)
    y_new = np.linspace(rrh_min-2, rrh_max+2, grid_ny)
    x_grid, y_grid = np.meshgrid(x_new, y_new)

    # Interpolate data on grid:
    # Remove duplicate FRH/RRH pairs:
    df_target = df_target.drop_duplicates(subset=['UUTFRh', 'UUTRRh'], keep='first')

    print(df_target)

    points_wt = (list(df_target['UUTFRh']), list(df_target['UUTRRh']), list(df_target['Cz']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    cz_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    cz_wt_grid = np.reshape(cz_wt_grid, x_grid.shape)

    points_wt = (list(df_target['UUTFRh']), list(df_target['UUTRRh']), list(df_target['Cx']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    cx_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    cx_wt_grid = np.reshape(cx_wt_grid, x_grid.shape)

    points_wt = (list(df_target['UUTFRh']), list(df_target['UUTRRh']), list(df_target['Czf']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    czf_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    czf_wt_grid = np.reshape(czf_wt_grid, x_grid.shape)

    points_wt = (list(df_target['UUTFRh']), list(df_target['UUTRRh']), list(df_target['Czr']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    czr_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    czr_wt_grid = np.reshape(czr_wt_grid, x_grid.shape)

    points_wt = (list(df_target['UUTFRh']), list(df_target['UUTRRh']), list(df_target['Pzf']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    ab_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    ab_wt_grid = np.reshape(ab_wt_grid, x_grid.shape)

    points_wt = (list(df_target['UUTFRh']), list(df_target['UUTRRh']), list(df_target['Eff']))
    interp = rbf.Rbf(points_wt[0],
                     points_wt[1],
                     points_wt[2])
    eff_wt_grid = interp(x_grid.flatten(), y_grid.flatten())
    eff_wt_grid = np.reshape(eff_wt_grid, x_grid.shape)

    #fig, ax = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(16, 7))
    fig, ax = plt.subplots(1, 3, figsize=(16, 7))
    levels_cz = np.linspace(-4.9, -4, 21)
    levels_cx = np.linspace(0.95, 1.1, 11)
    levels_qb = np.linspace(40, 50, 11)

    plt.subplot(131)
    plt.contourf(x_grid, y_grid, cz_wt_grid, extend='both', levels=levels_cz)
    plt.plot(df_target['UUTFRh'], df_target['UUTRRh'], 'ko', ms=2)
    plt.colorbar()
    plt.title('Cz')
    plt.xlabel('FRH [mm]')
    plt.ylabel('RRH [mm]')

    plt.subplot(132)
    plt.contourf(x_grid, y_grid, cx_wt_grid, extend='both', levels=levels_cx)
    plt.plot(df_target['UUTFRh'], df_target['UUTRRh'], 'ko', ms=2)
    plt.colorbar()
    plt.title('Cx')
    plt.xlabel('FRH [mm]')
    plt.ylabel('RRH [mm]')

    plt.subplot(133)
    plt.contourf(x_grid, y_grid, ab_wt_grid, extend='both')
    plt.plot(df_target['UUTFRh'], df_target['UUTRRh'], 'ko', ms=2)
    plt.colorbar()
    plt.title('AB')
    plt.xlabel('FRH [mm]')
    plt.ylabel('RRH [mm]')

    fig.suptitle("Run: " + title + ' / Group: ' + group)
    fig.tight_layout()

    fig_path = os.path.join(wt_dir, title + '_' + group.replace(' ', '') + ".png")
    plt.savefig(fig_path)
    plt.close()


