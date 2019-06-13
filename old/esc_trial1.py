import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
# Use the small numbers beside the pins
GPIO.setup(37, GPIO.OUT)
p = GPIO.PWM(37, 50)
finish = 0
p.start(7.5)
# Input for speed: 500 - neutral, 1000 full forward, 0 full brake
while (finish != 1):
    speed = input('Enter desired speed:')
    speed = float(speed)*0.005
    if (speed>1000) or (speed<0):
        finish = 1
    duty = 5+speed
    p.ChangeDutyCycle(duty)
p.ChangeDutyCycle(7.5)
sleep(1)
p.stop()
GPIO.cleanup()