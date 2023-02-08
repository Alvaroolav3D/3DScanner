import os
import subprocess

# Check if nmap is installed
try:
    subprocess.run(["nmap", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
    # If not installed, install nmap
    print("Installing nmap...")
    os.system("sudo apt-get update && sudo apt-get install nmap -y")

# Scan for connected devices with Ethernet
result = subprocess.run(["nmap", "-sP", "192.168.0.0/24"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = result.stdout.decode("utf-8")

# Extract IP addresses from the nmap output
ips = []
for line in output.split("\n"):
    if "Nmap scan report for" in line:
        ip = line.split(" ")[-1]
        ips.append(ip)

# Print the IP addresses of the connected devices
print("Connected devices:")
for ip in ips:
    print(ip)