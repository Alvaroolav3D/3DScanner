import socket
import struct
import os
import time
from datetime import datetime

#___________________FUNCTIONS___________________#

def projectPattern():

    img_files = ['/home/pi/Desktop/3DScanner/Client/img1.png', '/home/pi/Desktop/3DScanner/Client/img2.png']
    display_time = 1  # segundos

    option = data[1]
    print ("Option: " + option)

    os.system(f"sudo fbi -a --noverbose --vt 1 {img_files[int(option)]}")
    time.sleep(display_time)
    os.system(f"sudo fbi -a --noverbose --vt 1 /home/pi/Desktop/3DScanner/Client/black.png") #pantalla en negro

    return "Projected"

def checkListening(): #5
    # Send message to the server

    message =b""
    send_socket = socket.socket()
    send_socket.connect((SENDER_IP, MESSAGE_TRANSFER_PORT))
    send_socket.send(message)
    send_socket.close()
    
    return "Done."


def default():
# option used to record that the used command does not exist
    return "Incorrect command"

switcher = {
    6: projectPattern, # Press 0 to project the Pattern
    5: checkListening, # Press 5 to check what raspberries are listening

    # If you press another key, try again
    }

def switch(server_command):
    return switcher.get(server_command, default)()

#___________________CODE___________________#

# CONSTANT VARIABLES

MULTICAST_PROJECTOR_GROUP = '225.1.1.2' # Multicast projector address that listens for commands from the server
MULTICAST_COMMAND_PORT = 3179 # Port that it opens to receive the datagrams with the commands from the server

MESSAGE_TRANSFER_PORT = 5001 # Port used to send the images to the server once they have been made
BUFFER_SIZE = 10240 # Size of the buffer used in passing messages through the socket

# MAIN

# Conection with the server
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
cmd_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cmd_socket.bind(('', MULTICAST_COMMAND_PORT))
multicastStruct = struct.pack("4sl", socket.inet_aton(MULTICAST_PROJECTOR_GROUP), socket.INADDR_ANY)
cmd_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicastStruct)

print ("\n3D Scanner - Socket listening\n")

# Listening loop

print ("Projector setup, waiting for command\n")

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