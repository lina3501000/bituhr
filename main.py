# Bibliotheken laden
from machine import Pin, ADC, PWM, Timer
from neopixel import NeoPixel
import ds3231
from time import sleep
import time

#led_onboard = Pin(25, Pin.OUT)
led_off=True
zeit_alt=time.ticks_ms()

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

aus=1

# Initialisierung WS2812/NeoPixel
np_hour = NeoPixel(Pin(pin_hour, Pin.OUT), leds)
np_min = NeoPixel(Pin(pin_min, Pin.OUT), leds)
np_sec = NeoPixel(Pin(pin_sec, Pin.OUT), leds)

print(rtc.ReadTime("everything_sorted"))
print(rtc.ReadTime("everything_number"))

i=25
print(int(i))

while True:
    year =rtc.ReadTime("year")
    print("year:", year)
    everything_number=rtc.ReadTime("everything_number")
    print(everything_number)
    if everything_number[0]==0x02 and everything_number[1]==0x00 and everything_number[2]==0x00 and everything_number[3]==0x07 and everything_number[4]>=25 and everything_number[5]==0x03:
        #neu[6]=year_kurz#muss mit fancy ding machen
        neu=rtc.ReadTime("alles_buffer")
        neu=list(neu)
        neu[2]=neu[2]+1
        neu=tuple(neu)
        print("neu:",neu)
        neu=(bytes(neu))
        print(neu)
        rtc.SetTime(neu)
        print("von normal auf sommerzeit")
        print(rtc.ReadTime("everything_sorted"))
        print(rtc.ReadTime("everything_number"))
        sleep(60)
    if everything_number[0]==0x03 and everything_number[1]==0x00 and everything_number[2]==0x00 and everything_number[3]==0x07 and everything_number[4]>=25  and everything_number[5]==10:
        #neu[6]=year_kurz#muss mit fancy ding machen
        neu=rtc.ReadTime("alles_buffer")
        neu=list(neu)
        neu[2]=neu[2]-1
        neu=tuple(neu)
        print("neu:",neu)
        neu=(bytes(neu))
        print(neu)
        rtc.SetTime(neu)
        print("von sommer auf normal")
        print(rtc.ReadTime("everything_sorted"))
        print(rtc.ReadTime("everything_number"))
        sleep(60)
    print(rtc.ReadTime("everything_sorted"))
    
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
    hour=rtc.ReadTime("hour")
    print("hour:", hour)
    if schaltervalue==1:
        brightness_r, brightness_g, brightness_b = 0,0,0
        sleep(1)
    
    elif modusvalue==1:
        buttonvalue=button.value()
        print("button", buttonvalue)
        print("farbmodus:", farbmodus)
        if buttonvalue==1:
            farbmodus+=1
            sleep(0.3)
        
        if farbmodus==4:
            farbmodus=1
            
        if farbmodus == 1:
            brightness_r=min(max(value//280, 0), 255)
        elif farbmodus ==2:
            brightness_g=min(max(value//280, 0), 255)
        elif farbmodus==3:
            brightness_b=min(max(value//280, 0), 255)
    elif 20<=hour<22:
            brightness_r=50
            brightness_g=0
            brightness_b=0
    elif hour>=22 or hour < 8:
            brightness_r=10
            brightness_g=0
            brightness_b=0
    else:
        brightness_r = brightness_g = brightness_b = min(max(value//280, 0), 255)
    if hour_bit==min_bit:
        print("blink")
        now=time.ticks_ms()
        if(time.ticks_diff(now,zeit_alt) > 500):
            led_off=not led_off
            zeit_alt=now
        if led_off:
            brightness_r, brightness_g, brightness_b = 0,0,0

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