#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time
import sys
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_CharLCD as LCD
import GNSSDecode
import importlib
left="P9_12"
right="P9_14"
top="P9_16"
bottom="P9_18"
GPIO.setup(top, GPIO.IN)
GPIO.setup(bottom, GPIO.IN)
GPIO.setup(right, GPIO.IN)
GPIO.setup(left, GPIO.IN)
time.sleep(0.1)
lcd_rs        = 'P8_8'
lcd_en        = 'P8_10'
lcd_d4        = 'P8_18'
lcd_d5        = 'P8_16'
lcd_d6        = 'P8_14'
lcd_d7        = 'P8_12'
lcd_backlight = 'P8_7'

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 20
lcd_rows    = 4
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#time.sleep(0.05)
try:
	def findMax(array, k, h):
                max = len(array[k])
                for i in range (k,h):
                        if len(array[i])>max:
                                max = len(array[i])
                return max
        def printLCD(list, a, b, i, columns):
                h=0
                c=i-columns
                for n in range(a,b):
                        d=c
                        x= len(list[n][c:])
                        if c >= len(list[n]):
                                for m in range(0,columns):
                                        lcd.set_cursor(m,h)
                                        lcd.message(' ')
                        else:
                                if x>=columns:
                                        for m in range(0,columns):
                                                lcd.set_cursor(m,h)
                                                lcd.message(list[n][d])
                                                d=d+1
                                else:

                                        for m in range(0,x):
                                                lcd.set_cursor(m,h)
                                                lcd.message(list[n][d])
                                                d=d+1
                                        for m in range(x,columns):
                                                lcd.set_cursor(m,h)
                                                lcd.message(' ')
                                h=h+1
        a = 0
        b = lcd_rows
        i=lcd_columns
        while(1):
                importlib.reload(GNSSDecode)
                GNSSDecode.write()
                timeout = time.time()+0.9
                file1 = open("test0.txt","r+")
                message = file1.read()
                message = message[:-1]
                file1.close()
                array = message.split('\n')
                x=len(array)
                message = file1.read()
                message = message[:-1]
                file1.close()
                array = message.split('\n')
                x=len(array)
                if a in range (0,len(array)) and b in range (0,len(array)+1):
                        max = findMax(array, a, b)
                else:
                        continue
                printLCD(array, a, b, i, lcd_columns)
                #time.sleep(0.05)
                while (lcd_d7 == 1):
                        pass
                while(1):
                        if i < max and GPIO.input(right):
                                i=i+1
                                printLCD(array, a, b, i, lcd_columns)
                                #time.sleep(0.08)
                                while (lcd_d7 == 1):
                                        pass
                                continue
                        if i > lcd_columns and GPIO.input(left):
                                i=i-1
                                printLCD(array, a, b, i, lcd_columns)
                                #time.sleep(0.08)
                                while(lcd_d7 == 1):
                                        pass
                                continue
                        if b < x and GPIO.input(bottom):
                                a=a+1
                                b=b+1
                                printLCD(array, a, b, i, lcd_columns)
                                while(lcd_d7 == 1):
                                        pass
                                max = findMax(array, a, b)
                        if b > lcd_rows and GPIO.input(top):
                                a=a-1
                                b=b-1
                                printLCD(array, a, b, i, lcd_columns)
                                while(lcd_d7 == 1):
                                        pass
                                max = findMax(array, a, b)
                                time.sleep(0.08)
                                continue

                        if time.time() > timeout:
                                break
                        #time.sleep(0.01)
except KeyboardInterrupt:
        GPIO.cleanup()
        lcd.clear()


