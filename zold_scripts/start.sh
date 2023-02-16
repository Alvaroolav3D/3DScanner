#!/bin/bash

# Each script is executed in the order specified, and the next script is only 
# started after the previous one has completed
python3 /home/pi/Desktop/git_Update_Repository.py

python3 /home/pi/Desktop/3DScanner/Client/client_listen.py