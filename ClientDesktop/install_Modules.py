import importlib
import subprocess

# Actualizar pip
subprocess.run(['sudo', 'pip3', 'install', '--upgrade', 'pip'])

# Lista de módulos a instalar
modules = ['subprocess', 'importlib', 'time', 'os', 'datetime', 'socket', 'struct', 'picamera', 'ntplib']
#los que no vienen dados por el sistema son: ['importlib', 'datetime', 'picamera', 'ntplib']

for module in modules:
    try:
        importlib.import_module(module)
        print(module + ' library is already installed')
    except ImportError:
        print(module + ' library not found. Installing...')
        subprocess.run(['sudo', 'pip3', 'install', module])