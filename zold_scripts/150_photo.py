from picamera import PiCamera
import time

camera = PiCamera()

camera.capture("/home/pi/Desktop/pruebas/img_.jpg")
print("Done.")