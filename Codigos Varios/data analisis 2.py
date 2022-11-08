import RPi.GPIO as GPIO
puls_1 = 23
puls_2 = 21
puls_3 = 19
puls_4 = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(puls_1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(puls_2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(puls_3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(puls_4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
while True:
    if GPIO.input(23) == GPIO.HIGH:
        print("Button was pushed!")
    if  GPIO.input(puls_1):
        print("pulsador 1 presionado")
    if  GPIO.input(puls_2):
        print("pulsador 2 presionado")
    if  GPIO.input(puls_3):
        print("pulsador 3 presionado")
    if  GPIO.input(puls_4):
        print("pulsador 4 presionado")