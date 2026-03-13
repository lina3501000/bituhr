# Bibliotheken laden
import ds3231

# Initialisierung
rtc = ds3231.RTC(sda_pin=20, scl_pin=21)

# Zeit lesen und ausgeben
rtc_time = rtc.ReadTime('DIN-1355-1+time')
print('Alt:', rtc_time)

# Zeit setzen: Sekunde / Minute / Stunde / Wochentag / Tag / Monat / Jahr
rtc.SetTime(b'\x00\x31\x14\x06\x19\x12\x25')

# Zeit lesen und ausgeben
rtc_time = rtc.ReadTime('DIN-1355-1+time')
print('Neu:', rtc_time)