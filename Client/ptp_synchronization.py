import subprocess

server_ip = "192.168.1.200" # IP del servidor
ptp_interface = "eth0" # Interfaz de red utilizada para PTP

# Comando para ejecutar ptp4l y configurar la sincronización con el servidor
cmd = ["sudo", "ptp4l", "-i", ptp_interface, "-s", "-f", "/etc/ptp4l.conf", "-m", "-q", server_ip]

# Ejecutar el comando y esperar a que termine
subprocess.run(cmd)

print("Sincronización PTP completada")