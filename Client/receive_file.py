import socket

def receive_file(file_name, target_ip, target_port):
    with open('/Desktop/' + file_name, 'ab') as f:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((target_ip, target_port))
            s.listen(1)
            conn, addr = s.accept()
            print('Receiving file from' + addr + '}...')
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
            print('File received and saved as {' + file_name + '}')
        except socket.error as e:
            print('Failed to receive file: {' + e + '}')
        finally:
            conn.close()
            s.close()

receive_file('example.txt', '0.0.0.0', 5000)
