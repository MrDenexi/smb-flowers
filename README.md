# smb-flowers

To be ran on an Raspberry Pi with a rasberry pi connected on ttyUSB0

### structure
* main.py         Entry point of program
* app.py          Where most of th magic happens
* launch.sh       Point a cronjob on startup to this file to start on 


* db/db.py       sqlite database management files
* db/models.py   database models


* arduino/*      All the arduino states


* samples/*      Simple scripts to debug


Can be ran using anaconda with (environment.yml) or just use pip (requirements.txt)
