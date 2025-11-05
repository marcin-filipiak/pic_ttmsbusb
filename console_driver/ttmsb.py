#!/usr/bin/python

import time
import serial
from time import gmtime, strftime
import json

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	port='/dev/ttyACM2',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

#ser.open()
ser.isOpen()

print """Enter your command:
           s - sound
           m - relay1 on/off
           n - relay2 on/off
           t - temperature
           l - left
           r - rigt
           d - down
           u - up
           y - read RTC
           a - set local time to RTC
           o - set manual RTC
           p - test
           x - reset uC cpu
         Insert "exit" to leave the application.\n"""

input=1
while 1 :
	# get keyboard input
	input = raw_input(">> ")
        if input == 'a':
		 ser.write('o')
		 x = strftime("%d", gmtime()) #pobranie dnia
                 x = str(unichr(int(x)))
                 ser.write(x)
		 x = strftime("%m", gmtime()) #pobranie miesiaca
                 x = str(unichr(int(x)))
                 ser.write(x)
		 x = strftime("%Y", gmtime()) #pobranie roku
                 x = str(unichr(int(x)-2000))
                 ser.write(x)
		 x = strftime("%H", gmtime()) #pobranie godziny
                 x = str(unichr(int(x)))
                 ser.write(x)
		 x = strftime("%M", gmtime()) #pobranie minut
                 x = str(unichr(int(x)))
                 ser.write(x)
		 x = strftime("%S", gmtime()) #pobranie sekund
                 x = str(unichr(int(x)))
                 ser.write(x)
        if input == 'x':
                ser.write(input + '')
                ser.close()
                exit()
	if input == 'exit':
		ser.close()
		exit()
        if input == 't':
                ser.write('t')
                time.sleep(1)
                sd = ''.join(ser.readlines())
                #print(type(sd))
                
                jdt = json.loads(sd)
                print("sensor 0 : "+jdt["0"]+"\n")
                print("sensor 1 : "+jdt["1"]+"\n")
                
                
                
                
	else:
		# send the character to the device
		# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
		ser.write(input + '')
		out = ''
		# let's wait one second before reading output (let's give device time to answer)
		time.sleep(1)
		while ser.inWaiting() > 0:
			out += ''.join(ser.readlines())
			
		if out != '':
			print "<< " + out + "\n"
