# Author: Gerson Garsed-Brand
# Date: June 2023
# Description: class definitions for WT activities

import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


class WindTunnel:
    def __init__(self, name):
        self.name = name

class Session:
    def __init__(self, name, windtunnel, runs):
        self.name = name
        self.windtunnel = windtunnel
        self.runs = runs

    def add_run(self, run):
        self.runs.append(run)

class Run:
    def __init__(self, number):
        self.number = number

class WeightedData:
    def __init__(self, wt_name, file_path, wt_columns):
        self.wt_name = wt_name
        self.file_path = file_path
        self.wt_columns = wt_columns

    def extract_data(self):
        columns_original = ['RunNumber', 'RunComment', 'Merit_Czf', 'Merit_Czr', 'Merit_Cz', 'Merit_Cx']

        if 'sauber' in self.wt_name.lower():
            # Read the tunnel data and process:
            tunnel_df = pd.read_excel(self.file_path, sheet_name='Alldata', skiprows=[0,1])

            # Retain only the columns of interest:
            tunnel_df = tunnel_df[self.wt_columns]
            tunnel_df.columns = columns_original
            tunnel_df = tunnel_df[tunnel_df['Merit_Cz'].notna()]
            tunnel_df = tunnel_df[tunnel_df['Merit_Cz'].notna()]

            tunnel_df['Merit_Cz'] = round(tunnel_df['Merit_Cz'], 3)
            tunnel_df['Merit_Cx'] = round(tunnel_df['Merit_Cx'], 3)

            tunnel_df['Merit_Pzf'] = 100* tunnel_df['Merit_Czf'] / tunnel_df['Merit_Cz']



            return tunnel_df

        elif 'windshear' in self.wt_name.lower():            
            # Get the run number by splitting the parent folder name with the string 'Run' and taking the last element:
            parent_folder = os.path.dirname(self.file_path)            
            run_number = parent_folder.split('Run')[-1]
            
            # Convertion values:
            PSF_to_Newtons = 47.88125
            LBF_to_Newtons= 4.44822

            # Create weights dataframe:
            weights_homol = pd.DataFrame()
            weights_homol['name'] = ['First','S01','S02','S03','S04','S05','S06','S07','S08','S09','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20','S21','S22','S23','S24']
            weights_homol['Cz'] = [0,0,0,0,1/15,1/15,1/15,1/15, 1/15, 1/15, 1/15, 1/15, 1/15, 1/15, 1/27, 1/27, 1/27, 1/27, 1/27, 1/27, 1/27, 1/27, 1/27, 0, 0]
            weights_homol['Cx'] = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            
            weights_scnd = pd.DataFrame()
            weights_scnd['name'] = ['First','S01','S02','S03','S04','S05','S06']
            weights_scnd['Cz'] = [0.29,0.32,0.025,0.19,0.19,0,0]
            weights_scnd['Cx'] = [0,0,0,0,0,1,0]


            # Open the file:
            f = open(self.file_path, 'r')

            # Remove the first three rows:
            f.readline()
            f.readline()
            f.readline()

            # Convert the rest of the file to a dataframe:
            df = pd.read_csv(f, sep='\t')

            # Remove the first row:
            df = df.iloc[1:]

            # Retain only colums LF, LR, L, D, DYNPR, RRS Speed Feedback and Air Velocity:
            df = df[['LF', 'LR', 'L', 'D', 'DYNPR', 'RRS Speed Feedback', 'Air Velocity', 'YAW']]
                # Convert all values to float:
            df = df.astype(float)

            # Find the tare values:

            hs_drag_tare_133 = df[(df['RRS Speed Feedback'] > 130) & (df['RRS Speed Feedback'] < 135) & (abs(df['Air Velocity']) < 1)].iloc[-1]


            hs_lift_tare_133 = df[(df['RRS Speed Feedback'] < 5) & (abs(df['Air Velocity']) < 1)].iloc[-1]

            # Create a copy of df and retain only the wind on data:
            df_133 = df[(abs(df['Air Velocity']) > 1) & (abs(df['Air Velocity']) < 150)]

            # Subtract the tare values from the wind on data for all columns:
            results = pd.DataFrame()
            results['Merit_Cx'] = (df_133['D']-hs_drag_tare_133['D'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
            results['Merit_Cz'] = (df_133['L']-hs_lift_tare_133['L'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
            results['Merit_Czf'] = (df_133['LF']-hs_lift_tare_133['LF'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
            results['Merit_Czr'] = (df_133['LR']-hs_lift_tare_133['LR'])*LBF_to_Newtons/(df_133['DYNPR']*PSF_to_Newtons)
            results['Air Velocity'] = df_133['Air Velocity']
            results['YAW'] = df_133['YAW']

            # Re-index the dataframe:
            results = results.reset_index(drop=True)

            if len(results) < 15: # short map
                weights = weights_scnd
            else:
                weights = weights_homol

            # Multiply the Cz column by weights['Cz']:
            results['Cz_weighted'] = results['Merit_Cz']*weights['Cz']
            results['Czf_weighted'] = results['Merit_Czf']*weights['Cz']
            results['Czr_weighted'] = results['Merit_Czr']*weights['Cz']

            # Multiply the Cx column by weights['Cx']:
            results['Cx_weighted'] = results['Merit_Cx']*weights['Cx']

            print(results['Cx_weighted'])

            SCz = results['Cz_weighted'].sum()
            SCzf = results['Czf_weighted'].sum()
            SCzr = results['Czr_weighted'].sum()

            results['Cx_weighted'] = results['Cx_weighted'].replace(0, np.nan)
            SCx = results['Cx_weighted'].min()  

            tunnel_df = pd.DataFrame()
            tunnel_df['RunNumber'] = [run_number]
            tunnel_df['RunComment'] = ''
            tunnel_df['Merit_Czf'] = round(SCzf, 3)
            tunnel_df['Merit_Czr'] = round(SCzr, 3)
            tunnel_df['Merit_Cz'] = round(SCz, 3)
            tunnel_df['Merit_Cx'] = round(SCx, 3)
            tunnel_df['Merit_Pzf'] = 100* tunnel_df['Merit_Czf'] / tunnel_df['Merit_Cz']
            return tunnel_df


class Aeromap():
    def __init__(self, wt_import_path, run_number, gp_path, AAD_default, AAD_correction_min, AAD_correction_max, **kwargs):
        self.wt_import_path = wt_import_path
        self.run_number = run_number
        self.AAD_default = AAD_default
        self.AAD_correction_min = np.array(AAD_correction_min)
        self.AAD_correction_max = np.array(AAD_correction_max)
        self.gp_path = gp_path
        super().__init__(**kwargs)

    def gp_fit(self):
        # Load wind tunnel data:
        wt_data = pd.read_excel(self.wt_import_path, sheet_name=self.run_number, skiprows=[0])
        wt_data = wt_data[(wt_data['WindSpeed'] > 45)]

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
        y = wt_data[['Cz', 'Cx', 'Pzf', 'Eff']].to_numpy()

        # Fit a Gaussian process to the data:
        kernel = C(1.0, (1e-3, 1e3)) * RBF(length_scale=[5, 5, 1, 0.1], length_scale_bounds=(1e-1, 50))
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.05, normalize_y=True)
        gp.fit(X, y)

        # Save the Gaussian process fit:
        np.save(self.gp_path, gp)

    def read_gp(self):
        # Load the Gaussian process fit:
        gp = np.load(self.gp_path, allow_pickle=True).item()
        return gp
    
    def get_AAD_corrections(self, AAD): # percentage of AAD (0 is minimum and 1 is maximum), [Cz, Cx, Pzf, Eff] for default, min and max AAD
        if AAD < self.AAD_default:
            # interpolate between default and min
            AAD_corrections = self.AAD_correction_min - self.AAD_correction_min * (AAD / self.AAD_default)  
        elif AAD > self.AAD_default:
            # interpolate between default and max
            AAD_corrections = self.AAD_correction_max*(AAD - self.AAD_default)/(1 - self.AAD_default)        
        else:
            # Create a list of zeros with the same shape as min:
            AAD_corrections = np.zeros_like(self.AAD_correction_min)

        return AAD_corrections


