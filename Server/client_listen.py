import socket
import struct
import subprocess
import os
import picamera

#___________________FUNCTIONS___________________#

def restart():
# La funcion restart ejecuta en un hilo a parte el comando necesario para apagar la raspberry,
# haciendo el apagado de forma correcta y segura siempre antes de quitar la corriente
    command = "/sbin/shutdown -r now" # comando
    subprocess.Popen(command.split(), stdout=subprocess.PIPE) #abro un subproceso nuevo para ejecutar la funcion
    return "Rebooting"

def takePhoto():
# hace una foto con el nombre elegido desde el servidor y lo almacena en el directorio definido
# en este script
    print ("shooting")
    camera.capture(savePath + data[3],'png')
    return "Took picture"

def default():
# opcion que sirve para dejar constancia de que el comando utilizado no existe
    return "Incorrect command"

switcher = {
    0: restart,
    1: takePhoto,
    }

def switch(server_command):
    return switcher.get(server_command, default)()

#___________________CODE___________________#

# CONSTANT VARIABLES

MULTICAST_CAMERA_GRP = '225.1.1.1' #grupo de direccion multicast
MULTICAST_CAMERA_PORT = 3179
BUFFER_SIZE = 10240

# CONECTION WITH THE SERVER

name = socket.getfqdn() #name of the local device

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', MULTICAST_CAMERA_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_CAMERA_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print (" ")
print ("3D Scanner - Socket listening")
print (" ")

savePath = "/home/pi/Desktop/pruebas/3DScanner/Try/Pictures"
if not os.path.exists(savePath):
    os.makedirs(savePath)

# WAITING SERVER COMMANDS

with picamera.PiCamera() as camera:
    
    print ("Camera setup, waiting for command\n")
    
    while True:
        newdata = s.recv(BUFFER_SIZE)
        print ("Got new data from the server")
        data = newdata.decode().split()
        print("Data decoded")
        
        print("Full data message: " + data)
        
        cmd = data[0]
        filename = data[1]

        print ("Received cmd: "+ data[0])
        print ("Data: " + data[1])
        print ("File name: " + data[2])

        print(switch(cmd))