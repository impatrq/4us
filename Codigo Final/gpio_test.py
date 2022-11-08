import RPi.GPIO as GPIO
from time import sleep

infrarojo_gpio = 21
puls_1 = 20
plastico = 16
metales = 7
cartones = 8
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(infrarojo_gpio, GPIO.IN)
GPIO.setup(puls_1, GPIO.IN)
GPIO.setup(plastico, GPIO.IN)
GPIO.setup(metales, GPIO.IN)
GPIO.setup(cartones, GPIO.IN)

while True:
    print("puls 1 vale: ",(GPIO.input(puls_1)))
    print("plastico vale: ",(GPIO.input(plastico)))
    print("metales vale: ",(GPIO.input(metales)))
    print("cartones 4 vale: ",(GPIO.input(cartones)))
    sleep(.5)
    #GPIO.output(infrarojo_gpio, 0)
    #print(GPIO.input(infrarojo_gpio))
    sleep(.5)
    #GPIO.output(infrarojo_gpio, 1)
    #print(GPIO.input(infrarojo_gpio))
    #sleep(.5)