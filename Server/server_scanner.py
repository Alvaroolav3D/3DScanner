import socket
import json
import sys

#___________________CODE___________________#

# CONSTANT VARIABLES

MULTICAST_CAMERA_GRP = '225.1.1.1' #grupo de direccion multicast
MULTICAST_CAMERA_PORT = 3179
BUFFER_SIZE = 10240

print(
    "\nControl commands:\n" +
    "Press 0 to poweroff the raspberries\n" +
    "Press 1 to takePhoto\n" + 
    "Press 2 to install or update Python3\n" +
    "If you press another key, try again\n"
    )



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

while True:
    cmd = input("Command: ")
    print("")

    if (cmd == "0"):
        # data[0] seria el comando cmd

        data = cmd
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GRP, MULTICAST_CAMERA_PORT))
        #sock.close()

    if (cmd == "1"):
        # data[0] seria el comando cmd
        # data[1] seria el nombre imagen

        fileName = input("File name: ")

        data = cmd + " " + fileName
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GRP, MULTICAST_CAMERA_PORT))
        #sock.close()

    if (cmd == "2"):
        # data[0] seria el comando cmd

        data = cmd
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GRP, MULTICAST_CAMERA_PORT))
        #sock.close()