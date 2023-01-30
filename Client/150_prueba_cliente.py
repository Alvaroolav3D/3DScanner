import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = "192.168.1.153"
port = 5001

filename = input("Name of the file do you want to transfer: ")
filesize = os.path.getsize(filename)

s = socket.socket()
print("Connecting to " + str(host) + ":" + str(port))
s.connect((host, port))
print("Connected.")

data = "" + filename + SEPARATOR + str(filesize)
s.send(data.encode())

progress = tqdm.tqdm(range(filesize), "sending" + filename, unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()