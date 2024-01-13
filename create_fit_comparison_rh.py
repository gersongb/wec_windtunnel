import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import os
from scipy.interpolate import rbf

file_path = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\E9225_c01_SessionData_Extern_v008.xlsm'
object_path = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\aeromaps\21.pkl'

image_output_folder = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225'

rows = 1
cols = 1


# sweep through FRH and RRH plotting Cz vs yaw:
frh_range = [30, 80]
rrh_range = [30, 100]
roll_list = [0, -0.5, -1, -1.5]
yaw_list = [0, 1.5, 3, 5, 7]

for roll in roll_list:
    for yaw in yaw_list:
        # Create figures with the nunber o subplots equal to the number of teams:
        fig1, axs1 = plt.subplots(rows, cols, figsize=(15, 10), sharex=True, sharey=True)
        # add figure sup title with frh and rrh info:
        fig1.suptitle('Cz - Yaw = ' + str(yaw) + '/ Roll = ' + str(roll))
        # Read the object:
        pkl_file = open(object_path, 'rb')
        team_object = pickle.load(pkl_file)
        pkl_file.close()

        file_path = team_object.aeromap.wt_import_path 
        run_number = team_object.aeromap.run_number

        gp_path = team_object.aeromap.gp_path  
        gp = team_object.aeromap.read_gp()

        # Print the optimised hyperparameters:
        print(gp.kernel_)
        print(gp.log_marginal_likelihood(gp.kernel_.theta))
        x0 = np.linspace(frh_range[0], frh_range[1], 20)
        x1 = np.linspace(rrh_range[0], rrh_range[1], 20)
        x2 = np.linspace(yaw, yaw, 1)
        x3 = np.linspace(roll, roll, 1)
        x0, x1, x2, x3 = np.meshgrid(x0, x1, x2, x3)
        X_plot = np.vstack((x0.flatten(), x1.flatten(), x2.flatten(), x3.flatten())).T
        y_pred, sigma = gp.predict(X_plot, return_std=True)              

        x1_grid, x2_grid = np.meshgrid(X_plot[:, 0], X_plot[:, 1])
        points = (list(X_plot[:, 0]), list(X_plot[:, 1]), list(y_pred[:, 0]))
        interp = rbf.Rbf(points[0],
                        points[1],
                        points[2])
        z_grid = interp(x1_grid, x2_grid)
        z_grid = np.reshape(z_grid, x1_grid.shape)

        # Create a contour plot:
        levels = np.linspace(-4.4, -3, 21)

        fig1.colorbar(axs1.contourf(x1_grid, x2_grid, z_grid, 20, levels=levels, extend='both'), ax=axs1)
        axs1.set_title(run_number)
        axs1.set_xlabel('FRH')
        axs1.set_ylabel('RRH')
        axs1.set_xlim(frh_range[0], frh_range[1])
        axs1.set_ylim(rrh_range[0], rrh_range[1])
        axs1.grid(True)




        # Save the figure:
        image_output_path = os.path.join(image_output_folder, 'Cz_vs_rh_' + str(yaw) + '_' + str(roll) + '.png')
        fig1.savefig(image_output_path, dpi=300)


