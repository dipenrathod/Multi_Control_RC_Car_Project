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
        print('__init__')

        self.MOTOR_MODE = motorMode
        self.PIN1_NO = pin1_no
        self.PIN2_NO = pin2_no

        self.gpioInit()

    def gpioInit(self):
        print('gpioInit')
        GPIO.setmode(GPIO.BCM)
        if self.MOTOR_MODE is self.DC_MOTOR:
            # Setup GPIOs
            # Use BCM GPIO references
            # instead of physical pin numbers
            GPIO.setup(self.PIN1_NO , GPIO.OUT)
            GPIO.setup(self.PIN2_NO, GPIO.OUT)

    def syncMotorFromCommandStatus(self):
        print('syncMotorFromCommandStatus')
        print('%d, %d, %d, %d' % (self.MOTOR_MODE, self.DC_MOTOR, self.getPinStatus(), self.getCommandStatus()))
        if self.MOTOR_MODE is self.DC_MOTOR:
            print('%d, %d, %d' % (self.getPinStatus(), self.getCommandStatus(), self.getMotorStatus()))
            if self.getPinStatus() != self.getCommandStatus():
                if self.getCommandStatus() > 0:
                    self.setDCMotorStatusCW()
                elif self.getCommandStatus() < 0:
                    self.setDCMotorStatusCCW()
                else:
                    self.setDCMotorStatusStop()

    def setCommandStatus(self, speed=0):
        print('setCommandStatus')
        self.Command_Status = speed

    def getCommandStatus(self):
        print('getCommandStatus')
        return self.Command_Status

    def getMotorStatus(self):
        print('getMotorStatus')
        return self.Motor_Status

    def getPinStatus(self):
        print('getPinStatus')
        print('PinStatus %d, %d' % (GPIO.input(self.PIN1_NO), GPIO.input(self.PIN2_NO)))
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
        print('runMotorDirectionCW')
        if self.MOTOR_MODE == self.DC_MOTOR:
            print('self.MOTOR_MODE == self.DC_MOTOR')
            self.setCommandStatus(speed)

    def runMotorDirectionCCW(self, speed=-1):
        print('runMotorDirectionCCW')
        if self.MOTOR_MODE == self.DC_MOTOR:
            self.setCommandStatus(speed)

    def stopMotor(self):
        print('stopMotor')
        if self.MOTOR_MODE == self.DC_MOTOR:
            self.setCommandStatus(0)

    """ DC MOTOR MODE Function
    " this is private.
    """ 
    def syncDCMotorStatusFromPinStatus(self):
        print('syncDCMotorStatusFromPinStatus')
        self.Motor_Status = self.getPinStatus()

    def setDCMotorStatusStop(self):
        print('setDCMotorStatusStop')
        if self.MOTOR_MODE is not self.DC_MOTOR:
            return
        print('%d, %d' % (self.PIN1_NO, self.PIN2_NO))
        GPIO.output(self.PIN1_NO, GPIO.LOW)
        GPIO.output(self.PIN2_NO, GPIO.LOW)
        time.sleep(0.01)
        self.syncDCMotorStatusFromPinStatus()

    def setDCMotorStatusCW(self):
        print('setDCMotorStatusCW')
        if self.MOTOR_MODE is not self.DC_MOTOR:
            return
        GPIO.output(self.PIN1_NO, GPIO.LOW)
        time.sleep(0.01)
        if not GPIO.input(self.PIN1_NO):
            GPIO.output(self.PIN2_NO, GPIO.HIGH)
            time.sleep(0.01)
            self.syncDCMotorStatusFromPinStatus()

    def setDCMotorStatusCCW(self):
        print('setDCMotorStatusCCW')
        if self.MOTOR_MODE is not self.DC_MOTOR:
            return
        GPIO.output(self.PIN2_NO, GPIO.LOW)
        time.sleep(0.01)
        if not GPIO.input(self.PIN2_NO):
            GPIO.output(self.PIN1_NO, GPIO.HIGH)
            time.sleep(0.01)
            self.syncDCMotorStatusFromPinStatus()