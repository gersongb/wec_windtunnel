import pandas as pd
import matplotlib.pyplot as plt




# Create a dictionary of the teams and their respective data:
teams = {
    'Toyota': {
        'name': 'Toyota',
        'cars': {7, 8},
        'colour': 'brown',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\Toyota 2023\E9175_SessionData_Extern_v004.xlsm',
        'sensitivity_run': '029',
        'AAD_default': 0.667, # default AAD position as a percentage
        'AAD_min_correction': [+0.09, -0.027, +1.29], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.05, +0.010, -0.46], # correction at 100% AAD position
        'speed_sweep': ['S60', 'S61', 'S62']
    }, 
    'Ferrari 2023': {
        'name': 'Ferrari 2023',
        'cars': {50, 51, 83},
        'colour': 'red',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\FER 2023\E9163_SessionData_Extern_v004.xlsx',
        'sensitivity_run': '036',
        'AAD_default': 0.235, # default AAD position as a percentage
        'AAD_min_correction': [+0.053, -0.012, +0.049], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.140, +0.033, -1.846], # correction at 100% AAD position
        'speed_sweep': ['S59', 'S60', 'S61']
    },
    'Porsche': {
        'name': 'Porsche',
        'cars': {5, 6, 12, 38, 99},
        'colour': 'black',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\POR\E9167_SessionData_Extern_v004 (3).xlsx',
        'sensitivity_run': '035',
        'AAD_default': 0.2, # default AAD position as a percentage
        'AAD_min_correction': [+0.09, -0.027, +1.29], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.05, +0.010, -0.46], # correction at 100% AAD position
        'speed_sweep': ['S50', 'S51', 'Last']
    },
    'Cadillac': {
        'name': 'Cadillac',
        'cars': {2, 3},
        'colour': 'yellow', 
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\CAD\E9172_SessionData_Extern_v004.xlsx',
        'sensitivity_run': '032',
        'AAD_default': 0.3, # default AAD position as a percentage
        'AAD_min_correction': [+0.025, -0.002, -1.779], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.016, +0.024, 1.525], # correction at 100% AAD position
        'speed_sweep': ['S60', 'S61', 'S62']
    },
    'Peugeot': {
        'name': 'Peugeot',
        'cars': {93, 94},
        'colour': 'grey',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\PEU 2023\E9184_SessionData_Extern_v004.xlsx',
        'sensitivity_run': '038',
         'AAD_default': 0.444, # default AAD position as a percentage
        'AAD_min_correction': [+0.03, +0.004, -1.297], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [+0.025, +0.002, +0.802], # correction at 100% AAD position
        'speed_sweep': ['S58', 'S59', 'S60']
    },
    'Alpine': {
        'name': 'Alpine',
        'cars': {35, 36},
        'colour': 'blue',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\Alpine 2023\E9216_c01_SessionData_Extern_v008.xlsm',
        'sensitivity_run': '033',
         'AAD_default': 1.00, # default AAD position as a percentage
        'AAD_min_correction': [0.148, -0.034, +2.1], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [0, 0, 0], # correction at 100% AAD position
        'speed_sweep': ['S59', 'S60', 'S61']
    },
    'BMW': {
        'name': 'BMW',
        'cars': {15, 20},
        'colour': 'cyan',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\BMW 2023\E9212_c01_SessionData_Extern_v008.xlsm',
        'sensitivity_run': '031',
         'AAD_default': 0.287, # default AAD position as a percentage
        'AAD_min_correction': [0.035, -0.008, -0.57], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.086, 0.020, 1.38], # correction at 100% AAD position
        'speed_sweep': ['S59', 'S60', 'S61']
    },
    'Lamborghini': {
        'name': 'Lamborghini',
        'cars': {63},
        'colour': 'green',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\Lambo 2024\E9202_c01_SessionData_Extern_v008.xlsm',
        'sensitivity_run': '028',
         'AAD_default': 0.77, # default AAD position as a percentage
        'AAD_min_correction': [0.079, -0.013, -1.05], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.024, 0.004, -0.306], # correction at 100% AAD position
        'speed_sweep': ['S59', 'S60', 'S61']
    },
    'IF': {
        'name': 'IF',
        'cars': {11},
        'colour': 'magenta',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\IF\E9229_c01_SessionData_Extern_v008.xlsm',
        'sensitivity_run': '025',
         'AAD_default': 0.73, # default AAD position as a percentage
        'AAD_min_correction': [0.122, -0.029, 1.93], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.045, 0.011, -0.686], # correction at 100% AAD position
        'speed_sweep': ['S59', 'S60', 'S61']
    },
        'Ferrari 2024': {
        'name': 'Ferrari 2024',
        'cars': {50, 51, 83},
        'colour': 'orange',  
        'wt_file': 'Z:\homologation\WT_data\SAUBER-LMH-LMDh\FER 2024\E9248_c01_SessionData_Extern_v008.xlsm',
        'sensitivity_run': '032',
        'AAD_default': 0.235, # default AAD position as a percentage
        'AAD_min_correction': [+0.053, -0.012, +0.049], # correction at 0% AAD position for Cz, Cx and AB, Eff to be computed at the destination
        'AAD_max_correction': [-0.140, +0.033, -1.846], # correction at 100% AAD position
        'speed_sweep': ['S60', 'S61', 'S62']
    },
}

# Create a list of the target columns:
target_columns = ['StepName', 'WindSpeed', 'RoadSpeed', 'UUTFRh', 'UUTRRh', 'UUTYaw', 'UUTRoll', 'UUTPitch',
                    'Cx', 'Cz', 'Czf', 'Czr', 'Pzf', 'Eff']

# Create a figure with 3 subplots named 'Cx', 'Cz' and 'AB':
fig, axs = plt.subplots(1, 5, figsize=(15, 5))
fig.suptitle('Speed Sweep Sensitivity Check', fontsize=16)
fig.tight_layout(pad=3.0)
fig.subplots_adjust(top=0.9)

# Loop through the teams, read the excel file on the specified sheet and skip the first row:
for team in teams:
    print('Processing team ' + team + '...')
    wt_file = teams[team]['wt_file']
    sensitivity_run = teams[team]['sensitivity_run']
    wt_data = pd.read_excel(wt_file, sheet_name=sensitivity_run, skiprows=[0])
    wt_data.rows = wt_data.iloc[0]
    wt_data = wt_data[2:]



    # Filter the data to retain only the target columns:
    wt_data = wt_data[target_columns]
    wt_data = wt_data.dropna(axis='rows')

    # retain the data only from the speed sweep:
    wt_data = wt_data[wt_data['StepName'].isin(teams[team]['speed_sweep'])]

    # Sort the data based on the 'WindSpeed' column:
    wt_data = wt_data.sort_values(by='WindSpeed')

    # Add plots Cx, Cz and AB versus windspeed plots to the figure, using the team colour:
    axs[0].plot(wt_data['WindSpeed'], wt_data['Cx'], label=team, color=teams[team]['colour'])
    axs[1].plot(wt_data['WindSpeed'], wt_data['Czf'], label=team, color=teams[team]['colour'])
    axs[2].plot(wt_data['WindSpeed'], wt_data['Czr'], label=team, color=teams[team]['colour'])
    axs[3].plot(wt_data['WindSpeed'], wt_data['UUTFRh'], label=team, color=teams[team]['colour'])
    axs[4].plot(wt_data['WindSpeed'], wt_data['UUTRRh'], label=team, color=teams[team]['colour'])

# Add labels and legends to the plots:
axs[0].set_title('Cx vs WindSpeed')
axs[0].set_xlabel('WindSpeed')
axs[0].set_ylabel('Cx')
axs[0].legend(loc='upper left')

axs[1].set_title('Czf vs WindSpeed')
axs[1].set_xlabel('WindSpeed')
axs[1].set_ylabel('Czf')
axs[1].legend(loc='upper left')

axs[2].set_title('Czr vs WindSpeed')
axs[2].set_xlabel('WindSpeed')
axs[2].set_ylabel('Czr')
axs[2].legend(loc='upper left')

axs[3].set_title('FRH vs WindSpeed')
axs[3].set_xlabel('WindSpeed')
axs[3].set_ylabel('FRH')
axs[3].legend(loc='upper left')

axs[4].set_title('RRH vs WindSpeed')
axs[4].set_xlabel('WindSpeed')
axs[4].set_ylabel('RRH')
axs[4].legend(loc='upper left')

plt.show()