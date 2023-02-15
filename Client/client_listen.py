import socket
import struct
import subprocess
import os
import picamera

#___________________FUNCTIONS___________________#

def powerOff(): #0
# La funcion powerOff ejecuta en un hilo a parte el comando necesario para apagar la raspberry,
# haciendo el apagado de forma correcta y segura siempre antes de quitar la corriente
    option = data[1]
    print ("Option: " + option)

    if(option == "0"):
        os.system("sudo poweroff") # comando
        return "Power Off"

    elif(option == "1"):
        os.system("sudo reboot") # comando
        return "Rebooting"
    
    #subprocess.Popen(command.split(), stdout=subprocess.PIPE) #abro un subproceso nuevo para ejecutar la funcion

def systemUpdate(): #1
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"])
    return "Updated"

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

def synchronizeTime(): #3
    return "synchronized"

def takePhoto(): #4
# hace una foto con el nombre elegido desde el servidor y lo almacena en el directorio definido
# en este script

    fileName = data[1]
    print ("File name: " + fileName)

    #creo una carpeta con el nombre del archivo. Util si quiero hacer varias fotos con diferentes
    # iluminaciones y guardarlas bajo un mismo nombre ordenado
    savePath = "/home/pi/Desktop/3DScanner/Client/Pictures/" + fileName + "/"
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    #Actualmente solo guardo una foto
    print ("shooting")
    camera.capture(savePath + fileName,'png')
    print("Took picture")

    #envio la imagen al servidor aqui
    send_socket = socket.socket()
    send_socket.connect((SENDER_IP, IMAGE_TRANSFER_PORT))

    if os.path.isfile(savePath + fileName):
        print("SI existe el path")
    else:
        print("NO existe el path")

    with open(savePath + fileName, 'rb') as image:
        
        image_data = image.read()
        send_socket.sendall(image_data)
    
    send_socket.close()
    
    return "Sent picture to: " + SENDER_IP

def checkListening(): #5
    return "Done."

def default():
# opcion que sirve para dejar constancia de que el comando utilizado no existe
    return "Incorrect command"


switcher = {
    0: powerOff, # Press 0 to poweroff the raspberries
    1: systemUpdate, # Press 1 to update the system of the raspberries
    2: installPython3, # Press 2 to install or update Python3
    3: synchronizeTime, # Press 3 to synchronize_time with the server
    4: takePhoto, # Press 4 to takePhoto
    5: checkListening, # Press 5 to check what raspberries are listening
    
    # If you press another key, try again
    }

def switch(server_command):
    return switcher.get(server_command, default)()

#___________________CODE___________________#

# CONSTANT VARIABLES

MULTICAST_CAMERA_GROUP = '225.1.1.1' #direccion multicast por la que escucha los comandos del servidor
MULTICAST_COMMAND_PORT = 3179 #puerto que abre para recivir los datagramas con los comandos del servidor
IMAGE_TRANSFER_PORT = 5001 #puerto utilizado para enviar las imagenes al servidor una vez realizadas
BUFFER_SIZE = 10240 #tamaño del buffer utilizado en el paso de mensajes por el socket

# CONECTION WITH THE SERVER

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', MULTICAST_COMMAND_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_CAMERA_GROUP), socket.INADDR_ANY)
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
        SENDER_IP = address[0]
        print ("Got new data from the server")
        data = newdata.decode().split()
        print("Data decoded")
        
        cmd = int(data[0])
        print ("Received cmd: " + data[0] + " from: " + SENDER_IP)
        
        print(switch(cmd))
        print()