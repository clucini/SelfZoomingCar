import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
# Use the small numbers beside the pins
GPIO.setup(33, GPIO.OUT)
p = GPIO.PWM(33, 50)

# angle should range from 45 to 135, 45 is R and 135 is L
# recommened between 120 and 60
angle = 90
duty = angle/18+2
p.start(duty)
#p.ChangeDutyCycle(75)

input('Press return to stop:')   # use raw_input for Python 2
p.stop()
GPIO.cleanup()
