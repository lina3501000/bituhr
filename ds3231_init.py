# Bibliotheken laden
import ds3231

# Initialisierung
rtc = ds3231.RTC(sda_pin=16, scl_pin=17, port=0)

print(rtc.ReadTime("everything_sorted"))
print(rtc.ReadTime("everything_number"))

# Zeit setzen: Sekunde / Minute / Stunde / Wochentag / Tag / Monat / Jahr
rtc.SetTime(b'\x55\x59\x21\x07\x30\x06\x26')

print(rtc.ReadTime("everything_sorted"))
print(rtc.ReadTime("everything_number"))