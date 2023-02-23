import subprocess

def get_ntpstat_info():
    try:
        output = subprocess.check_output(['ntpstat'])
        lines = output.decode().strip().split('\n')
        status = lines[0].split(': ')[1]
        info = lines[1:]
        return status, info
    except subprocess.CalledProcessError as e:
        return 'error', [e.output.decode().strip()]

def get_ntp_service_status():
    try:
        output = subprocess.check_output(['systemctl', 'status', 'ntp'])
        lines = output.decode().strip().split('\n')
        status = lines[2].split(':')[1].strip()
        return status
    except subprocess.CalledProcessError as e:
        return 'error'

ntpstat_info = get_ntpstat_info()
ntp_service_status = get_ntp_service_status()

print('NTP service status:', ntp_service_status)

if ntpstat_info[0] == 'synchronised':
    print('NTP status: synced')
    print('\n'.join(ntpstat_info[1]))
else:
    print('NTP status:', ntpstat_info[0])
    print('\n'.join(ntpstat_info[1]))
