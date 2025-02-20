import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

folder = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225'
file_name = 'RunDataLive_E9225_0024.csv'
file_path = os.path.join(folder, file_name)

gp_path = os.path.join(folder, 'gp_fit.npy')

# Load the Gaussian process fit:
gp = np.load(gp_path, allow_pickle=True).item()

# Print the optimised hyperparameters:
print(gp.kernel_)
print(gp.log_marginal_likelihood(gp.kernel_.theta))

x0 = np.linspace(30, 30, 50)
x1 = np.linspace(60, 60, 50)
x2 = np.linspace(-10, 10, 50)
x3 = np.linspace(-0, -0, 50)
X_plot = np.vstack((x0.flatten(), x1.flatten(), x2.flatten(), x3.flatten())).T
y_pred, sigma = gp.predict(X_plot, return_std=True)

# create a comparison plot of the Gaussian process fit and the actual data:

fig, ax = plt.subplots()
ax.plot(X_plot[:, 2], y_pred[:, 0], 'b-', label='Gaussian Process')
ax.fill(np.concatenate([X_plot[:, 2], X_plot[:, 2][::-1]]),
        np.concatenate([y_pred[:, 0] - 1.9600 * sigma[:, 0],
                        (y_pred[:, 0] + 1.9600 * sigma[:, 0])[::-1]]),
        alpha=.5, fc='b', ec='None', label='95% confidence interval')
ax.set_xlabel('UUTYaw')
ax.set_ylabel('CLTot')
#ax.set_ylim(-0.5, 1.5)
ax.legend(loc='upper left')
plt.show()

x0 = np.linspace(30, 80, 20)
x1 = np.linspace(30, 100, 20)
x2 = np.linspace(5, 5, 1)
x3 = np.linspace(-.5, -.5, 1)
x0, x1, x2, x3 = np.meshgrid(x0, x1, x2, x3)
X_plot = np.vstack((x0.flatten(), x1.flatten(), x2.flatten(), x3.flatten())).T
y_pred, sigma = gp.predict(X_plot, return_std=True)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X_plot[:, 0], X_plot[:, 1], y_pred[:, 0], linewidth=0.2, antialiased=True)
#ax.scatter(X3[:, 0], X3[:, 1], y3, c='r', marker='o')
ax.set_xlabel('UUTFRh')
ax.set_ylabel('UUTRRh')
ax.set_zlabel('CLTot')
ax.plot_trisurf(X_plot[:, 0], X_plot[:, 1], y_pred[:, 0] + sigma[:, 0], linewidth=0.2, antialiased=True, color='b', alpha=0.2)
ax.plot_trisurf(X_plot[:, 0], X_plot[:, 1], y_pred[:, 0] - sigma[:, 0], linewidth=0.2, antialiased=True, color='b', alpha=0.2)
plt.show() 
