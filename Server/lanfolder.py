import os
import shutil
import platform

# Path of the directory you want to copy
source_path = ''
if platform.system() == 'Windows':
    print("windows")
    source_path = r'c:/Users/Alvaro/OneDrive - Universidad Rey Juan Carlos/Escritorio/3DScanner/Prueba'
elif platform.system() == 'Linux':
    source_path = '/path/to/directory/to/copy'

# Format the destination path with the current IP address
destination_path = ''
if platform.system() == 'Windows':
    destination_path = r'\\192.168.1.10\scanner'
elif platform.system() == 'Linux':
    destination_path = '/mnt/192.168.1.10/scanner'

# Check if the directory already exists in the destination path
if os.path.exists(os.path.join(destination_path, os.path.basename(source_path))):
    # If it already exists, replace it
    shutil.rmtree(os.path.join(destination_path, os.path.basename(source_path)))
    shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
else:
    # If it doesn't exist, paste it
    shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
