import socket

def send_file(file_name, target_ips, target_port):
    with open(file_name, 'rb') as f:
        file_data = f.read()

    for target_ip in target_ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.sendall(file_data)
            print(f'Successfully sent file to {target_ip}')
        except socket.error as e:
            print(f'Failed to send file to {target_ip}: {e}')
        finally:
            s.close()

send_file('example.txt', ['192.168.1.150'], 5000)