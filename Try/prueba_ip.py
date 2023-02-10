import subprocess
import re

def get_interface_name2():
    output = subprocess.check_output(["ifconfig"])
    interfaces = [line.split()[0] for line in output.splitlines() if line.startswith("eth")]
    if len(interfaces) == 0:
        raise Exception("No network interfaces found.")
    return interfaces[0]



def get_interface_name():
    output = subprocess.check_output(["ifconfig"])
    output = output.decode("utf-8")
    interfaces = re.findall("^(\w+)\s", output, re.MULTILINE)
    return interfaces[0]

def get_network_config(interface):
    output = subprocess.check_output(["ifconfig", interface])
    output = output.decode("utf-8")
    ip_address = re.search("inet ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)
    netmask = re.search("netmask ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)
    #gateway = re.search("default gw ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)
    #dns = re.search("nameserver ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)
    return (ip_address, netmask, "none", "none")

#interface = get_interface_name()
ip_address, netmask, gateway, dns = get_network_config("eth0")

#print("Interface:", interface)
print("IP address:", ip_address)
print("Netmask:", netmask)
print("Gateway:", gateway)
print("DNS:", dns)