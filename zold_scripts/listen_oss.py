import socket
import struct
import subprocess
import json
import os

import picamera

from ftplib import FTP

def restart():
    command = "/sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

MCAST_GRP = '225.1.1.1'
MCAST_PORT = 3179

name = socket.getfqdn() #name of the local device

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print (" ")
print ("3D Scanner - Open Source listen script")

debug = 1  # Turn debug message on/off

savePath = "/home/pi/Desktop/pruebas/3DScanner-main/Try"
if not os.path.exists(savePath):
    os.makedirs(savePath)

with picamera.PiCamera() as camera:
    print ("Camera setup, waiting for command\n")
    while True:
        ndata = sock.recv(10240)
        print ("Got ndata")
        #data = json.loads(ndata)
        data = ndata.decode()
        
        print("el datamento es: " + data)
        sdata = data.split()
        print(sdata)
        
        rcmd = 1
        
        if debug == 1:
            print ("Received cmd: "+ sdata[0])
            print ("Data: " + sdata[1])
            print ("File name: " + sdata[3])

        if (rcmd == 1):
            print ("shooting")
            camera.capture(savePath+sdata[3],'png')
            #cmd = "raspistill " + ' '.join(rdata) + " " + iname
            #pid = subprocess.call(cmd, shell=True)
            #while(!check_pid(pid)):
            #   time.sleep(2)
            print ("Took picture")

        if(rcmd == "2"):
            if rdata[0] == name:
                ftp = FTP(rdata[1])
                ftp.login(rdata[2],rdata[3])
                ftp.cwd(name)
                image = open(iname,'rb')
                ftp.storbinary('STOR '+iname,image)
                image.close()
                try:
                    ftp.quit()
                except ftplib.all_errors:
                    ftp.close()

        if (rcmd == "3"):
            camera.resolution = (640, 480)
            camera.framerate = 24

            server_socket = socket.socket()
            server_socket.bind(('0.0.0.0', 8000))
            server_socket.listen(0)

            # Accept a single connection and make a file-like object out of it
            connection = server_socket.accept()[0].makefile('wb')
            try:
                camera.start_recording(connection, format='h264')
                camera.wait_recording(60)
                camera.stop_recording()
            finally:
                connection.close()
                server_socket.close()

        if (rcmd == "-1"):
            print ("Rebooting")
            restart()
