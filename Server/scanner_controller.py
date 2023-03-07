import socket
import os
import threading
import time
import statistics

#___________________FUNCTIONS___________________#

def handle_connection(connection, fileName):
    savePath = "Server/Pictures/" + fileName + "/"
    os.makedirs(savePath, exist_ok=True)

    sender_ip = connection.getpeername()[0].split('.')[-1]
    receivedImageName = fileName + '_' + str(sender_ip)

    with open(savePath + receivedImageName + '.png', 'wb') as image:
        try:
            while True:
                imageData = connection.recv(BUFFER_SIZE)
                if not imageData:
                    break
                image.write(imageData)
        except Exception as e:
            print("Error during image reception:", e)
        finally:
            connection.close()

    print('Image received from', sender_ip)

def check_Detected_Devices(detected_Devices):
    c_Dictionary = {0: "1B", 1: "1A", 2: "2B", 3: "2A", 4: "3B", 5: "3A", 6: "4B", 7: "4A", 8: "5A", 9: "6B", 10: "6A", 11: "7B", 12: "7A", 13: "8B", 14: "8A", 15: "9B", 16: "9A"}
    missing_Devices = []

    for i in range(len(scanner_Devices)):
        missing = [val for val in scanner_Devices[i] if val not in detected_Devices]
        missing_Devices.append(missing)

    for i in range(len(missing_Devices)):
        print("Missing devices in", c_Dictionary[i], ":", missing_Devices[i])
    
#___________________CODE___________________#

# CONSTANT VARIABLES

MULTICAST_CAMERA_GROUP = '225.1.1.1' # Multicast camera address that listens for commands from the server
MULTICAST_COMMAND_PORT = 3179 # Port that it opens to receive the datagrams with the commands from the server
IMAGE_TRANSFER_PORT = 5001 # Port used to send the images to the server once they have been made
BUFFER_SIZE = 10240 # Size of the buffer used in passing messages through the socket
NUM_CAMERAS = 74 # Number of raspberries with cameras in the escaner

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
    ['', '', '', ''], #8A
    ['', '', '', '', ''], #9B
    ['', '', '', '', ''], #9A
]

# MAIN

print(
    "\nControl commands:\n" +

    "Press 0 to poweroff or reboot the raspberries\n" +
    "Press 1 to update the system of the raspberries\n" +
    "Press 2 to install or update Python3\n" +
    "Press 3 to synchronize_time with the server\n" +
    "Press 4 to take a picture\n" + 
    "Press 5 to check what raspberries are listening\n" + 

    "If you press another key, try again\n"
    )

# Create the socket in charge of sending commands to the different raspberries
cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
cmd_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

while True:
    cmd = input("Command: ")
    print("")

    if (cmd == "-1"):
        cmd_socket.close()
        break

    if (cmd == "0"): # Press 0 to poweroff or reboot the raspberries
        # data[0] is the chosen command
        # data[1] is the chosen option

        print(
            "Control commands:\n" +
            "Press 0 to poweroff the raspberries\n" +
            "Press 1 to reboot the raspberries\n"
            )
        
        option = input("What do you want: ")

        data = cmd + " " + option
        
        cmd_socket.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))

    if (cmd == "1"): # Press 1 to update the system of the raspberries
        # data[0] is the chosen command

        data = cmd
        
        cmd_socket.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))

        receive_socket = socket.socket()
        receive_socket.bind(('', IMAGE_TRANSFER_PORT))
        receive_socket.listen(NUM_CAMERAS)

        system_update_Done = []

        for i in range(NUM_CAMERAS):
            try:
                connection, client_address = receive_socket.accept()
                sender_ip = connection.getpeername()[0].split('.')[-1]
                print(sender_ip)
                system_update_Done.append(sender_ip)
                connection.close()
            except socket.timeout:
                print("Timed out waiting for connection.\n")
                break
        
        time.sleep(1)
        print(system_update_Done, "\n")
        receive_socket.close()

    if (cmd == "2"): # Press 2 to install or update Python3
        # data[0] is the chosen command

        data = cmd
        
        cmd_socket.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))
        
        receive_socket = socket.socket()
        receive_socket.bind(('', IMAGE_TRANSFER_PORT))
        receive_socket.settimeout(5)
        receive_socket.listen(NUM_CAMERAS)

        python_update_Done = []

        for i in range(NUM_CAMERAS):
            try:
                connection, client_address = receive_socket.accept()
                sender_ip = connection.getpeername()[0].split('.')[-1]
                print(sender_ip)
                python_update_Done.append(sender_ip)
                connection.close()
            except socket.timeout:
                print("Timed out waiting for connection.\n")
                break
        
        time.sleep(1)
        print(python_update_Done, "\n")
        receive_socket.close()
        
    if (cmd == "3"): # Press 3 to synchronize_time with the server
        # data[0] is the chosen command

        timer = time.time()

        data = cmd + " " + str(timer)
        
        cmd_socket.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))
        
        receive_socket = socket.socket()
        receive_socket.bind(('', IMAGE_TRANSFER_PORT))
        receive_socket.settimeout(5)
        receive_socket.listen(NUM_CAMERAS)

        ips_timeDiffs = []
        timeDiffs = []

        for i in range(NUM_CAMERAS):
            try:
                connection, client_address = receive_socket.accept()
                sender_ip = connection.getpeername()[0].split('.')[-1]
                message = float(connection.recv(1024).decode('utf-8'))
                ips_timeDiffs.append((sender_ip, message))
                timeDiffs.append(message)
                connection.close()
            except socket.timeout:
                print("Timed out waiting for connection.\n")
                break
        
        mean = statistics.mean(timeDiffs)
        
        time.sleep(1)
        print(ips_timeDiffs, "\n")
        print("The max difference is: ", max(timeDiffs) - min(timeDiffs)," seconds\n")
        print("The mean is: ", mean, "\n")
        receive_socket.close()

    if (cmd == "4"): # Press 4 to take a picture
        # data[0] is the chosen command
        # data[1] is the picture file name

        fileName = input("File name: ")

        data = cmd + " " + fileName
        
        cmd_socket.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))

        savePath = "Server/Pictures/" + fileName + "/"
        os.makedirs(savePath, exist_ok=True)

        receive_socket = socket.socket()
        receive_socket.bind(('', IMAGE_TRANSFER_PORT))
        receive_socket.settimeout(10)
        receive_socket.listen(NUM_CAMERAS) # en vez de 1 habria que poner el numero de camaras que tenga

        print('Waiting for image...')
        
        for i in range(NUM_CAMERAS):
            try:
                connection, client_address = receive_socket.accept()
                
                print('Connected by', client_address)

                # Start a new thread to handle the connection
                t = threading.Thread(target=handle_connection, args=(connection, fileName))
                t.start()
            except socket.timeout:
                print("Timed out waiting for connection.\n")
                break

        time.sleep(2)
        print ('Images received successfully!\n')
        receive_socket.close()

    if (cmd == "5"): # Press 5 to check what raspberries are listening
        # data[0] is the chosen command

        data = cmd
        
        cmd_socket.sendto(data.encode(), (MULTICAST_CAMERA_GROUP, MULTICAST_COMMAND_PORT))

        receive_socket = socket.socket()
        receive_socket.bind(('', IMAGE_TRANSFER_PORT))
        receive_socket.settimeout(5)
        receive_socket.listen(NUM_CAMERAS)

        ips_listening = []

        for i in range(NUM_CAMERAS):
            try:
                connection, client_address = receive_socket.accept()
                sender_ip = connection.getpeername()[0].split('.')[-1]
                print(sender_ip)
                ips_listening.append(sender_ip)
                connection.close()
            except socket.timeout:
                print("Timed out waiting for connection.\n")
                break
        
        time.sleep(1)
        
        check_Detected_Devices(ips_listening)
        
        print("Detected: ", len(ips_listening), "\n")

        receive_socket.close()