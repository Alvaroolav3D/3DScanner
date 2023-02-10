import socket
import struct
import subprocess
import os
import picamera

#___________________FUNCTIONS___________________#

def powerOff(): #0
# La funcion powerOff ejecuta en un hilo a parte el comando necesario para apagar la raspberry,
# haciendo el apagado de forma correcta y segura siempre antes de quitar la corriente
    command = "/sbin/shutdown -h now" # comando
    subprocess.Popen(command.split(), stdout=subprocess.PIPE) #abro un subproceso nuevo para ejecutar la funcion
    return "Rebooting"

def takePhoto(): #1
# hace una foto con el nombre elegido desde el servidor y lo almacena en el directorio definido
# en este script

    filename = data[1]
    print ("File name: " + filename)

    savePath = "/home/pi/Desktop/3DScanner/Client/Pictures/"+filename
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    print ("shooting")
    camera.capture(savePath + filename,'png')
    
    #envio la imagen al servidor aqui
    
    return "Took picture"

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

    return "Done. Now you have Python"

def default():
# opcion que sirve para dejar constancia de que el comando utilizado no existe
    return "Incorrect command"

switcher = {
    0: powerOff,
    1: takePhoto,
    2: installPython3,
    }

def switch(server_command):
    return switcher.get(server_command, default)()

#___________________CODE___________________#

# CONSTANT VARIABLES

MULTICAST_CAMERA_GRP = '225.1.1.1' #grupo de direccion multicast
MULTICAST_CAMERA_PORT = 3179
BUFFER_SIZE = 10240

# CONECTION WITH THE SERVER

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', MULTICAST_CAMERA_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_CAMERA_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print ()
print ("3D Scanner - Socket listening")
print ()

# WAITING SERVER COMMANDS

with picamera.PiCamera() as camera:
    
    print ("Camera setup, waiting for command\n")
    
    while True:
        #newdata = s.recv(BUFFER_SIZE)
        newdata, address = s.recvfrom(BUFFER_SIZE)
        sender_ip = address[0]
        print ("Got new data from the server")
        data2 = newdata.decode()
        data = newdata.decode().split()
        print("Data decoded")
        
        cmd = int(data[0])
        print ("Received cmd: " + data[0] + " from: " + sender_ip)
        
        print(switch(cmd))
        print()