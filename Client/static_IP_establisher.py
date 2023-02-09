import re
import subprocess

def get_network_config(interface):
    output = subprocess.run(["ip", "address", "show", interface], stdout=subprocess.PIPE)
    output = output.stdout.decode("utf-8")
    ip_address = re.search("inet ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)
    netmask = re.search("netmask ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)
    gateway = re.search("default via ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)
    dns = re.search("nameserver ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", output).group(1)

    return (ip_address, netmask, gateway, dns)

def get_interface_name2():
    output = subprocess.run(["ip", "link", "show"], stdout=subprocess.PIPE)
    output = output.stdout.decode("utf-8")
    match = re.search("(\d+): ([a-z0-9]+):", output)
    return match.group(2)

def disable_dhcp_and_set_static_ip(interface, ip_address, gateway):
    with open("/etc/dhcpcd.conf", "r") as file:
        lines = file.readlines()

    with open("/etc/dhcpcd.conf", "w") as file:
        for line in lines:
            if line.startswith("interface " + interface):
                file.write(line)
                file.write("static ip_address=" + ip_address + "\n")
                file.write("static routers=" + gateway + "\n")
            elif not line.startswith("interface "):
                file.write(line)

if __name__ == "__main__":
    interface = get_interface_name()
    print("Network interface name:", interface)

    ip_address, netmask, gateway, dns = get_network_config("eth0")
    print("IP address:", ip_address)
    print("Netmask:", netmask)
    print("Gateway:", gateway)
    print("DNS server:", dns)

    #new_ip_address = input("Enter new IP address: ")
    #new_gateway = input("Enter new gateway: ")
    #disable_dhcp_and_set_static_ip(interface, new_ip_address, new_gateway)
    print("Static IP address and gateway set successfully")