import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

file_path = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\E9225_c01_SessionData_Extern_v008.xlsm'
object_path = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\aeromaps\21.pkl'

# Read the object:
pkl_file = open(object_path, 'rb')
team_object = pickle.load(pkl_file)
pkl_file.close()

file_path = team_object.aeromap.wt_import_path 
run_number = team_object.aeromap.run_number

gp_path = team_object.aeromap.gp_path  
print(gp_path)
gp = team_object.aeromap.read_gp()

# Load wind tunnel data:
wt_data = pd.read_excel(file_path, sheet_name=run_number, skiprows=[0])
wt_data = wt_data[(wt_data['WindSpeed'] > 40)]

# Enforce zero yaw/roll when values are small:
wt_data.loc[wt_data['UUTYaw'].abs() < 0.01, 'UUTYaw'] = 0
wt_data.loc[wt_data['UUTRoll'].abs() < 0.01, 'UUTRoll'] = 0

# Mirror points where yaw & roll are not zero:
temp_df = wt_data
temp_df = temp_df.drop(temp_df[(temp_df['UUTYaw'] == 0) & (temp_df['UUTRoll'] == 0)].index)
temp_df['UUTYaw'] = -temp_df['UUTYaw']
temp_df['UUTRoll'] = -temp_df['UUTRoll']

wt_data = pd.concat([wt_data, temp_df], axis=0)

X = wt_data[['UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll']].to_numpy()
y = wt_data[['Cz']]

# Print the optimised hyperparameters:
print(gp.kernel_)
print(gp.log_marginal_likelihood(gp.kernel_.theta))

# Create a subset of X and y with UUTFRh between 34 and 36, UUTRRh between 59 and 61 and UUTRoll between -0.51 and -0.49:
X2 = X[(X[:, 0] > 48) & (X[:, 0] < 52) & (X[:, 1] > 53) & (X[:, 1] < 57) & (X[:, 3] > -0.5) & (X[:, 3] < 0.5)]
y2 = y[(X[:, 0] > 48) & (X[:, 0] < 52) & (X[:, 1] > 53) & (X[:, 1] < 57) & (X[:, 3] > -0.5) & (X[:, 3] < 0.5)]

# Create a line plot of the Gaussian process fit of X2 and y2, varying X2[:, 2] between -8 and 8:
x0_min, x0_max = X2[:, 0].min() - 5, X2[:, 0].max() + 5
x1_min, x1_max = X2[:, 1].min() - 5, X2[:, 1].max() + 5
x2_min, x2_max = X2[:, 2].min() - 2, X2[:, 2].max() + 2
x3_min, x3_max = X2[:, 3].min() - 0.1, X2[:, 3].max() + 0.1

x0 = np.linspace(50, 50, 50)
x1 = np.linspace(55, 55, 50) 
x2 = np.linspace(x2_min - 2, x2_max + 2, 50)
x3 = np.linspace(0, 0, 50)
X_plot = np.vstack((x0.flatten(), x1.flatten(), x2.flatten(), x3.flatten())).T
y_pred, sigma = gp.predict(X_plot, return_std=True)

# create a comparison plot of the Gaussian process fit and the actual data:
fig, ax = plt.subplots()
ax.plot(X2[:, 2], y2, 'r.', markersize=10, label='Actual')
ax.plot(X_plot[:, 2], y_pred[:, 0], 'b-', label='Gaussian Process')
ax.fill(np.concatenate([X_plot[:, 2], X_plot[:, 2][::-1]]),
        np.concatenate([y_pred[:, 0] - 1.9600 * sigma[:, 0],
                        (y_pred[:, 0] + 1.9600 * sigma[:, 0])[::-1]]),
        alpha=.5, fc='b', ec='None', label='95% confidence interval')
ax.set_xlabel('UUTYaw')
ax.set_ylabel('CLTot')
ax.legend(loc='upper left')
plt.show()
