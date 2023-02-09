import subprocess


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




def get_interface_name():
    # Use the `ip addr` command to find the name of the network interface
    result = subprocess.run(["ip", "addr"], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    
    # Split the output into lines
    lines = output.split("\n")
    
    # Find the line that starts with "2: " (the network interface)
    for line in lines:
        if line.startswith("2: "):
            # Split the line into words
            words = line.split(" ")
            
            # The name of the network interface is the second word
            interface = words[1]
            return interface



def get_network_config():
    output = subprocess.run(["ip", "addr", "show", interface], stdout=subprocess.PIPE).stdout.decode("utf-8")
    lines = output.split("\n")
    for line in lines:
        if "inet " in line:
            ip_address = line.split(" ")[1].split("/")[0]
        if "netmask" in line:
            netmask = line.split(" ")[3]
        if "broadcast" in line:
            broadcast = line.split(" ")[3]
    gateway_output = subprocess.run(["ip", "route", "show", "default"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    gateway_line = gateway_output.split("\n")[0]
    gateway = gateway_line.split(" ")[2]
    dns_output = subprocess.run(["cat", "/etc/resolv.conf"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    dns_lines = dns_output.split("\n")
    dns_servers = []
    for dns_line in dns_lines:
        if "nameserver" in dns_line:
            dns_servers.append(dns_line.split(" ")[1])
    print("Interface: " + interface)
    print("IP address: " + ip_address)
    print("Netmask: " + netmask)
    print("Broadcast: " + broadcast)
    print("Gateway: " + gateway)
    print("DNS servers: " + ', '.join(dns_servers))



get_network_config()

interface = get_interface_name() #me permite utilizar el mismo nombre de interfaz que ya tenia
set_static_ip(interface, ip_address, netmask, gateway, dns)
