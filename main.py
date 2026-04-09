# komischer grauer kasten, heist das es ein syntax fehler gibt


# Bibliotheken laden
from machine import Pin, ADC, PWM
from neopixel import NeoPixel
import ds3231
from time import sleep

# pin an/aus schalter
schalter=Pin(0, Pin.IN, Pin.PULL_DOWN)
modus=Pin(1, Pin.IN, Pin.PULL_DOWN)
# pin button
button=Pin(2, Pin.IN, Pin.PULL_DOWN)
# Pin DS3231
rtc = ds3231.RTC(sda_pin=16, scl_pin=17, port=0)
# GPIO-Pin für WS2812
pin_sec=18
pin_min=19
pin_hour = 20
# Pin potentiometer
adc0 = ADC(26)

# Anzahl der LEDs
leds = 6
# Helligkeit: 0 bis 255
brightness = 10

brightness_r = 10
brightness_g = 10
brightness_b = 10

farbmodus=1

# Initialisierung WS2812/NeoPixel
np_hour = NeoPixel(Pin(pin_hour, Pin.OUT), leds)
np_min = NeoPixel(Pin(pin_min, Pin.OUT), leds)
np_sec = NeoPixel(Pin(pin_sec, Pin.OUT), leds)

print(rtc.ReadTime("everything_sorted"))
print(rtc.ReadTime("everything_number"))

while True:
    rtc_hour =int(rtc.ReadTime("hour"))
    hour_bit=bin(rtc_hour)
    
    rtc_min = int(rtc.ReadTime('minute'))
    min_bit=bin(rtc_min)
    
    rtc_sec = int(rtc.ReadTime("second"))
    sec_bit=bin(rtc_sec)
    
    schaltervalue = schalter.value()
    #print("schalter:", schaltervalue)
    
    modusvalue=modus.value()
    print("modus:", modusvalue)
   
    print(brightness_r, brightness_g, brightness_b)
   
    value = adc0.read_u16()
    
    if schaltervalue==1:
        brightness = 0
    elif modusvalue==1:
        sleep(0.1)
        buttonvalue=button.value()
        print("button", buttonvalue)
        print("farbmodus:", farbmodus)
        if buttonvalue==1:
            farbmodus+=1
        
        if farbmodus==4:
            farbmodus=1
            
        if farbmodus == 1:
            brightness_r=min(max(value//256, 0), 255)
        elif farbmodus ==2:
            brightness_g=min(max(value//256, 0), 255)
        elif farbmodus==3:
            brightness_b=min(max(value//256, 0), 255)
    
    else:
        brightness_r = min(max(value//256, 0), 255)
        brightness_g = min(max(value//256, 0), 255)
        brightness_b = min(max(value//256, 0), 255)
    
    
    for i in range(6):
        if rtc_hour & 0b1 << i:
            np_hour[i]=(brightness_r, brightness_g, brightness_b)
        else:
            np_hour[i]=(0,0,0)
    
    for i in range(6):
        if rtc_min & 0b1 << i:
            np_min[i]=(brightness_r, brightness_g, brightness_b)
        else:
            np_min[i]=(0,0,0)
            
    for i in range(6):
        if rtc_sec & 0b1 << i:
            np_sec[i]=(brightness_r, brightness_g, brightness_b)
        else:
            np_sec[i]=(0,0,0)

    np_hour.write()
    np_min.write()
    np_sec.write()
    sleep(0.05)