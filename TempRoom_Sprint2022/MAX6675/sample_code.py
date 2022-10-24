from machine import Pin,I2C
import utime as time
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
from max6675 import MAX6675

WIDTH  = 128                                          
HEIGHT = 64
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=200000)   
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

so = Pin(15, Pin.IN)
sck = Pin(13, Pin.OUT)
cs = Pin(14, Pin.OUT)

max = MAX6675(sck, cs , so)
buzzer = Pin(28, Pin.OUT)

while True:
    print(max.read())
    data= max.read()
    oled.fill(0) 
    write20 = Write(oled, ubuntu_mono_20)
    write20.text("Temperature: ", 0, 0)
    write20.text(str(round(data,1)),0,20)
    write20.text("*C",44,20)
    oled.show()
    if data > 50:
        buzzer.value(1)
        time.sleep(3)
        buzzer.value(0)

        

    time.sleep(1.1)