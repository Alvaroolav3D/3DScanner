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
        print(module + ' ya está instalado')
    except ImportError:
        print(module + ' no está instalado, se procederá a instalar')
        # Utilizar subprocess para ejecutar el comando pip3 install
        subprocess.run(['sudo', 'pip3', 'install', module])