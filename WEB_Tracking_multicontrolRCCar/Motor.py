import time
import RPi.GPIO as GPIO
#import webiopi

# Retrieve GPIO lib
#GPIO = webiopi.GPIO

class Motor:

    """ Motor Pin
    " Motor has 2 Pins
    """
    PIN1_NO = -1
    PIN2_NO = -1

    """ MotorMode
    """
    DC_MOTOR = 0  # Normal DC Motor
    PWM_MOTOR = 1 # Using DC Motor 
    MOTOR_MODE = DC_MOTOR

    #""" Pin Status
    #" GPIO Pin Status
    #"""
    #Pin1_Status = False
    #Pin2_Status = False

    """ MotorStatus
    " Positive : Run CW
    " Zero : Stop
    " Negative : Run CCW
    """
    Motor_Status = 0

    """ CurrentCommand
    " Positive : Run CW
    " Zero : Stop
    " Negative : Run CCW
    """
    Command_Status = 0

    def __init__(self, pin1_no, pin2_no, motorMode=0):
        #webiopi.debug('__init__')

        self.MOTOR_MODE = motorMode
        self.PIN1_NO = pin1_no
        self.PIN2_NO = pin2_no

        self.gpioInit()

    def gpioInit(self):
        #webiopi.debug('gpioInit')
        GPIO.setmode(GPIO.BCM)
        if self.MOTOR_MODE is self.DC_MOTOR:
            # Setup GPIOs
            # Use BCM GPIO references
            # instead of physical pin numbers
            GPIO.setup(self.PIN1_NO , GPIO.OUT)
            GPIO.setup(self.PIN2_NO, GPIO.OUT)

    def syncMotorFromCommandStatus(self):
        #webiopi.debug('syncMotorFromCommandStatus')
        #webiopi.debug('%d, %d, %d, %d' % (self.MOTOR_MODE, self.DC_MOTOR, self.getPinStatus(), self.getCommandStatus()))
        if self.MOTOR_MODE is self.DC_MOTOR:
            #webiopi.debug('%d, %d, %d' % (self.getPinStatus(), self.getCommandStatus(), self.getMotorStatus()))
            if self.getPinStatus() != self.getCommandStatus():
                if self.getCommandStatus() > 0:
                    self.setDCMotorStatusCW()
                elif self.getCommandStatus() < 0:
                    self.setDCMotorStatusCCW()
                else:
                    self.setDCMotorStatusStop()

    def setCommandStatus(self, speed=0):
        #webiopi.debug('setCommandStatus')
        self.Command_Status = speed

    def getCommandStatus(self):
        #webiopi.debug('getCommandStatus')
        return self.Command_Status

    def getMotorStatus(self):
        #webiopi.debug('getMotorStatus')
        return self.Motor_Status

    def getPinStatus(self):
        #webiopi.debug('getPinStatus')
        #webiopi.debug('PinStatus %d, %d' % (GPIO.input(self.PIN1_NO), GPIO.input(self.PIN2_NO)))
        if self.MOTOR_MODE is self.DC_MOTOR:
            if GPIO.input(self.PIN1_NO) and not GPIO.input(self.PIN2_NO):
                return -1
            elif not GPIO.input(self.PIN1_NO) and GPIO.input(self.PIN2_NO):
                return 1
            else:
                return 0

    """ Any Motor used Function
    """
    def runMotorDirectionCW(self, speed=1):
        #webiopi.debug('runMotorDirectionCW')
        if self.MOTOR_MODE is self.DC_MOTOR:
            self.setCommandStatus(speed)

    def runMotorDirectionCCW(self, speed=-1):
        #webiopi.debug('runMotorDirectionCCW')
        if self.MOTOR_MODE is self.DC_MOTOR:
            self.setCommandStatus(speed)

    def stopMotor(self):
        #webiopi.debug('stopMotor')
        if self.MOTOR_MODE is self.DC_MOTOR:
            self.setCommandStatus(0)

    """ DC MOTOR MODE Function
    " this is private.
    """ 
    def syncDCMotorStatusFromPinStatus(self):
        #webiopi.debug('syncDCMotorStatusFromPinStatus')
        self.Motor_Status = self.getPinStatus()

    def setDCMotorStatusStop(self):
        #webiopi.debug('setDCMotorStatusStop')
        if self.MOTOR_MODE is not self.DC_MOTOR:
            return
        #webiopi.debug('%d, %d' % (self.PIN1_NO, self.PIN2_NO))
        GPIO.output(self.PIN1_NO, GPIO.LOW)
        GPIO.output(self.PIN2_NO, GPIO.LOW)
        time.sleep(0.01)
        self.syncDCMotorStatusFromPinStatus()

    def setDCMotorStatusCW(self):
        #webiopi.debug('setDCMotorStatusCW')
        if self.MOTOR_MODE is not self.DC_MOTOR:
            return
        GPIO.output(self.PIN1_NO, GPIO.LOW)
        time.sleep(0.01)
        if not GPIO.input(self.PIN1_NO):
            GPIO.output(self.PIN2_NO, GPIO.HIGH)
            time.sleep(0.01)
            self.syncDCMotorStatusFromPinStatus()

    def setDCMotorStatusCCW(self):
        #webiopi.debug('setDCMotorStatusCCW')
        if self.MOTOR_MODE is not self.DC_MOTOR:
            return
        GPIO.output(self.PIN2_NO, GPIO.LOW)
        time.sleep(0.01)
        if not GPIO.input(self.PIN2_NO):
            GPIO.output(self.PIN1_NO, GPIO.HIGH)
            time.sleep(0.01)
            self.syncDCMotorStatusFromPinStatus()

