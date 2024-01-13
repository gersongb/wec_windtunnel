import os
import pandas as pd
import numpy as np
import windtunnel as wt
import team
import pickle

output_folder = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\aeromaps'
input_file = r'Z:\homologation\WT_data\SAUBER-LMGT3\Toyota_E9225\E9225_c01_SessionData_Extern_v008.xlsm'

team_name= 'Toyota'
team_colour= 'brown'

run_number = 21

map_export_path = os.path.join(output_folder, str(run_number) + '.npy')

team_object = team.Team(team_name, team_colour)

# Create aeromap and export:
aeromap_object = wt.Aeromap(input_file, run_number, map_export_path, 0, 0, 0)
aeromap_object.gp_fit()

team_object.set_aeromap(aeromap_object)

team_object_file = open(os.path.join(output_folder, str(run_number) + '.pkl'), 'wb')
pickle.dump(team_object, team_object_file)
team_object_file.close()
print('Team ' + team_object.name + ' saved to file.')




