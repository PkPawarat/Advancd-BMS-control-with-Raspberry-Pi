import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

pwm = GPIO.PWM(18,300)
pwm.start(0)

try: 
    while True:
        pwm.ChangeDutyCycle(int(input()))

except KeyboardInterrupt:
    pass
    pwm.stop()
    #GPIO.cleanup()



