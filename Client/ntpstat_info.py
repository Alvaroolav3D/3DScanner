import subprocess

def get_ntpstat_info():
    try:
        output = subprocess.check_output(['ntpstat'], stderr=subprocess.STDOUT)
        output = output.decode('utf-8').strip()
        lines = output.split('\n')
        status = lines[0].split(': ')[1]
        if status == 'synchronized':
            offset = float(lines[1].split(': ')[1])
            jitter = float(lines[2].split(': ')[1])
            return {'status': status, 'offset': offset, 'jitter': jitter}
        else:
            return {'status': status}
    except subprocess.CalledProcessError:
        return {'status': 'error'}

ntpstat_info = get_ntpstat_info()

if ntpstat_info['status'] == 'synchronized':
    print('NTP synchronized with an offset of {} ms and a jitter of {} ms'.format(ntpstat_info['offset'], ntpstat_info['jitter']))
else:
    print('NTP is not synchronized')
