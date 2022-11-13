import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

pwm = GPIO.PWM(18,300)
pwm.start(0)

try: 
    while True:
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
            print(dc)
        for dc in range(100, -1, -5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
            print(dc)
except KeyboardInterrupt:
    pass
    pwm.stop()
    GPIO.cleanup()



