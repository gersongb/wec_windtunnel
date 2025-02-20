# Author: Gerson Garsed-Brand
# Date: June 2023
# Description: class definitions for WT plots

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import rbf


class ACO_Plot:
    def __init__(self, df):
        self.df = df

    def create_rh_grid(self, grid_nx, grid_ny, extrapolation):
        # Create RH grid for contour plots:
        frh_min = self.df['UUTFRh'].min()
        frh_max = self.df['UUTFRh'].max()
        rrh_min = self.df['UUTRRh'].min()
        rrh_max = self.df['UUTRRh'].max()

        # Create grid:
        frh_new = np.linspace(frh_min-extrapolation, frh_max+extrapolation, grid_nx)
        rrh_new = np.linspace(rrh_min-extrapolation, rrh_max+extrapolation, grid_ny)
        frh_grid, rrh_grid = np.meshgrid(frh_new, rrh_new)
        
        self.frh_grid = frh_grid
        self.rrh_grid = rrh_grid

    def interpolate_data(self, x, y, z, x_grid, y_grid):
        # Interpolate data on grid:
        points = (list(x), list(y), list(z))
        interp = rbf.Rbf(points[0],
                         points[1],
                         points[2])
        z_grid = interp(x_grid.flatten(), y_grid.flatten())
        z_grid = np.reshape(z_grid, x_grid.shape)
        return z_grid
    
    def create_contour_plots(self, levels_Cz, levels_Cx, levels_AB, title):
        fig, ax = plt.subplots(1, 3, figsize=(16, 7))

        plt.subplot(131)
        cz_wt_grid = self.interpolate_data(self.df['UUTFRh'], self.df['UUTRRh'], self.df['Cz'], 
                                    self.frh_grid, self.rrh_grid)
        plt.contourf(self.frh_grid, self.rrh_grid, cz_wt_grid, extend='both', levels=levels_Cz)
        plt.plot(self.df['UUTFRh'], self.df['UUTRRh'], 'ko', ms=2)
        plt.colorbar()
        plt.title('Cz')
        plt.xlabel('FRH [mm]')
        plt.ylabel('RRH [mm]')

        plt.subplot(132)
        cx_wt_grid = self.interpolate_data(self.df['UUTFRh'], self.df['UUTRRh'], self.df['Cx'],
                                    self.frh_grid, self.rrh_grid)
        plt.contourf(self.frh_grid, self.rrh_grid, cx_wt_grid, extend='both', levels=levels_Cx)
        plt.plot(self.df['UUTFRh'], self.df['UUTRRh'], 'ko', ms=2)
        plt.colorbar()
        plt.title('Cx')
        plt.xlabel('FRH [mm]')
        plt.ylabel('RRH [mm]')

        plt.subplot(133)
        ab_wt_grid = self.interpolate_data(self.df['UUTFRh'], self.df['UUTRRh'], self.df['Pzf'],
                                    self.frh_grid, self.rrh_grid)
        plt.contourf(self.frh_grid, self.rrh_grid, ab_wt_grid, extend='both', levels=levels_AB)
        plt.plot(self.df['UUTFRh'], self.df['UUTRRh'], 'ko', ms=2)
        plt.colorbar()
        plt.title('AB')
        plt.xlabel('FRH [mm]')
        plt.ylabel('RRH [mm]')

        fig.suptitle(title)
        fig.tight_layout()

        return plt


    def create_line_plots(self, variable, axis_label, title, levels_Cz, levels_Cx, levels_AB, invert_flag):

        df = self.df.sort_values(by=[variable])
        fig, ax = plt.subplots(1, 3, figsize=(16, 7))

        plt.subplot(131)
        plt.plot(df[variable], df['Cz'], '-o', linewidth=2)
        if invert_flag:
            plt.gca().invert_xaxis()
        plt.title('Cz')
        plt.xlabel(axis_label)
        plt.ylabel('Cz')
        if len(levels_Cz)==2:
            plt.ylim((levels_Cz[0], levels_Cz[1]))

        plt.subplot(132)
        plt.plot(df[variable], df['Cx'], '-o', linewidth=2)
        if invert_flag:
            plt.gca().invert_xaxis()
        plt.title('Cx')
        plt.xlabel(axis_label)
        plt.ylabel('Cx')
        if len(levels_Cx)==2:
            plt.ylim((levels_Cx[0], levels_Cx[1]))

        plt.subplot(133)
        plt.plot(df[variable], df['Pzf'], '-o', linewidth=2)
        if invert_flag:
            plt.gca().invert_xaxis()
        plt.title('AB')
        plt.xlabel(axis_label)
        plt.ylabel('AB')
        if len(levels_AB)==2:
            plt.ylim((levels_AB[0], levels_AB[1]))

        fig.suptitle(title)
        fig.tight_layout()

        return plt


