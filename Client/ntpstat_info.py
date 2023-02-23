import subprocess

def get_ntpstat_info():
    output = subprocess.check_output(['ntpstat']).decode('utf-8')
    lines = output.strip().split('\n')
    if len(lines) < 2:
        return None
    status = lines[0].split(': ')[1]
    synced_server = lines[1].split(' ')[-1]
    return {'status': status, 'server': synced_server}

ntpstat_info = get_ntpstat_info()
if ntpstat_info:
    print('NTP status:', ntpstat_info['status'])
    print('Synced server:', ntpstat_info['server'])
else:
    print('NTP status information not available')
