#!/usr/bin/python
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import os, sys # mkdir(path)
from webiopi.clients import *

import gps

class Gpsreceive:

    def __init__(self):
        # Listen on port 2947 (gpsd) of localhost
        global session
        session = gps.gps("localhost", "2947")
        session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        self.nowGpsdata = []


    def readData(self):
        global session
        try:
            report = session.next()

            # Wait for a 'TPV' report and display the current time
            # To see all report data, uncomment the line below
                
            #print (report)
            if report['class'] == 'TPV':
                if hasattr(report, 'epx'):
                    self.gpsepx = report.epx
                    #print ('Time:%s' % report.epx)
                if hasattr(report, 'epy'):
                    self.gpsepy = report.epy
                    #print ('Time:%s' % report.epy)
                if hasattr(report, 'epv'):
                    self.gpsepv = report.epv
                    #print ('Time:%s' % report.epv)
                if hasattr(report, 'ept'):
                    self.gpsept = report.ept
                    #print ('Time:%s' % report.ept)
                if hasattr(report, 'lon'):
                    self.gpslon = report.lon
                    #print ('Lon:%f' % report.lon)
                if hasattr(report, 'eps'):
                    self.gpseps = report.eps
                    #print ('Time:%s' % report.eps)
                if hasattr(report, 'lat'):
                    self.gpslat = report.lat
                    #print ('Lat:%f' % report.lat)
                    #print ('%6.3f' % (report.lat))
                if hasattr(report, 'tag'):
                    self.gpstag = report.tag
                    #print ('Time:%s' % report.tag)
                if hasattr(report, 'track'):
                    self.gpstrack = report.track
                    #print ('Time:%s' % report.track)
                if hasattr(report, 'mode'):
                    self.gpsmode = report.mode
                    #print ('Time:%s' % report.mode)
                if hasattr(report, 'time'):
                    self.gpstime = report.time
                    #print ('Time:%s' % report.time)
                if hasattr(report, 'device'):
                    self.gpsdevice = report.device
                    #print ('Time:%s' % report.device)
                if hasattr(report, 'climb'):
                    self.gpsclimb = report.climb
                    #print ('Time:%s' % report.climb)
                if hasattr(report, 'alt'):
                    self.gpsalt = report.alt
                    #print ('Time:%s' % report.alt)
                if hasattr(report, 'speed'):
                    self.gpsspeed = report.speed
                    #print ('Time:%s' % report.speed)
            else:
                print ('GPS Signal not found')
        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print ("GPSD has terminated")

    def setAllData(self):
        try:
            alldata = []
            alldata.append(self.gpsepx)
            alldata.append(self.gpsepy)
            alldata.append(self.gpsepv)
            alldata.append(self.gpsept)
            alldata.append(self.gpslon)
            alldata.append(self.gpseps)
            alldata.append(self.gpslat)
            alldata.append(self.gpstag)
            alldata.append(self.gpstrack)
            alldata.append(self.gpsmode)
            alldata.append(self.gpstime)
            alldata.append(self.gpsdevice)
            alldata.append(self.gpsclimb)
            alldata.append(self.gpsalt)
            alldata.append(self.gpsspeed)
            self.nowGpsdata = alldata
        except AttributeError:
            print ("getAllData AttributeError")

    def getAllData(self):
        return self.nowGpsdata

if __name__ == '__main__':

    while True:
        try:
            # Create a WebIOPi client
            client = PiHttpClient("localhost")
            client.setCredentials("webiopi", "raspberry")
            sleep(1)

            macroclient = Macro(client, 'SetAllGpsData')

            gpsreceive = Gpsreceive()
            while True:
                try:
                    gpsreceive.readData()
                    gpsreceive.setAllData()
                    #sendData = gpsreceive.getAllData()
                    sendData = ''
                    sendData += ('%.3f_' % gpsreceive.gpsepx)
                    sendData += ('%.3f_' % gpsreceive.gpsepy)
                    sendData += ('%.3f_' % gpsreceive.gpsepv)
                    sendData += ('%.3f_' % gpsreceive.gpsept)
                    sendData += ('%.3f_' % gpsreceive.gpslon)
                    sendData += ('%.3f_' % gpsreceive.gpseps)
                    sendData += ('%.3f_' % gpsreceive.gpslat)
                    sendData += ('%s' % gpsreceive.gpstag)
                    sendData += ('%.3f_' % gpsreceive.gpstrack)
                    sendData += ('%.3f_' % gpsreceive.gpsmode)
                    sendData += ('%s' % gpsreceive.gpstime)
                    #sendData += ('%s' % gpsreceive.gpsdevice)
                    sendData += ('%.3f_' % gpsreceive.gpsclimb)
                    sendData += ('%.3f_' % gpsreceive.gpsalt)
                    sendData += ('%.3f' % gpsreceive.gpsspeed)
                    response = macroclient.call(sendData)
                    print (sendData)
                except AttributeError:
                    print ("getAllData AttributeError")

        except Exception as Error:
            print ("Exception Error: %s" % Error) 
            client = None
            gpsreceive = None
            sleep(1)

