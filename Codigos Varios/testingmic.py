######## prueba de infrarojo
import RPi.GPIO as GPIO
from time import sleep

sensor = 10
sensor_2 = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(sensor_2,GPIO.IN)

print ("Sensores listos.....")
while True:
    if not GPIO.input(sensor_2) or not GPIO.input(sensor):
        print("objeto detectado por alguno de los dos sensores")
        sleep(.1)
    else:
        print("nada")
        sleep(.2)
