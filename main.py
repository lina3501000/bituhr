# komischer grauer kasten, heist das es ein syntax fehler gibt


# Bibliotheken laden
from machine import Pin, ADC, PWM
from neopixel import NeoPixel
import ds3231
from time import sleep

# Pin DS3231
rtc = ds3231.RTC(sda_pin=16, scl_pin=17, port=0)
# GPIO-Pin für WS2812
pin_hour = 20
pin_min=19
pin_sec=18
# Pin potentiometer
adc0 = ADC(26)

# Anzahl der LEDs
leds = 6
# Helligkeit: 0 bis 255
brightness = 10

# Initialisierung WS2812/NeoPixel
np_hour = NeoPixel(Pin(pin_hour, Pin.OUT), leds)
np_min = NeoPixel(Pin(pin_min, Pin.OUT), leds)
np_sec = NeoPixel(Pin(pin_sec, Pin.OUT), leds)

print(rtc.ReadTime("everything_sorted"))
print(rtc.ReadTime("everything_number"))
# 0 bis 65600

while True:
    rtc_hour =int(rtc.ReadTime("hour"))
    print("hour", rtc_hour)
    hour_bit=bin(rtc_hour)
    print("hourbit", hour_bit)
    
    rtc_min = int(rtc.ReadTime('minute'))
    print("min", rtc_min)
    min_bit=bin(rtc_min)
    print("minbit", min_bit)
    
    rtc_sec = int(rtc.ReadTime("second"))
    print("sec", rtc_sec)
    sec_bit=bin(rtc_sec)
    print("secbit", sec_bit)
    
    value = adc0.read_u16()
    print(value)
    brightness = min(max(value//256, 0), 255)
    print(brightness)
    
    for i in range(6):
        if rtc_hour & 0b1 << i:
            np_hour[i]=(brightness, brightness, brightness)
        else:
            np_hour[i]=(0,0,0)
    
    for i in range(6):
        if rtc_min & 0b1 << i:
            np_min[i]=(brightness, brightness, brightness)
        else:
            np_min[i]=(0,0,0)
            
    for i in range(6):
        if rtc_sec & 0b1 << i:
            np_sec[i]=(brightness, brightness, brightness)
        else:
            np_sec[i]=(0,0,0)

    np_hour.write()
    np_min.write()
    np_sec.write()
    sleep(0.1)
