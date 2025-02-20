import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

folder = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225'
file_name = 'RunDataLive_E9225_0024.csv'
file_path = os.path.join(folder, file_name)

# read csv file as a dataframe ignoring the first row and using semi-colon as separator:
df = pd.read_csv(file_path, sep=';', skiprows=[0])

# retain the columns WindSpeed	RoadSpeed	UUTFRh	UUTRRh	UUTYaw	UUTRoll	UUTPitch Cx	Cz	Czf	Czr	Pzf:
df = df[['WindSpeed', 'UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll', 'Cx', 'Cz', 'Pzf', 'Eff']]

df = df[(df['WindSpeed'] > 44)]

# Remove rows with NaN values:
df = df.dropna()

print(df.head())
print(df.shape)

# Coarsen the data by removing every other row:
df = df.iloc[::20, :]

print(df.shape)

# save df as csv:
df.to_csv(os.path.join(folder, 'coarsened.csv'), index=False)


def gp_fit(wt_data, gp_path):
        # Enforce zero yaw/roll when values are small:
        print('Enforcing zero yaw/roll when values are small')
        wt_data.loc[wt_data['UUTYaw'].abs() < 0.01, 'UUTYaw'] = 0
        wt_data.loc[wt_data['UUTRoll'].abs() < 0.01, 'UUTRoll'] = 0

        # Mirror points where yaw & roll are not zero:
        print('Mirroring points where yaw & roll are not zero')
        temp_df = wt_data
        temp_df = temp_df.drop(temp_df[(temp_df['UUTYaw'] == 0) & (temp_df['UUTRoll'] == 0)].index)
        temp_df['UUTYaw'] = -temp_df['UUTYaw']
        temp_df['UUTRoll'] = -temp_df['UUTRoll']

        wt_data = pd.concat([wt_data, temp_df], axis=0)

        X = wt_data[['UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll']].to_numpy()
        y = wt_data[['Cz', 'Cx', 'Pzf', 'Eff']].to_numpy()
        #y = wt_data[['Cz']].to_numpy()

        # Fit a Gaussian process to the data:
        print('Fitting Gaussian process to the data')
        kernel = C(1.0, (1e-3, 1e3)) * RBF(length_scale=[5, 5, 1, 0.1], length_scale_bounds=(1e-1, 50))
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.05, normalize_y=True, copy_X_train=False) # copy_X_train=False is required to avoid a memory error
        gp.fit(X, y)

        # Save the Gaussian process fit:
        np.save(gp_path, gp)

# Fit a Gaussian process to the data:
gp_fit(df, os.path.join(folder, 'gp_fit.npy'))


