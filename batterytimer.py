#!/usr/bin/env python

from urllib.request import urlopen
from datetime import datetime
import configparser

#read config
config = configparser.ConfigParser()
config.read('/app/batterytimer.ini')

def tactivate():
    statuslink = urlopen(config['TimerSection']['tasmota.status'])
    tasmotastatus = statuslink.read().decode('utf-8')
    if 'OFF' in tasmotastatus:
        switchlink = urlopen(config['TimerSection']['tasmota.switch'])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + retval)

def tdeactivate():
    statuslink = urlopen(config['TimerSection']['tasmota.status'])
    tasmotastatus = statuslink.read().decode('utf-8')
    if 'ON' in tasmotastatus:
        switchlink = urlopen(config['TimerSection']['tasmota.switch'])    
        retval = switchlink.read().decode('utf-8')
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' ' + retval)

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' timer1 check: ' + config['TimerSection']['tasmota.status'])
currentMonth = datetime.now().month
currentHour = datetime.now().hour
activation = config['TimerSection']['timer.'+str(currentMonth)]
fromTo = activation.split("-")
#activation during night
if currentHour >= int(fromTo[0]) or currentHour <= int(fromTo[1]):
    tactivate()
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' timer1 activated')
else:
    tdeactivate()
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' timer1 deactivated')
