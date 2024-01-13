import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import os

file_path = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\E9225_c01_SessionData_Extern_v008.xlsm'
object_path = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\aeromaps\21.pkl'

image_output_folder = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225'

rows = 1
cols = 1


# sweep through FRH and RRH plotting Cz vs yaw:
frh_list = [30, 40, 50, 60, 70, 80]
rrh_list = [30, 40, 50, 60, 70, 80]
roll = 0

for frh in frh_list:
    for rrh in rrh_list:
        # Create figures with the nunber o subplots equal to the number of teams:
        fig1, axs1 = plt.subplots(rows, cols, figsize=(15, 10), sharex=True, sharey=True)
        # add figure sup title with frh and rrh info:
        fig1.suptitle('FRH = ' + str(frh) + '/ RRH = ' + str(rrh))


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
        x0 = np.linspace(frh, frh, 50)
        x1 = np.linspace(rrh, rrh, 50)
        x2 = np.linspace(-10, 10, 50)
        x3 = np.linspace(roll, roll, 50)
        X_plot = np.vstack((x0.flatten(), x1.flatten(), x2.flatten(), x3.flatten())).T
        y_pred, sigma = gp.predict(X_plot, return_std=True)        

        # plot of the Gaussian process fit :
        axs1.plot(X_plot[:, 2], y_pred[:, 0], 'b-', label='Gaussian Process')
        axs1.fill(np.concatenate([X_plot[:, 2], X_plot[:, 2][::-1]]),
                np.concatenate([y_pred[:, 0] - 1.9600 * sigma[:, 0],
                                (y_pred[:, 0] + 1.9600 * sigma[:, 0])[::-1]]),
                alpha=.5, fc='b', ec='None', label='95% confidence interval')
        axs1.set_xlabel('UUTYaw')
        axs1.set_ylabel('Cz')
        axs1.legend(loc='upper left')
        axs1.set_title('run ' + str(run_number))



        # Save the figure:
        image_output_path = os.path.join(image_output_folder, 'Cz_vs_yaw_' + str(frh) + '_' + str(rrh) + '.png')
        fig1.savefig(image_output_path, dpi=300)


