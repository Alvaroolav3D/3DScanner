import socket

#___________________CODE___________________#

# METHODS

def get_device_ip():
# conecto con un servidor DNS de google que siempre esta activo 
# para comprobar simplemente cual es la ip de mi dispositivo

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    device_ip = s.getsockname()[0]
    s.close()
    return device_ip

# CONSTANT VARIABLES

MULTICAST_CAMERA_GRP = '225.1.1.1' #grupo de direccion multicast
MULTICAST_CAMERA_PORT = 3179
BUFFER_SIZE = 10240

print(
    "\nControl commands:\n" +
    "Press 0 to poweroff the raspberries\n" +
    "Press 1 to takePhoto\n" + 
    "Press 2 to install or update Python3\n" +
    "Press 3 to synchronize_time with the server\n" +
    "If you press another key, try again\n"
    )



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

while True:
    cmd = input("Command: ")
    print("")

    if (cmd == "-1"):
        sock.close()
        break

    if (cmd == "0"):
        # data[0] seria el comando cmd

        data = cmd
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GRP, MULTICAST_CAMERA_PORT))

    if (cmd == "1"):
        # data[0] seria el comando cmd
        # data[1] seria el nombre imagen

        fileName = input("File name: ")

        data = cmd + " " + fileName
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GRP, MULTICAST_CAMERA_PORT))

    if (cmd == "2"):
        # data[0] seria el comando cmd

        data = cmd
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GRP, MULTICAST_CAMERA_PORT))

    if (cmd == "3"):
        # data[0] seria el comando cmd
        # data[1] seria la ip de este dispositivo

        serverIP = get_device_ip()

        data = cmd + " " + serverIP
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GRP, MULTICAST_CAMERA_PORT))