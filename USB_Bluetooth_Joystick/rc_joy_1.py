#!/usr/bin/python
# Joystick RC Car Controller
#
# Created by www.openmake.cc
#

import sys,os
import RPi.GPIO as gpio
import time
import logging

path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(path+'/log'):
    os.makedirs(path+'/log')
logging.basicConfig(filename=path+'/log/joystick.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', filemode='a', level=logging.INFO)

pipe = None

#Motor 1 GPIO Pin
IC1_A = 27
IC1_B = 22

#Motor 2 GPIO Pin
IC2_A = 17
IC2_B = 23

gpio.setmode(gpio.BCM)

#Motor Pin Setup
gpio.setup(IC1_A, gpio.OUT)
gpio.setup(IC1_B, gpio.OUT)
gpio.setup(IC2_A, gpio.OUT)
gpio.setup(IC2_B, gpio.OUT)

IS_PRINT_LOG = True

def LOG(level, message):
    if level is 'info':
        logging.info(message)
    if level is 'error':
        logging.error(message)
    if level is 'debug':
        logging.debug(message)
    if IS_PRINT_LOG:
        print(message)

def main():
    global pipe
    pipe = open('/dev/input/js0','r')

    readJoystick()

def readJoystick():
    action = []

    while 1:
        for character in pipe.read(1):
                action += ['%02X' % ord(character)]

                if len(action) == 8:

                        num = int(action[5], 16) # Translate back to integer form
                        percent254 = str(((float(num)-128.0)/126.0)-100)[4:6] # Calculate the percentage of push
                        percent128 = str((float(num)/127.0))[2:4]

                        LOG('debug','%s' % action)

                        if percent254 == '.0':
                                percent254 = '100'
                        if percent128 == '0':
                                percent128 = '100'

                        if action[6] == '01': # Button
                                if action[4] == '01':
                                        LOG('debug','You pressed button: ' + action[7])
                                        if action[7] == '00':
                                            pressRDPadLeft()
                                        if action[7] == '01':
                                            pressRDPadUp()
                                        if action[7] == '02':
                                            pressRDPadDown()
                                        if action[7] == '03':
                                            pressRDPadRight()

                                        if action[7] == '04':
                                            pressL1Button()
                                        if action[7] == '05':
                                            pressL2Button()
                                        if action[7] == '06':
                                            pressR1Button()
                                        if action[7] == '07':
                                            pressR2Button()

                                        if action[7] == '08':
                                            pressSelectButton()
                                        if action[7] == '09':
                                            pressStartButton()

                                else:
                                        LOG('debug','You released button: ' + action[7])
                                        if action[7] == '00':
                                            releaseRDPadLeft()
                                        if action[7] == '01':
                                            releaseRDPadUp()
                                        if action[7] == '02':
                                            releaseRDPadDown()
                                        if action[7] == '03':
                                            releaseRDPadRight()

                        ######
                        # Left D-pad Section
                        ######
                        # D-pad left/right
                        elif action[7] == '00': 
                                if action[4] == 'FF':
                                        pressLDPadRight()
                                elif action[4] == '01':
                                        pressLDPadLeft()
                                else:
                                        LOG('debug','You released the D-pad')
                                        releaseLDPadRight()

                        # D-pad up/down
                        elif action[7] == '01': 
                                if action[4] == 'FF':
                                        pressLDPadDown()
                                elif action[4] == '01':
                                        pressLDPadUp()
                                else:
                                        LOG('debug','You released the D-pad')
                                        releaseLDPadDown()


                        ######
                        # Left Joystick Section
                        ######
                        # Left Joystick left/right
                        elif action[7] == '04': 
                                if action[4] == 'FF':
                                        pressLJoyDigitalRight()
                                elif action[4] == '01':
                                        pressLJoyDigitalLeft()
                                else:
                                        LOG('debug','You released the left joystick')
                                        releaseLJoyDigitalRight()
                        # Left Joystick up/down
                        elif action[7] == '05': 
                                if action[4] == 'FF':
                                        pressLJoyDigitalDown()
                                elif action[4] == '01':
                                        pressLJoyDigitalUp()
                                else:
                                        LOG('debug','You released the left joystick')
                                        releaseLJoyDigitalDown()

                        ######
                        # Right Analog Joystick Section
                        ######
                        # Right Analog Joystick left/right
                        elif action[7] == '02': 
                                num = int(action[5], 16) # Translate back into integer form
                                if num >= 128:
                                        pressRJoyAnalogLeft()
                                elif num <= 127 \
                                and num != 0:
                                        pressRJoyDigitalRight()
                                else:
                                        LOG('debug','You stopped moving the right joystick')
                        # Right Analog Joystick up/ down
                        elif action[7] == '03': 
                                if num >= 128:
                                        pressRJoyAnalogUp()
                                elif num <= 127 \
                                and num != 0:
                                        pressRJoyAnalogDown()
                                else:
                                        LOG('debug','You stopped moving the right joystick')

                        action = []

######
# Left D-PAD
######
def pressLDPadLeft():
    LOG('debug', 'You Pressed Left button on LeftDPad ')
    turnLeft()
def pressLDPadRight():
    LOG('debug', 'You Pressed Right button on LeftDPad ')
    turnRight()
def pressLDPadUp():
    LOG('debug', 'You Pressed Up button on LeftDPad ')
    forword()
def pressLDPadDown():
    LOG('debug', 'You Pressed Down button on LeftDPad ')
    backword()

def releaseLDPadLeft():
    LOG('debug', 'You Released Left button on LeftDPad ')
    stopLR()
def releaseLDPadRight():
    LOG('debug', 'You Released Right button on LeftDPad ')
    stopLR()
def releaseLDPadUp():
    LOG('debug', 'You Released Up button on LeftDPad ')
    stopFB()
def releaseLDPadDown():
    LOG('debug', 'You Released Down button on LeftDPad ')
    stopFB()

######
# Left Joystick - Digital
######
def pressLJoyDigitalLeft():
    LOG('debug', 'You Controled Left on LeftJoystick Digital Mode ')
    turnLeft()
def pressLJoyDigitalRight():
    LOG('debug', 'You Controled Right on LeftJoystick Digital Mode ')
    turnRight()
def pressLJoyDigitalUp():
    LOG('debug', 'You Controled Up on LeftJoystick Digital Mode ')
    forword()
def pressLJoyDigitalDown():
    LOG('debug', 'You Controled Down on LeftJoystick Digital Mode ')
    backword()

def releaseLJoyDigitalLeft():
    LOG('debug', 'You Released Left on LeftJoystick Digital Mode ')
    stopLR()
def releaseLJoyDigitalRight():
    LOG('debug', 'You Released Right on LeftJoystick Digital Mode ')
    stopLR()
def releaseLJoyDigitalUp():
    LOG('debug', 'You Released Up on LeftJoystick Digital Mode ')
    stopFB()
def releaseLJoyDigitalDown():
    LOG('debug', 'You Released Down on LeftJoystick Digital Mode ')
    stopFB()

######
# Left Joystick - Analog
######
def pressLJoyAnalogLeft():
    LOG('debug', 'You Controled Left on LeftJoystick Analog Mode ')
def pressLJoyAnalogRight():
    LOG('debug', 'You Controled Right on LeftJoystick Analog Mode ')
def pressLJoyAnalogUp():
    LOG('debug', 'You Controled Up on LeftJoystick Analog Mode ')
def pressLJoyAnalogDown():
    LOG('debug', 'You Controled Down on LeftJoystick Analog Mode ')

######
# Right D-PAD
######
def pressRDPadLeft():
    LOG('debug', 'You Pressed Left button on RightDPad ')
    turnLeft()
def pressRDPadRight():
    LOG('debug', 'You Pressed Right button on RightDPad ')
    turnRight()
def pressRDPadUp():
    LOG('debug', 'You Pressed Up button on RightDPad ')
    forword()
def pressRDPadDown():
    LOG('debug', 'You Pressed Down button on RightDPad ')
    backword()

def releaseRDPadLeft():
    LOG('debug', 'You Released Left button on RightDPad ')
    stopLR()
def releaseRDPadRight():
    LOG('debug', 'You Released Right button on RightDPad ')
    stopLR()
def releaseRDPadUp():
    LOG('debug', 'You Released Up button on RightDPad ')
    stopFB()
def releaseRDPadDown():
    LOG('debug', 'You Released Down button on RightDPad ')
    stopFB()


######
# Right Joystick - Digital
######
def pressRJoyDigitalLeft():
    LOG('debug', 'You Controled Left on RightJoystick Digital Mode ')
    turnLeft()
def pressRJoyDigitalRight():
    LOG('debug', 'You Controled Right on RightJoystick Digital Mode ')
    turnRight()
def pressRJoyDigitalUp():
    LOG('debug', 'You Controled Up on RightJoystick Digital Mode ')
    forword()
def pressRJoyDigitalDown():
    LOG('debug', 'You Controled Down on RightJoystick Digital Mode ')
    backword()

def releaseRJoyDigitalLeft():
    LOG('debug', 'You Released Left on RightJoystick Digital Mode ')
    stopLR()
def releaseRJoyDigitalRight():
    LOG('debug', 'You Released Right on RightJoystick Digital Mode ')
    stopLR()
def releaseRJoyDigitalUp():
    LOG('debug', 'You Released Up on RightJoystick Digital Mode ')
    stopFB()
def releaseRJoyDigitalDown():
    LOG('debug', 'You Released Down on RightJoystick Digital Mode ')
    stopFB()

######
# Right Joystick - Analog
######
def pressRJoyAnalogLeft():
    LOG('debug', 'You Controled Left on RightJoystick Analog Mode ')
def pressRJoyAnalogRight():
    LOG('debug', 'You Controled Right on RightJoystick Analog Mode ')
def pressRJoyAnalogUp():
    LOG('debug', 'You Controled Up on RightJoystick Analog Mode ')
def pressRJoyAnalogDown():
    LOG('debug', 'You Controled Down on RightJoystick Analog Mode ')

######
# Other Buttons
######
def pressL1Button():    # Complete
    LOG('debug', 'You Pressed Left 1 Button')
def pressL2Button():    # Complete
    LOG('debug', 'You Pressed Left 2 Button')
def pressR1Button():    # Complete
    LOG('debug', 'You Pressed Right1 Button')
def pressR2Button():    # Complete
    LOG('debug', 'You Pressed Right 2 Button')
def pressSelectButton():
    LOG('debug', 'You Pressed Select Button')
def pressStartButton():
    LOG('debug', 'You Pressed Start Button')

def forword():
    LOG('info','GPIO Forward')
    gpio.output(IC2_A, gpio.LOW)
    gpio.output(IC2_B, gpio.HIGH)

def backword():
    LOG('info','GPIO Backward')
    gpio.output(IC2_A, gpio.HIGH)
    gpio.output(IC2_B, gpio.LOW)

def turnLeft():
    LOG('info','GPIO Turn Left')
    gpio.output(IC1_A, gpio.HIGH)
    gpio.output(IC1_B, gpio.LOW)

def turnRight():
    LOG('info','GPIO Turn Right')
    gpio.output(IC1_A, gpio.LOW)
    gpio.output(IC1_B, gpio.HIGH)

def stopFB():
    LOG('info','GPIO Stop Back Wheel')
    gpio.output(IC2_A, gpio.LOW)
    gpio.output(IC2_B, gpio.LOW)

def stopLR():
    LOG('info','GPIO Front Wheel Zero')
    gpio.output(IC1_A, gpio.LOW)
    gpio.output(IC1_B, gpio.LOW)

if __name__ == "__main__":
    main()
