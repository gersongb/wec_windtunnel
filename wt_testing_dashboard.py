import os

import pandas as pd
import streamlit as st
import plotly.express as px

import windtunnel as wt

wt_name = 'Sauber'
#wt_name = 'Windshear'

data_folder = r'Z:\homologation\WT_data\SAUBER-LMH-LMDh\POR 2024\Processed_Data'
input_file = r'Z:\homologation\WT_data\SAUBER-LMH-LMDh\POR 2024\E9267_c01_SessionData_Extern_v008.xlsm'

input_folder = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024\Raw_Data'
windshear_meta = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024\Windshear_Meta'

wt_columns = ['RunNumber', 'RunComment', 'Merit_Czf', 'Merit_Czr', 'Merit_Cz', 'Merit_Cx']

run_number_status = 0
run_type_status = 0
dCx_status = 0.0
dCz_status = 0.0
data_file_status = ''

if 'sauber' in wt_name.lower():
    window_pd = pd.DataFrame({
        'Cx': [1.040, 1.040, 1.024, 0.98, 1.040],
        'Cz': [4.048, 4.230, 4.230, 4.048, 4.048]
    })
    
elif 'windshear' in wt_name.lower():
    window_pd = pd.DataFrame({
        'Cx': [0.954, 1.014, 1.014, 0.999, 0.954],
        'Cz': [3.965, 3.965, 4.145, 4.145, 3.965]
    })

# Braking window Sauber LMH:
blanking_dx = 0.01
blanking_dz = 0.035



# Homologation window Sauber LMGT3:
#window_pd = pd.DataFrame({
#    'Cx': [1.107, 1.161, 1.308, 1.255, 1.107],
#    'Cz': [2.850, 3.245, 3.357, 2.962, 2.850]
#})

# Braking window Sauber LMGT3:
#blanking_dx = 0.01
#blanking_dz = 0.05

#  Create a dictionary of colours for the plotly graph:
colours = {
    'window': 'black',
    'homologation': 'blue',
    'testing_long': 'red',
    'testing_short': 'orange',
    'blanking': 'green'
}

# Define columns:
columns_new = ['RunNumber', 'RunComment', 'Cz', 'Cx', 'Type', 'dCx', 'dCz']
columns_original = ['RunNumber', 'RunComment', 'Merit_Czf', 'Merit_Czr', 'Merit_Cz', 'Merit_Cx']

# Create a dashboard using streamlit:
st.set_page_config(page_title='Wind Tunnel Homologation Dashboard', layout='wide')

# Print the title with font size:
st.title('Wind Tunnel Homologation Dashboard')
st.markdown('<style>h1{font-size: 30px;}</style>', unsafe_allow_html=True)

# Print side bar title:
st.sidebar.title('Tunnel Data')

# Add a button called refresh data to the sidebar:
refresh_data = st.sidebar.button('Refresh Data')

if 'sauber' in wt_name.lower():
    tunnel_pd = wt.WeightedData(wt_name, input_file, wt_columns).extract_data()

    if refresh_data:
        tunnel_pd = wt.WeightedData(wt_name, input_file, wt_columns).extract_data()


elif 'windshear' in wt_name.lower():
    # Read the windshear meta data:
    runs_to_ignore_df = pd.read_csv(os.path.join(windshear_meta, 'Runs_To_Ignore.csv'))

    runs_description_df = pd.read_csv(os.path.join(windshear_meta, 'Runs_Description.csv'))
    print(runs_description_df)

    # List the folders in the input_folder:
    folders = os.listdir(input_folder) 

    # Remove the items that are not folders:
    folders = [folder for folder in folders if os.path.isdir(os.path.join(input_folder, folder))]

    # Loop through the folders:
    # Create a new dataframe for the tunnel data with the columns in columns_original and the addition of Merit_Pzf column:
    tunnel_pd = pd.DataFrame(columns=columns_original + ['Merit_Pzf'])

    for folder in folders:
        # Get the path to the D1 file:
        folder_path = os.path.join(input_folder, folder)   
        d1_path = os.path.join(folder_path, 'D1.asc')
          
        run_number = folder_path.split('Run')[-1]

        ignore_flag = False
        for ignore in runs_to_ignore_df['ignore']:
            if ignore == int(run_number):
                ignore_flag = True


        # if file exists, extract the data:
        if os.path.isfile(d1_path) & ignore_flag == False:
            print('Extracting data for ' + run_number)
            run_pd = wt.WeightedData(wt_name, d1_path, wt_columns).extract_data()

            # Check if the run has a description:
            has_description = False
            for run in runs_description_df['run']:
                if run == int(run_number):
                    has_description = True

            if has_description:
                temp_df = runs_description_df[runs_description_df['run'] == int(run_number)]
                description = temp_df['description'].values[0]
                run_pd['RunComment'] = description
                print(description)

            # Concatenate the run_pd dataframe to the tunnel_pd dataframe, merging headers:
            tunnel_pd = pd.concat([tunnel_pd, run_pd], axis=0, ignore_index=True)

# Show the tunnel data:
st.sidebar.dataframe(tunnel_pd)

# Add an interactive widget to the sidebar to select the run number, with a default value of status, show the runs in inverse order:
run_number = st.sidebar.selectbox('Run Number', tunnel_pd['RunNumber'].unique().tolist()[::-1], index=run_number_status)

# Add drop down menus to select run type:
run_type = st.sidebar.selectbox('Run Type', ['Not Required', 'Testing Short', 'Testing Long', 'Testing Long AAD', 
                                             'Homologation', 'Homologation_Ref', 'Blanking'], index=run_type_status)

# Add fiels for dCx and dCz:
dCx = st.sidebar.number_input('dCx', value=dCx_status, format='%.3f')
dCz = st.sidebar.number_input('dCz', value=dCz_status, format='%.3f')

# Add a button to save the data:
save_data = st.sidebar.button('Save Data')

# When the button is pressed, add the selected data to the processed_pd dataframe:
if save_data:
    # Get data from tunnel_pd mathcing the selected run number:
    run_pd = tunnel_pd[tunnel_pd['RunNumber'] == run_number]

    data = [run_pd['RunNumber'].values[0], run_pd['RunComment'].values[0], -run_pd['Merit_Cz'].values[0], run_pd['Merit_Cx'].values[0], 
            run_type, dCx, dCz]
    
    # Add the data to the processed_pd dataframe:
    temp_pd = pd.DataFrame([data], columns=columns_new)
    
    # Save the temp_dp dataframe as a csv file with run number as name:
    temp_pd.to_csv(os.path.join(data_folder, str(run_number) + '.csv'), index=False)

    # Set the statuses:
    run_number_status = tunnel_pd['RunNumber'].unique().tolist().index(run_number)
    run_type_status = ['Not Required', 'Testing Short', 'Testing Long', 'Testing Long AAD', 'Homologation', 'Homologation_Ref', 'Blanking'].index(run_type)
    dCx_status = dCx
    dCz_status = dCz


# Create a dataframe containing all the files in the data folder:
processed_pd = pd.DataFrame(columns=columns_new)
for file in os.listdir(data_folder):
    if file.endswith('.csv'):
        temp_pd = pd.read_csv(os.path.join(data_folder, file))

        if temp_pd['Type'].values[0] != 'Not Required':
            processed_pd = pd.concat([processed_pd, temp_pd])


# Correct the Cz and Cx values for the dCx and dCz values:
processed_pd['Cz'] = processed_pd['Cz'] + processed_pd['dCz']
processed_pd['Cx'] = processed_pd['Cx'] + processed_pd['dCx']

st.dataframe(processed_pd)

# Create secondary dataframe containing each run type:
homologation_pd = processed_pd[processed_pd['Type'] == 'Homologation']
testing_short_pd = processed_pd[processed_pd['Type'] == 'Testing Short']
testing_long_pd = processed_pd[processed_pd['Type'] == 'Testing Long']
testing_long_AAD_pd = processed_pd[processed_pd['Type'] == 'Testing Long AAD']
blanking_pd = processed_pd[processed_pd['Type'] == 'Blanking']

# Concatenate the homologation_ref_pd dataframe to the homologation_pd dataframe:
homologation_ref_pd = processed_pd[processed_pd['Type'] == 'Homologation_Ref']
homologation_pd = pd.concat([homologation_pd, homologation_ref_pd])


# sort each dataframe by Cz:
homologation_pd = homologation_pd.sort_values(by=['Cz'])
testing_short_pd = testing_short_pd.sort_values(by=['Cz'])
testing_long_pd = testing_long_pd.sort_values(by=['Cz'])
blanking_pd = blanking_pd.sort_values(by=['Cz'])
testing_long_AAD_pd = testing_long_AAD_pd.sort_values(by=['Cz'])

# Create a plotly line graph with the window_pd data in pairs of Cx and Cz::
fig = px.line(window_pd, x='Cx', y='Cz', color_discrete_sequence=[colours['window']])

# Add the homologation data to the plotly graph as a line plot with points:
fig.add_scatter(x=homologation_pd['Cx'], y=homologation_pd['Cz'], mode='lines+markers', marker_color=colours['homologation'], name='Homologation')

# Add the testing data to the plotly graph:
fig.add_scatter(x=testing_short_pd['Cx'], y=testing_short_pd['Cz'], mode='markers', marker_color=colours['testing_short'], name='Testing Short')
fig.add_scatter(x=testing_long_pd['Cx'], y=testing_long_pd['Cz'], mode='markers', marker_color=colours['testing_long'], name='Testing Long')
fig.add_scatter(x=testing_long_AAD_pd['Cx'], y=testing_long_AAD_pd['Cz'], mode='lines+markers', marker_color=colours['testing_long'], name='Testing Long AAD')

# Add the blanking data to the plotly graph:
fig.add_scatter(x=blanking_pd['Cx'], y=blanking_pd['Cz'], mode='markers', marker_color=colours['blanking'], name='Blanking')

# For each homologation_ref, create a box around the blanking data using dotted lines and the blanking dx and dz values:
for index, row in homologation_ref_pd.iterrows():
    fig.add_shape(type='rect', 
                  x0=row['Cx'] - blanking_dx, 
                  y0=row['Cz'] - blanking_dz, 
                  x1=row['Cx'] + blanking_dx, 
                  y1=row['Cz'] + blanking_dz, 
                  line=dict(
                      color=colours['blanking'], 
                      width=1, 
                      dash='dash'
                    ), 
                    fillcolor=colours['blanking'], 
                    opacity=0.1)




# Set the x and y axis range to be 0.01 smaller and bigger than the data:
fig.update_xaxes(range=[window_pd['Cx'].min() - 0.01, window_pd['Cx'].max() + 0.01])
fig.update_yaxes(range=[window_pd['Cz'].min() - 0.01, window_pd['Cz'].max() + 0.01])

# Set the axis names to match the dataframe:
fig.update_xaxes(title_text='Cx')
fig.update_yaxes(title_text='Cz')

# Increase the font size of the axis titles:
fig.update_xaxes(title_font_size=20)
fig.update_yaxes(title_font_size=20)

# Increase the font size of the axis ticks:
fig.update_xaxes(tickfont_size=15)
fig.update_yaxes(tickfont_size=15)


st.plotly_chart(fig)
