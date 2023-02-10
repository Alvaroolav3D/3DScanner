#!/bin/bash

# Each script is executed in the order specified, and the next script is only 
# started after the previous one has completed
python3 /home/pi/Desktop/gitrepo.py

sudo chmod +x /home/pi/Desktop/3DScanner/Client/start.sh

python3 /home/pi/Desktop/3DScanner/Client/client_listen.py