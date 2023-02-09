import subprocess
import re

def get_network_config(interface):
    output = subprocess.run(["ifconfig", interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    ip_address = re.search("inet ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output.stdout).group(1)
    netmask = re.search("netmask ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output.stdout).group(1)
    gateway = re.search("default gw ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output.stdout).group(1)
    dns_output = subprocess.run(["cat", "/etc/resolv.conf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    dns = re.search("nameserver ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", dns_output.stdout).group(1)
    return ip_address, netmask, gateway, dns

def get_interface_name():
    output = subprocess.run(["ifconfig"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    match = re.search("eth0", output.stdout)
    if match:
        return "eth0"
    else:
        raise Exception("eth0 interface not found")

if __name__ == "__main__":
    interface = get_interface_name()
    ip_address, netmask, gateway, dns = get_network_config(interface)
    print("IP Address:", ip_address)
    print("Netmask:", netmask)
    print("Gateway:", gateway)
    print("DNS:", dns)
