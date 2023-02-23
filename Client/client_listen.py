import socket
import struct
import subprocess
import os
import ntplib
import time
from datetime import datetime
import picamera

#___________________FUNCTIONS___________________#

def powerOff(): #0
# The powerOff function executes in a separate thread the command needed to turn off the raspberry,
# doing the shutdown correctly and safely always before removing the power.

    option = data[1]
    print ("Option: " + option)

    if(option == "0"):
        os.system("sudo poweroff") # command
        return "Power Off"

    elif(option == "1"):
        os.system("sudo reboot") # command
        return "Rebooting"

def systemUpdate(): #1
# Checks for available system updates and proceeds to upgrade them

    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"])
    return "Upgrade completed"

def installPython3(): #2
    # Check if Python is already installed
    try:
        result = subprocess.run(["python3", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Get the version of Python installed
        version = os.sys.version_info[:3]
        version_str = ".".join(str(x) for x in version)
        print("Python version:", version_str)
        
    except FileNotFoundError:
        print("Python is not installed. Installing latest version...")
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3"])
        os.sys.exit()

    # Update to the latest version of Python
    print("Updating Python to the latest version...")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3"])

    return "Done. Now you have Python updated"

def synchronizeTime():

    ntp_client = ntplib.NTPClient()

    # Get the current time on the Raspberry Pi
    pi_time_before_sync = time.time()

    try:
        response = ntp_client.request(SENDER_IP, version=3)
        # Get the current time from the NTP server
        ntp_time = response.tx_time
        # Convert the NTP time to a readable format
        current_time = datetime.fromtimestamp(ntp_time)
        # Set the system time to the current time
        
        os.system('sudo date --set="%s"' % current_time.strftime('%Y-%m-%d %H:%M:%S'))
        print("Time synchronized with NTP server:", SENDER_IP)

        # Get the current time on your laptop
        laptop_time_after_sync = time.time()

        # Calculate the time difference between the Raspberry Pi and your laptop
        time_diff = laptop_time_after_sync - pi_time_before_sync
        print("Time difference between Raspberry Pi and laptop:", time_diff, "seconds")
    except Exception as e:
        print("Error syncing time with NTP server:", e)

    return "Synchronized"

def takePhoto(): #4
# takes a picture with the chosen name from the server and stores it in the defined directory
# in this script

    fileName = data[1]
    print ("File name: " + fileName)

    # Create a folder with the file name. Useful if I want to take several photos with different
    # lighting and save them under the same sorted name.
    savePath = "/home/pi/Desktop/3DScanner/Client/Pictures/" + fileName + "/"
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # Currently I only keep one photo
    print ("shooting")
    camera.capture(savePath + fileName,'png')
    print("Took picture")

    # Send the image to the server
    send_socket = socket.socket()
    send_socket.connect((SENDER_IP, IMAGE_TRANSFER_PORT))

    with open(savePath + fileName, 'rb') as image:
        
        image_data = image.read()
        send_socket.sendall(image_data)
    
    send_socket.close()
    
    return "Sent picture to: " + SENDER_IP

def checkListening(): #5
    # Send message to the server

    message =b"yes"

    send_socket = socket.socket()
    send_socket.connect((SENDER_IP, IMAGE_TRANSFER_PORT))
    send_socket.send(message)

    send_socket.close()
    return "Done."

def default():
# option used to record that the used command does not exist
    return "Incorrect command"

switcher = {
    0: powerOff, # Press 0 to poweroff or reboot the raspberries
    1: systemUpdate, # Press 1 to update the system of the raspberries
    2: installPython3, # Press 2 to install or update Python3
    3: synchronizeTime, # Press 3 to synchronize_time with the server
    4: takePhoto, # Press 4 to take a picture
    5: checkListening, # Press 5 to check what raspberries are listening
    
    # If you press another key, try again
    }

def switch(server_command):
    return switcher.get(server_command, default)()

#___________________CODE___________________#

# CONSTANT VARIABLES

MULTICAST_CAMERA_GROUP = '225.1.1.1' # Multicast camera address that listens for commands from the server
MULTICAST_COMMAND_PORT = 3179 # Port that it opens to receive the datagrams with the commands from the server
IMAGE_TRANSFER_PORT = 5001 # Port used to send the images to the server once they have been made
BUFFER_SIZE = 10240 # Size of the buffer used in passing messages through the socket

# MAIN

# Conection with the server
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
cmd_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cmd_socket.bind(('', MULTICAST_COMMAND_PORT))
multicastStruct = struct.pack("4sl", socket.inet_aton(MULTICAST_CAMERA_GROUP), socket.INADDR_ANY)
cmd_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicastStruct)

print ("\n3D Scanner - Socket listening\n")

# Listening loop

with picamera.PiCamera() as camera:
    
    print ("Camera setup, waiting for command\n")
    
    while True:
        newdata, address = cmd_socket.recvfrom(BUFFER_SIZE)
        SENDER_IP = address[0]
        print ("Got new data from the server")
        data = newdata.decode().split()
        print("Data decoded")
        
        cmd = int(data[0])
        print ("Received cmd: " + data[0] + " from: " + SENDER_IP)
        
        print(switch(cmd))
        print()