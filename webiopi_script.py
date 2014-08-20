# Imports
import webiopi
import time
import os, sys # mkdir(path)

HOME_DIR = '/home/pi/multicontrolRCCar'
lib_path = os.path.abspath(HOME_DIR)
sys.path.append(lib_path)

from Motor import Motor

# Enable debug output
#webiopi.setDebug()

# Retrieve GPIO lib
GPIO = webiopi.GPIO

global MOTOR1_PIN1
global MOTOR1_PIN2
global MOTOR2_PIN1
global MOTOR2_PIN2

MOTOR1_PIN1 = 4
MOTOR1_PIN2 = 17
MOTOR2_PIN1 = 27
MOTOR2_PIN2 = 22

""" RC Car Mode
" 0: Left Right DC Motor RCCar
" 1: Front Rear DC Motor RCCar
" 2: 4WD DC Motor RCCar
"""
global DC_LR_RCCAR
global DC_FR_RCCAR
global RCCar_Mode

global allGpsData
allGpsData = []

DC_LR_RCCAR = 0
DC_FR_RCCAR = 1
#DC_4WD_RCCAR = 2

RCCar_Mode = -1

# Called by WebIOPi at script loading
def setup():
    try:
        webiopi.debug("Script Motor Control")

        global refreshTimeInterval
        refreshTimeInterval = 0

        GPIO.setFunction(MOTOR1_PIN1, GPIO.OUT)
        GPIO.setFunction(MOTOR1_PIN2, GPIO.OUT)
        GPIO.setFunction(MOTOR2_PIN1, GPIO.OUT)
        GPIO.setFunction(MOTOR2_PIN2, GPIO.OUT)

        GPIO.digitalWrite(MOTOR1_PIN1, GPIO.LOW)
        GPIO.digitalWrite(MOTOR1_PIN2, GPIO.LOW)
        GPIO.digitalWrite(MOTOR2_PIN1, GPIO.LOW)
        GPIO.digitalWrite(MOTOR2_PIN2, GPIO.LOW)

    except Exception as Err:
        webiopi.debug('%s' % Err)

# Looped by WebIOPi
def loop():
    global motor1
    global motor2

    global RCCar_Mode
    global refreshTimeInterval
    global allGpsData

    try:
        if RCCar_Mode != -1:
            #webiopi.debug('goSync')
            motor1.syncMotorFromCommandStatus()
            motor2.syncMotorFromCommandStatus()

        webiopi.info('Read:%s' % getAllGpsData())

    except Exception as Err:
        webiopi.debug('%s' % Err)
    finally:
        # Cyclic Period
        webiopi.sleep(1)
        #refreshTimeInterval += 1

# Called by WebIOPi at server shutdown
def destroy():
    global MOTOR1_PIN1
    global MOTOR1_PIN2
    global MOTOR2_PIN1
    global MOTOR2_PIN2
    
    try:
        webiopi.debug("Script with macros - Destroy")
        # Reset GPIO functions
        GPIO.setFunction(MOTOR1_PIN1, GPIO.IN)
        GPIO.setFunction(MOTOR1_PIN2, GPIO.IN)
        GPIO.setFunction(MOTOR2_PIN1, GPIO.IN)
        GPIO.setFunction(MOTOR2_PIN2, GPIO.IN)
    except Exception as Err:
        webiopi.debug('%s' % Err)

def set2DCMotor():
    global motor1
    global motor2
    global MOTOR1_PIN1
    global MOTOR1_PIN2
    global MOTOR2_PIN1
    global MOTOR2_PIN2
    try:
        #webiopi.debug('set2DCMotor')
     
        motor1 = Motor(MOTOR1_PIN1, MOTOR1_PIN2)
        motor2 = Motor(MOTOR2_PIN1, MOTOR2_PIN2)
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def SetDCMotorLRRCCar():
    global RCCar_Mode
    global DC_LR_RCCAR

    try:
        webiopi.debug('SetDCMotorLRRCCar')
        set2DCMotor()
        RCCar_Mode = DC_LR_RCCAR
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def SetDCMotorFRRCCar():
    global RCCar_Mode
    global DC_FR_RCCAR
    try:
        webiopi.debug('SetDCMotorFRRCCar')
        set2DCMotor()
        RCCar_Mode = DC_FR_RCCAR
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def TurnLeft():
    global motor1
    global motor2
    global DC_LR_RCCAR
    global DC_FR_RCCAR
    global RCCar_Mode
    try:
        #webiopi.debug('TurnLeft')
        if RCCar_Mode == DC_LR_RCCAR:
            motor1.runMotorDirectionCCW()
            motor2.runMotorDirectionCCW()
        elif RCCar_Mode == DC_FR_RCCAR:
            motor1.runMotorDirectionCW()
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def TurnRight():
    global motor1
    global motor2
    global DC_LR_RCCAR
    global DC_FR_RCCAR
    global RCCar_Mode
    try:
        #webiopi.debug('TurnRight')
        if RCCar_Mode == DC_LR_RCCAR:
            motor1.runMotorDirectionCW()
            motor2.runMotorDirectionCW()
        elif RCCar_Mode == DC_FR_RCCAR:
            motor1.runMotorDirectionCCW()
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def MoveForward():
    global motor1
    global motor2
    global DC_LR_RCCAR
    global DC_FR_RCCAR
    global RCCar_Mode
    try:
        #webiopi.debug('MoveForward')
        if RCCar_Mode == -1:
            SetDCMotorLRRCCar()
        if RCCar_Mode == DC_LR_RCCAR:
            motor1.runMotorDirectionCW()
            motor2.runMotorDirectionCCW()
        elif RCCar_Mode == DC_FR_RCCAR:
            motor2.runMotorDirectionCCW()
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def MoveBackward():
    global motor1
    global motor2
    global DC_LR_RCCAR
    global DC_FR_RCCAR
    global RCCar_Mode
    try:
        #webiopi.debug('MoveBackward')
        if RCCar_Mode == -1:
            SetDCMotorLRRCCar()
        if RCCar_Mode == DC_LR_RCCAR:
            motor1.runMotorDirectionCCW()
            motor2.runMotorDirectionCW()
        elif RCCar_Mode == DC_FR_RCCAR:
            motor2.runMotorDirectionCW()
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def Stop():
    global motor1
    global motor2
    global RCCar_Mode
    try:
        #webiopi.debug('Stop')
        if RCCar_Mode == -1:
            SetDCMotorLRRCCar()
        motor1.stopMotor()
        motor2.stopMotor()
    except Exception as Err:
        webiopi.debug('%s' % Err)

# Not Used, Only use for old version Support
@webiopi.macro
def MoveLeft():
    global RCCar_Mode
    try:
        #webiopi.debug('MoveLeft')
        if RCCar_Mode == -1:
            SetDCMotorLRRCCar()
        TurnLeft()
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def MoveRight():
    global RCCar_Mode
    try:
        #webiopi.debug('MoveRight')
        if RCCar_Mode == -1:
            SetDCMotorLRRCCar()
        TurnRight()
    except Exception as Err:
        webiopi.debug('%s' % Err)

@webiopi.macro
def SetAllGpsData(gpsData):
    #webiopi.debug('SetAllGpsData')
    global allGpsData
    allGpsData = gpsData
    #webiopi.debug('set : %s' % allGpsData)

@webiopi.macro
def getAllGpsData():
    global allGpsData
    return allGpsData
