import os
import shutil
import platform
import time

scanner_Devices = [
#     00    01    02    03    04
#     05    06    07    08    09
    ['10', '11', '12', '13', '14'], #1B
    ['15', '16', '17', '18'], #1A
    ['20', '21', '22', '23'], #2B
    ['25', '26', '27', '28'], #2A
    ['30', '31', '32', '33'], #3B
    ['35', '36', '37', '38'], #3A
    ['40', '41', '42', '43'], #4B
    ['45', '46', '47', '48', '49'], #4A
    ['50', '51', '52', '53', '54'], #5A
    ['60', '61', '62', '63', '64'], #6B
    ['65', '66', '67', '68'], #6A
    ['70', '71', '72', '73'], #7B
    ['75', '76', '77', '78'], #7A
    ['80', '81', '82', '83'], #8B
]

# Path of the directory you want to copy
source_path = ''
if platform.system() == 'Windows':
    print("windows server")
    source_path = r'c:/Users/Alvaro/OneDrive - Universidad Rey Juan Carlos/Escritorio/3DScanner/Client'
elif platform.system() == 'Linux':
    print("Linux server")
    source_path = '/path/to/directory/to/copy'

for column in scanner_Devices:
    for ip in column:
        # Format the destination path with the current IP address
        destination_path = ''
        if platform.system() == 'Windows':
            destination_path = fr'\\192.168.1.{ip}\scanner'
        elif platform.system() == 'Linux':
            destination_path = f'/mnt/192.168.1.{ip}/scanner'

        # Check if the directory already exists in the destination path
        if os.path.exists(os.path.join(destination_path, os.path.basename(source_path))):
            # If it already exists, replace it
            shutil.rmtree(os.path.join(destination_path, os.path.basename(source_path)))
            #time.sleep(1)
            shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
            print(f"La {ip} se ha copiado correctamente: Existe")
        else:
            # If it doesn't exist, paste it
            print(f"La {ip} se ha copiado correctamente: No existe")
            shutil.copytree(source_path, os.path.join(destination_path, os.path.basename(source_path)))
