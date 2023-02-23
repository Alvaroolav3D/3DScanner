import time
import os
from datetime import datetime
import ntplib
    
def synchronize_time(server_ip):

    ntp_client = ntplib.NTPClient()

    # Get the current time on the Raspberry Pi
    pi_time_before_sync = time.time()

    try:
        response = ntp_client.request(server_ip, version=3)
        # Get the current time from the NTP server
        ntp_time = response.tx_time
        # Convert the NTP time to a readable format
        current_time = datetime.fromtimestamp(ntp_time)
        # Set the system time to the current time
        
        os.system('sudo date --set="%s"' % current_time.strftime('%Y-%m-%d %H:%M:%S'))
        print("Time synchronized with NTP server:", server_ip)

        # Get the current time on your laptop
        laptop_time_after_sync = time.time()

        # Calculate the time difference between the Raspberry Pi and your laptop
        time_diff = laptop_time_after_sync - pi_time_before_sync
        print("Time difference between Raspberry Pi and laptop:", time_diff, "seconds")
    except Exception as e:
        print("Error syncing time with NTP server:", e)

# Call the function with the IP address of the NTP server
synchronize_time("192.168.1.200")
