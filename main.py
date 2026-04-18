from machine import Pin, ADC, PWM, Timer
from neopixel import NeoPixel
import ds3231
from time import sleep
import time

# pin an/aus schalter und modus
schalter=Pin(0, Pin.IN, Pin.PULL_DOWN)
modus=Pin(1, Pin.IN, Pin.PULL_DOWN)
# pin button
button=Pin(2, Pin.IN, Pin.PULL_DOWN)
# Pin DS3231
rtc = ds3231.RTC(sda_pin=16, scl_pin=17, port=0)
# GPIO-Pin neopixel
pin_sec=18
pin_min=19
pin_hour = 20
# Pin potentiometer
adc0 = ADC(26)

# variablen LED
leds = 6
brightness_r = 10
brightness_g = 10
brightness_b = 10

#variablen rest
farbmodus=1
aus=1

#timer 
led_off=True
zeit_alt=time.ticks_ms()

# init NeoPixel
np_hour = NeoPixel(Pin(pin_hour, Pin.OUT), leds)
np_min = NeoPixel(Pin(pin_min, Pin.OUT), leds)
np_sec = NeoPixel(Pin(pin_sec, Pin.OUT), leds)

def zeitumstellung(change_to):
    neue_zeit=rtc.ReadTime("alles_buffer")
    neue_zeit=list(neue_zeit)
    if change_to=="sommer":  
        neue_zeit[2]=neue_zeit[2]+1
    elif change_to == "normal":
        neue_zeit[2]=neue_zeit[2]-1
    neue_zeit=tuple(neue_zeit)
    neue_zeit=(bytes(neue_zeit))
    rtc.SetTime(neue_zeit)
    print(rtc.ReadTime("everything_sorted"))
    sleep(60)

print(rtc.ReadTime("everything_sorted"))
print(rtc.ReadTime("everything_number"))

while True:
    everything_number=rtc.ReadTime("everything_number")
    
    rtc_hour =int(rtc.ReadTime("hour"))
    hour_bit=bin(rtc_hour)
    hour=rtc.ReadTime("hour")
    rtc_min = int(rtc.ReadTime('minute'))
    min_bit=bin(rtc_min)
    rtc_sec = int(rtc.ReadTime("second"))
    sec_bit=bin(rtc_sec)
    
    schaltervalue = schalter.value()
    modusvalue=modus.value()
    value = adc0.read_u16()
    
    #print(brightness_r, brightness_g, brightness_b)
    
    if everything_number[0]==0x02 and everything_number[1]==0x00 and everything_number[2]==0x00 and everything_number[3]==0x07 and everything_number[4]>=25 and everything_number[5]==0x03:
        zeitumstellung("sommer")
    elif everything_number[0]==0x03 and everything_number[1]==0x00 and everything_number[2]==0x00 and everything_number[3]==0x07 and everything_number[4]>=25  and everything_number[5]==10:
        zeitumstellung("normal")
        
    if schaltervalue==1:
        brightness_r, brightness_g, brightness_b = 0,0,0
        sleep(0.5)
    
    elif modusvalue==1:
        buttonvalue=button.value()
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