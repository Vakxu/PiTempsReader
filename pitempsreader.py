#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script for reading temp & Humidity information from BMP085 and DHT22
# sensors on an Raspberry PI.
# This program updates the current temp/humidity in a file that you can
# specify in the variables and also displays the current temp and time
# on an character LCD. For running it on an raspberryPI with an SD-card
# it is suggested to use ramdisk to limit the writes to the SD-card.

# Original Adafruit_DHT&BMP scripts by Tony DiCola used as starting point
# Script modified by vaxaren(ATmbnet.fi)
# **************************

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import Adafruit_CharLCD as LCD
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import signal
import os
import time

clean_state = True
shutdown_flag = False
temps_in,temps_out = [], []

def signal_handler(signum, frame):
    print 'PiTempsReader: Received signal',signum,'exiting...'
    clearLCD_shutdown()
    if clean_state: exit()
    global shutdown_flag
    shutdown_flag = True

def ensure_dir_exists(d):
    if not os.path.exists(d):
        os.mkdir(d)

def readFromFile(f):
    if not os.path.isfile(f):
        return None
    file = open(f, 'r')
    temp = file.read()
    file.close()
    return temp

def writeToFile(f,t):
    with open(f, 'w') as f:
        f.write(t)

def updateLCD(tin,tout,humout):
    message = 'In : {0}\x00C\nOut: {1}\x00C/{2}%\n\n{3}'
    lcd.clear()
    lcd.message(message.format(tin, tout, humout, time.strftime('%d.%m.%Y %H:%M')))

def clearLCD_shutdown():
    lcd.clear()
    lcd.message('Shutted down at:\n{0}'.format(time.strftime('%d.%m.%Y %H:%M')))

def update_temps_lists(lin, tin, lout, tout):
    # Store a 2 hour long history of temps
    def limit_history(l):
        if len(l) > 120: del l[0]
    lin.append(float(tin))
    lout.append(float(tout))
    limit_history(lin)
    limit_history(lout)

# Catch a SIGTERM signal if sent and
# exit cleanly
signal.signal(signal.SIGTERM, signal_handler)
# Catch a SIGINT(CTRL+C)
signal.signal(signal.SIGINT, signal_handler)

# LCD Pins
lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = None #4
# DHT 22 Sensor pin
pin           = 4
# LCD columns and row size definitions
lcd_columns   = 20
lcd_rows      = 4
# Files
working_dir   = "/tmp/pitemps"
file_out      = "/outside"
file_in       = "/inside"
fout = working_dir + file_out
fin = working_dir + file_in
ensure_dir_exists(working_dir)

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
# *********************************************
# Sensor2 shall always be BMP085, using default
# I2C bus on Raspberry PI main GPIO
sensor = Adafruit_DHT.DHT22
sensor2 = BMP085.BMP085()

# Initialize the LCD
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
lcd.create_char(0, [0xc,0x12,0x12,0xc,0x0,0x0,0x0,0x0]) #degree char in \x00
lcd.clear()

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
#humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    inside = sensor2.read_temperature()
    if humidity is not None and temperature is not None and inside is not None:
	temperature = "{0:0.2f}".format(temperature)
	humidity = "{0:0.2f}".format(humidity)
	outside = temperature + "\n" + humidity
	inside = "{0:0.2f}".format(inside)
	update_temps_lists(temps_in, inside, temps_out, temperature)
	updateLCD(inside,temperature,humidity)
	clean_state = False
	writeToFile(fout, outside)
	writeToFile(fin, inside)
	clean_state = True
	if shutdown_flag: break
    else:
	pass
    # update temps once per minute
    time.sleep(60 - time.localtime()[5])
