import os
import shutil


source = r'Y:'

target = r'Z:\homologation\WT_data\WINDSHEAR-LMH-LMDh\ASTON_MARTIN-2024\Raw_Data'

# Scan the source folder for all files and folders:
for root, dirs, files in os.walk(source):
    for file in files:
        if file.endswith('D1.asc') or file.endswith('D2.asc'):
            # Get the name of the parent folder:
            parent_folder = os.path.basename(root)

            # Create the target folder:
            target_folder = os.path.join(target, parent_folder)

            # Create the target folder if it doesn't exist:
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # Copy the file to the target folder:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_folder, file)

            # Copy the file:
            print('Copying file: ' + source_file + ' to ' + target_file)
            shutil.copy(source_file, target_file)

