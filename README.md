# PiTempsReader

Script to read temps from 2 sensors on a raspberry pie and store the current temps in a file and also display them on an CharLCD

To run it as a daemon on raspbian:
**********************************
- copy the pitempsreader.py python file into /usr/local/bin/pitempsreader (or change the initscript)
- copy the initscript into /etc/init.d/
- make both files executable (chmod 755)
now you can control the script with the command 'sudo service pitempsreader <start|stop|status|etc>'

if you wan't it to run automagically at boot you have to run the following command:
sudo update-rc pitempsreader defaults
