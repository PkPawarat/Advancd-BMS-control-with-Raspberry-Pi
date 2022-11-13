import RPi.GPIO as GPIO
import dht11
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin = 17)

def read_sensor():
    result = instance.read()
    return [result.temperature, result.humidity]


if __name__ == "__main__":
    while True :
        current_sensor = read_sensor()
        print(current_sensor[0], current_sensor[1])
        time.sleep(2)
