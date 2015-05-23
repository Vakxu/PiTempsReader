# PiTempsReader
Script to read temps from 2 sensors on a raspberry pie and store the current temps in a file
to use in another apps, and also display them on an CharLCD.

Needed libraries:
- https://github.com/adafruit/Adafruit_Python_CharLCD
- https://github.com/adafruit/Adafruit_Python_DHT
- https://github.com/adafruit/Adafruit_Python_BMP

And also of course the equivavelnt sensors and an character lcd display. Feel free to modify 
it as you wish, for example for other sensors or just make better code, commits needed! ;)

To run it as a daemon on raspbian:
**********************************
- copy the pitempsreader.py python file into /usr/local/bin/pitempsreader/ (or change the initscript path)
- copy the initscript into /etc/init.d/
- make both files executable (chmod 755)
now you can control the script with the command 'sudo service pitempsreader <start|stop|status|etc>'

if you want to run it automagically at boot you have to run the following command:
- 'sudo update-rc pitempsreader defaults'
