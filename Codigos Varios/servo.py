import RPi.GPIO as GPIO
from time import sleep
 
servoPin = 7
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)
pin7 = GPIO.PWM(servoPin, 50)
pin7.start(0)
 
def angleToDutyConvert(angle):
  dutyCycle = angle / 18 + 2
  GPIO.output(servoPin, GPIO.HIGH)
  pin7.ChangeDutyCycle(dutyCycle)
  sleep(0.15)
  GPIO.output(servoPin, GPIO.LOW)
  sleep(0.15)

def sweep(degrees):
  for pos in range(0, degrees, +5):
    print(pos)
    angleToDutyConvert(pos)
  for pos in range(degrees, 0, -5):
    print(pos)
    angleToDutyConvert(pos)
 
while True:
  sweep(45)
  sweep(90)