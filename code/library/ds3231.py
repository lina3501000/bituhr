import machine

class RTC:
    w = ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']
    
    def __init__(self, sda_pin=16, scl_pin=17, port=0, speed=100000, address=0x68, register=0x00):
        self.rtc_address = address
        self.rtc_register = register
        sda=machine.Pin(sda_pin)
        scl=machine.Pin(scl_pin)
        self.i2c=machine.I2C(port, sda=sda, scl=scl, freq=speed)

    def SetTime(self, NowTime = b'\x00\x23\x12\x28\x14\x07\x21'):
        # NowTime (sec min hour weekday day month year)
        self.i2c.writeto_mem(int(self.rtc_address), int(self.rtc_register), NowTime)

    # Convert to binary format
    def bcd2bin(self, value):
        return (value or 0) - 6 * ((value or 0) >> 4)

    # Add a 0 in front of numbers smaller than 10
    def pre_zero(self, value):
        if value < 10:
            value = '0' + str(value)
        return str(value)

    def ReadTime(self, mode=0):
        try:
            buffer = self.i2c.readfrom_mem(self.rtc_address, self.rtc_register, 7)
        except:
            return 'Error: Not connected to DS3231'
        
        year = self.bcd2bin(buffer[6])
        year_buffer=buffer[6]
        month = self.bcd2bin(buffer[5])
        month_buffer=buffer[5]
        day = self.bcd2bin(buffer[4])
        day_buffer=buffer[4]
        weekday = self.bcd2bin(buffer[3])
        weekday_buffer=buffer[3]
        hour = self.bcd2bin(buffer[2])
        hour_buffer=buffer[2]
        minute = self.bcd2bin(buffer[1])
        minute_buffer=buffer[1]
        second = self.bcd2bin(buffer[0])
        second_buffer=buffer[0]
        

        #montag=1, sonntag=7
        # Output
        if mode == 'everything_sorted':
            return self.pre_zero(hour) + ':' + self.pre_zero(minute) + ':' + self.pre_zero(second) + " " + self.w[weekday] + ": " + self.pre_zero(day) + '.' + self.pre_zero(month) + '.' + str(year)
        elif mode == 'everything_number':
            return hour , minute, second , weekday, day, month, year
        elif mode == "everything_set":
            return second, minute,  hour , weekday, day, month, year
        elif mode == "alles_buffer":
            return second_buffer, minute_buffer, hour_buffer, weekday_buffer, day_buffer, month_buffer,year_buffer
        elif mode == 'second':
            return second
        elif mode == 'minute':
            return minute
        elif mode == 'hour':
            return hour
        elif mode =="year_kurz":
            return year_kurz
        elif mode == "tag":
            return day
        elif mode =="year":
            return year
        else:
            return "wrong cathegory"
