import paramiko
import io
import socket

def receive_file(file_name, target_ip, target_port):
    with open(file_name, 'wb') as f:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((target_ip, target_port))
            s.listen(1)
            conn, addr = s.accept()
            print(f'Receiving file from {addr}...')
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
            print(f'File received and saved as {file_name}')
        except socket.error as e:
            print(f'Failed to receive file: {e}')
        finally:
            conn.close()
            s.close()

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

def run_remote_command(ip, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode()

# Example usage
# On the receiver:
# receive_file('received_file.txt', '0.0.0.0', 5000)

# On the sender:
#send_file('example.txt', ['192.168.1.100', '192.168.1.101', '192.168.1.102'], 5000)



target_ips = ['192.168.1.150']
receive_file_script = '''
import socket

def receive_file(file_name, target_ip, target_port):
    with open('/Desktop/' + file_name, 'wb') as f:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((target_ip, target_port))
            s.listen(1)
            conn, addr = s.accept()
            print(f'Receiving file from {addr}...')
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
            print(f'File received and saved as {file_name}')
        except socket.error as e:
            print(f'Failed to receive file: {e}')
        finally:
            conn.close()
            s.close()

receive_file('example.txt', '0.0.0.0', 5000)
'''

username = 'pi'
password = '123'

for target_ip in target_ips:
    with io.StringIO(receive_file_script) as script_file:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(target_ip, username=username, password=password)
        sftp_client = ssh_client.open_sftp()
        sftp_client.putfo(script_file, 'receive_file.py')
        sftp_client.close()
        ssh_client.close()
        run_remote_command(target_ip, username, password, 'python3 receive_file.py')
        send_file('example.txt', ['192.168.1.150', '192.168.1.150', '192.168.1.150', '192.168.1.150'], 5000)
        print("nice")