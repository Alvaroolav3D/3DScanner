import socket
import os

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

MULTICAST_CAMERA_GROUP = '225.1.1.1' #direccion multicast por la que escucha los comandos del servidor
MULTICAST_COMMAND_PORT = 3179 #puerto que abre para recivir los datagramas con los comandos del servidor
IMAGE_TRANSFER_PORT = 5001 #puerto utilizado para enviar las imagenes al servidor una vez realizadas
BUFFER_SIZE = 10240 #tamaño del buffer utilizado en el paso de mensajes por el socket

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
        print(
            "Control commands:\n" +
            "Press 0 to poweroff the raspberries\n" +
            "Press 1 to reboot the raspberries\n"
            )
        
        option = input("What do you want: ")

        data = cmd + " " + option
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))

    if (cmd == "1"):
        # data[0] seria el comando cmd
        # data[1] seria el nombre imagen

        fileName = input("File name: ")

        data = cmd + " " + fileName
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))

        savePath = "Server/Pictures/" + fileName + "/"
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        receive_socket = socket.socket()
        receive_socket.bind(('', IMAGE_TRANSFER_PORT))
        receive_socket.listen(1)

        print ('Waiting for image...')

        connection, client_address = receive_socket.accept()

        print ('Connected by', client_address[0])

        sender_ip = client_address[0].split(".")[-1]
        receivedImageName = fileName + "_" + str(sender_ip)

        with open(savePath + receivedImageName + '.png', 'wb') as image:
            while True:
                imageData = connection.recv(BUFFER_SIZE)
                if not imageData:
                    break
                image.write(imageData)

        connection.close()

        print ('Image received successfully!')


    if (cmd == "2"):
        # data[0] seria el comando cmd

        data = cmd
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))

    if (cmd == "3"):
        # data[0] seria el comando cmd
        # data[1] seria la ip de este dispositivo

        serverIP = get_device_ip()

        data = cmd + " " + serverIP
        
        sock.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))