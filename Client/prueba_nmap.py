import os
import subprocess
import nmap

# Check if nmap is installed
try:
    subprocess.run(["nmap", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    # If not installed, install nmap
    print("Installing nmap...")
    os.system("sudo apt-get update && sudo apt-get install nmap -y")

# Initialize nmap scanner object
nm = nmap.PortScanner()

# Scan for devices on local network
nm.scan(hosts='192.168.1.0/24', arguments='-sn') #sn perform a ping scan

# Get a list of all hosts up
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

# Extract just the IP addresses and store in an array
ips = [host[0] for host in hosts_list if host[1] == 'up']

# Print the list of IPs
print("Connected devices:")
for ip in ips:
    print(ip)