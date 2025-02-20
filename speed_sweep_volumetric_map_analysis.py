import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

folder = r'Z:\homologation\WT_data\SAUBER-LMH-LMDh\FER 2024'
file_name = 'RunDataLive_E9248_0033.csv'
file_path = os.path.join(folder, file_name)

# read csv file as a dataframe ignoring the first row and using semi-colon as separator:
df = pd.read_csv(file_path, sep=';', skiprows=[0])

# Print the column names:
print(df.columns)

# retain the columns WindSpeed	RoadSpeed	UUTFRh	UUTRRh	UUTYaw	UUTRoll	UUTPitch Cx	Cz	Czf	Czr	Pzf:
columns = ['Time', 'RoadSpeed', 'WindSpeed', 'UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll', 'UUTPitch', 'Cx', 'Cz', 'Czf', 'Czr', 'Pzf']
try:
    df = df[columns]

except:
    # rename the columns removing 'Live_' prefix from the column names:
    df.columns = [col.replace('Live_', '') for col in df.columns]
    df = df[columns]

# Remove the data where the magnitude of the difference between road speed and wind speed is below 2m/s:
df = df[(df['RoadSpeed'] - df['WindSpeed']).abs() < 2]

# Retain only the data with FRH values 45 +- 2%:
#df = df[(df['UUTFRh'] > 45*0.95) & (df['UUTFRh'] < 45*1.05)]

# Retain only the data with RRH values 51 +- 2%:
#df = df[(df['UUTRRh'] > 51*0.95) & (df['UUTRRh'] < 51*1.05)]

# Remove rows where UUTYaw and UUTRoll are not small:
df = df[(df['UUTYaw'].abs() < 0.2) | (df['UUTRoll'].abs() < 0.2)]

# Retain only the data with speeds below 98% of the maximum:
df = df[df['WindSpeed'] < 0.98*df['WindSpeed'].max()]

# Retain only the data with time above 50% of the maximum:
df = df[df['Time'] > 0.5*df['Time'].max()]

# Print the maximum wind speed:
print('Max wind speed:', df['WindSpeed'].max())

# Remove rows with NaN values:
df = df.dropna()

# Create a 3rd order polynomial fit for the data:
poly = np.polyfit(df['WindSpeed'], df['Cx'], 6)
poly_y = np.poly1d(poly)(df['WindSpeed'])

# Plot the raw data and the polynomial fit:
plt.figure()
plt.plot(df['WindSpeed'], df['Cx'], 'ro')
plt.plot(df['WindSpeed'], poly_y, 'b-')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Cx')
plt.title('Cx vs Wind Speed')
plt.grid()
plt.show()
