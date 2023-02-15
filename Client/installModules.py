import importlib
import subprocess

# Actualizar pip
subprocess.run(['sudo', 'pip3', 'install', '--upgrade', 'pip'])

# Lista de módulos a instalar
modules = ['subprocess', 'importlib', 'time', 'os', 'datetime', 'socket', 'struct', 'picamera']

# Iterar sobre la lista de módulos y comprobar si están instalados
for module in modules:
    try:
        importlib.import_module(module)
        print('{} ya está instalado'.format(module))
    except ImportError:
        print('{} no está instalado, se procederá a instalar'.format(module))
        # Utilizar subprocess para ejecutar el comando pip3 install
        subprocess.run(['sudo', 'pip3', 'install', module])
