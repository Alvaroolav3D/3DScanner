import importlib
import time
import os
from datetime import datetime
import subprocess


try:
    importlib.import_module("ntplib")
    print("ntplib library is already installed.")
except ImportError:
    print("ntplib library not found. Installing...")
    subprocess.run(["pip", "install", "ntplib"])
    print("ntplib library installed.")

def synchronize_time(server_ip):
    import ntplib

    ntp_client = ntplib.NTPClient()

    try:
        response = ntp_client.request(server_ip, version=3)
        # Get the current time from the NTP server
        ntp_time = response.tx_time
        # Convert the NTP time to a readable format
        current_time = datetime.fromtimestamp(ntp_time)
        # Set the system time to the current time
        time.sleep(2)
        os.system('sudo date --set="%s"' % current_time.strftime('%Y-%m-%d %H:%M:%S'))
        print("Time synchronized with NTP server:", server_ip)
    except Exception as e:
        print("Error syncing time with NTP server:", e)

# Call the function with the IP address of the NTP server
synchronize_time("192.168.1.145")
