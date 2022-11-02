import RPi.GPIO as GPIO
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
import sensor, k_type_temp

# Setup Fan pin by usign driver at MA
FAN_PIN_A1 = 37
FAN_PIN_A2 = 35
FAN_PIN_EA = 40
GPIO.setup(FAN_PIN_A1, GPIO.OUT)
GPIO.setup(FAN_PIN_A2, GPIO.OUT)
GPIO.setup(FAN_PIN_EA, GPIO.OUT)
GPIO.output(FAN_PIN_A1, GPIO.LOW)
GPIO.output(FAN_PIN_A2, GPIO.HIGH)               #turn on
fan = GPIO.PWM(FAN_PIN_EA,1000)             # Set GPIO14 as a PWM output, with 100Hz frequency (we need to make it match the fans specified PWM frequency)
fan.start(50)                               # Generate a PWM signal with a 50% duty cycle (fan on), start on so that it increases humidity of room and then turns it off or slows down

# Setup Relay pin by usign driver at MB
relay_pin_B1 = 33
relay_pin_B2 = 31
GPIO.setup(relay_pin_B1, GPIO.OUT)
GPIO.setup(relay_pin_B2, GPIO.OUT)
GPIO.output(relay_pin_B1, GPIO.HIGH)             #turn on
GPIO.output(relay_pin_B2, GPIO.LOW)

def Fan(humid = sensor.sensor_get_humid()):
    if int(humid) < 40:
        fan.start(100)
        fan_on()
        print("ON 100 speed Fan")
    elif int(humid) > 40 and int(humid) < 60:
        fan.start(50)
        fan_on()
        print("ON 50 speed Fan")
    elif int(humid) > 60:
        fan.start(0)
        fan_off()
        print("OFF 0 speed Fan")

def relay(humid = k_type_temp.read_temp()):         #this funciton will trun on Humidifyis water temp less than 50 C, else turn off
    if int(humid) < 50:
        relay_on()
    else:
        relay_off()

def relay_on():
    GPIO.output(relay_pin_B1, GPIO.HIGH)
    GPIO.output(relay_pin_B2, GPIO.LOW)

def relay_off():
    GPIO.output(relay_pin_B1, GPIO.LOW)
    GPIO.output(relay_pin_B2, GPIO.LOW)

def fan_on():
    GPIO.output(FAN_PIN_A1, GPIO.LOW)
    GPIO.output(FAN_PIN_A2, GPIO.HIGH)

def fan_off():
    GPIO.output(FAN_PIN_A1, GPIO.LOW)
    GPIO.output(FAN_PIN_A2, GPIO.LOW)


if __name__ == "__main__":

    while(1):
        Fan()
        relay()
        # pass
        
GPIO.cleanup()