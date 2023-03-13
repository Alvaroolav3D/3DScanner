import os
from time import sleep

# lista de nombres de archivo de imagen
img_files = ['/home/pi/Desktop/3DScanner/Client/img1.png', '/home/pi/Desktop/3DScanner/Client/img2.png']

print(os.getcwd())

# tiempo de visualización de cada imagen
display_time = 1  # segundos

# mostrar cada imagen
for img_file in img_files:
    # comprobar si el archivo de imagen existe
    if not os.path.isfile(img_file):
        print(f"Error: el archivo {img_file} no existe")
        continue
    
    # mostrar la imagen durante el tiempo especificado
    os.system(f"sudo fbi -a --noverbose --vt 1 {img_file}")
    sleep(display_time)
    
print("Todas las imágenes han sido mostradas.")