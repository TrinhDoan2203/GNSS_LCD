#decode GNSS data and write it to test.txt file
import time
import serial
import sys
from datetime import datetime, timedelta
from pytz import timezone
import pytz
ser = serial.Serial('/dev/ttyS2', 115200)
try:
        class GNSS:
                def read(self):
                        #ser.reset_input_buffer()
                        while ser.inWaiting()==0:
                        #       print('waiting')
                                pass
                        NMEA=ser.readline().decode('latin1')
                        array=NMEA.split(",")
                        #self.fix = 0
                        #self.timeUTC=' '
                        #self.latDeg=' '
                        utc = pytz.utc
                        helsinki = timezone('Europe/Helsinki')
                        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
                        try:
                                if array[0] == '$GNGGA':
                                        #self.timeUTC=array[1][0:2]+':'+array[1][2:4]+':'+array[1][4:6]
                                        self.latDeg=array[2][0:2]+chr(223)+array[2][2:]+'\'' +array[3]
                                        self.longDeg=array[4][0:3]+chr(223)+array[4][3:]+'\''+array[5]
                                        self.fix=array[6]+ ' '
        #                               print(array)
                                if array[0] == '$GNZDA':
                                        loc_time=utc.localize(datetime(int(array[4]), int(array[3]), int(array[2]), int(array[1][0:2]), int(array[1][2:4]), int(array[1][4:6])))
                                        #loc_time=utc.localize(datetime(2002, 10, 27, 6, 0, 0))
                                                #print('ok')
                                        hel = loc_time.astimezone(helsinki)
                                        self.time=hel.strftime(fmt)[11:20]+hel.strftime(fmt)[:10]
                        #               self.fix  = 1
                        #               print(self.time)
                                if array[0] == '$GNZDA':
                                        loc_time=utc.localize(datetime(int(array[4]), int(array[3]), int(array[2]), int(array[1][0:2]), int(array[1][2:4]), int(array[1][4:6])))
                                        #loc_time=utc.localize(datetime(2002, 10, 27, 6, 0, 0))
                                                #print('ok')
                                        hel = loc_time.astimezone(helsinki)
                                        self.time=hel.strftime(fmt)[11:20]+hel.strftime(fmt)[:10]
                        #               self.fix  = 1
                        #               print(self.time)
        #                               print(array)
                        except:
                                pass
        def write():
                myGNSS=GNSS()
                while(1):
                        myGNSS.read()
                #print(myGNSS.NMEA1)
                        try:
                                myGNSS.fix
                                myGNSS.time

                #print('Universal Time: ',myGPS.timeUTC)
                #print('You are Tracking: ',myGPS.sats,' satellites')
                        except AttributeError:
                                continue
                        else:
                                if (myGNSS.fix == 0):
                                        continue
                                if (myGNSS.fix != 0):
                                        break

                f=open("test0.txt","w")
                f.write("time:"+myGNSS.time)
                f.write("\nLat:"+myGNSS.latDeg)
                f.write("\nLong:"+myGNSS.longDeg)
                f.write("\nFix mode:"+str(myGNSS.fix))
                f.close()
except KeyboardInterrupt:
        NMEA=' '
        array=' '
        ser.reset_input_buffer()
        sys.exit()

