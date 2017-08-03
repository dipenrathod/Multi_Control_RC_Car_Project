# Imports
import webiopi
import time

# Enable debug output
webiopi.setDebug()

# Retrieve GPIO lib
GPIO = webiopi.GPIO

# Two LB1630
M1_A = 4
M1_B = 17
M2_A = 27
M2_B = 22

DIR_FW = 1
DIR_BW = 0

# Called by WebIOPi at script loading
def setup():
    webiopi.debug("Script with macros - Setup")
    # Setup GPIOs
    GPIO.setFunction(M1_A, GPIO.OUT)
    GPIO.setFunction(M1_B, GPIO.OUT)
    GPIO.setFunction(M2_A, GPIO.OUT)
    GPIO.setFunction(M2_B, GPIO.OUT)

    GPIO.digitalWrite(M1_A, GPIO.LOW)
    GPIO.digitalWrite(M1_B, GPIO.LOW)
    GPIO.digitalWrite(M2_A, GPIO.LOW)
    GPIO.digitalWrite(M2_B, GPIO.LOW)

# Looped by WebIOPi
def loop():
    # Toggle LED each 5 seconds
    webiopi.sleep(5)

# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("Script with macros - Destroy")
    # Reset GPIO functions
    GPIO.setFunction(M1_A, GPIO.IN)
    GPIO.setFunction(M1_B, GPIO.IN)
    GPIO.setFunction(M2_A, GPIO.IN)
    GPIO.setFunction(M2_B, GPIO.IN)

# A macro without args which return nothing
@webiopi.macro
def MoveLeft():
    Stop()
    #GPIO.digitalWrite(M1_A, GPIO.LOW)
    #GPIO.digitalWrite(M1_B, GPIO.LOW)
    #GPIO.digitalWrite(M2_A, GPIO.LOW)
    #GPIO.digitalWrite(M2_B, GPIO.HIGH)
    RightMotor(DIR_FW)

@webiopi.macro
def MoveRight():
    Stop()
    #GPIO.digitalWrite(M1_A, GPIO.LOW)
    #GPIO.digitalWrite(M1_B, GPIO.HIGH)
    #GPIO.digitalWrite(M2_A, GPIO.LOW)
    #GPIO.digitalWrite(M2_B, GPIO.LOW)
    LeftMotor(DIR_FW)

@webiopi.macro
def MoveForward():
    Stop()
    #GPIO.digitalWrite(M1_A, GPIO.LOW)
    #GPIO.digitalWrite(M1_B, GPIO.HIGH)
    #GPIO.digitalWrite(M2_A, GPIO.LOW)
    #GPIO.digitalWrite(M2_B, GPIO.HIGH)
    LeftMotor(DIR_FW)
    RightMotor(DIR_FW)

@webiopi.macro
def MoveBackward():
    Stop()
    #GPIO.digitalWrite(M1_A, GPIO.HIGH)
    #GPIO.digitalWrite(M1_B, GPIO.LOW)
    #GPIO.digitalWrite(M2_A, GPIO.HIGH)
    #GPIO.digitalWrite(M2_B, GPIO.LOW)
    LeftMotor(DIR_BW)
    RightMotor(DIR_BW)

@webiopi.macro
def Stop():
    while True:
        if GPIO.digitalRead(M1_A):
            GPIO.digitalWrite(M1_A, GPIO.LOW)
        if GPIO.digitalRead(M1_B):
            GPIO.digitalWrite(M1_B, GPIO.LOW)
        if GPIO.digitalRead(M2_A):
            GPIO.digitalWrite(M2_A, GPIO.LOW)
        if GPIO.digitalRead(M2_B):
            GPIO.digitalWrite(M2_B, GPIO.LOW)
        webiopi.sleep(0.1)
        if not GPIO.digitalRead(M1_A) and not GPIO.digitalRead(M1_B) and not GPIO.digitalRead(M2_A) and not GPIO.digitalRead(M2_B):
            break

def LeftMotor(dir):
    if dir:
        while GPIO.digitalRead(M1_A):
            GPIO.digitalWrite(M1_A, GPIO.LOW)
            webiopi.sleep(0.1)
        GPIO.digitalWrite(M1_B, GPIO.HIGH)
        webiopi.sleep(0.1)
    else:
        while GPIO.digitalRead(M1_B):
            GPIO.digitalWrite(M1_B, GPIO.LOW)
            webiopi.sleep(0.1)
        GPIO.digitalWrite(M1_A, GPIO.HIGH)
        webiopi.sleep(0.1)

def RightMotor(dir):
    if dir:
        while GPIO.digitalRead(M2_A):
            GPIO.digitalWrite(M2_A, GPIO.LOW)
            webiopi.sleep(0.1)
        GPIO.digitalWrite(M2_B, GPIO.HIGH)
        webiopi.sleep(0.1)
    else:
        while GPIO.digitalRead(M2_B):
            GPIO.digitalWrite(M2_B, GPIO.LOW)
            webiopi.sleep(0.1)
        GPIO.digitalWrite(M2_A, GPIO.HIGH)
        webiopi.sleep(0.1)
