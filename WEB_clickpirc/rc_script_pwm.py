# Imports
import webiopi
import time
from RPIO import PWM

# Enable debug output
webiopi.setDebug()


# 
M1_A = 4
M1_B = 17
M2_A = 27
M2_B = 22

DIR_STOP = 0
DIR_FW = 1
DIR_BW = 2

PWM_WIDTH = 1800

# Called by WebIOPi at script loading
def setup():
    webiopi.debug("Script with macros - Setup")

    # Setup PWM and DMA channel 0
    PWM.setup()
    PWM.init_channel(0)

# Looped by WebIOPi
def loop():
    # Toggle LED each 5 seconds
    webiopi.sleep(5)

# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("Script with macros - Destroy")

    # Shutdown all PWM and DMA activity
    PWM.cleanup()

# A macro without args which return nothing
@webiopi.macro
def MoveLeft():
    #Stop()
    LeftMotor(DIR_STOP)
    RightMotor(DIR_FW)

@webiopi.macro
def MoveRight():
    #Stop()
    RightMotor(DIR_STOP)
    LeftMotor(DIR_FW)

@webiopi.macro
def MoveForward():
    #Stop()
    LeftMotor(DIR_FW)
    RightMotor(DIR_FW)

@webiopi.macro
def MoveBackward():
    #Stop()
    LeftMotor(DIR_BW)
    RightMotor(DIR_BW)

@webiopi.macro
def Stop():
    # Stop PWM for specific GPIO on channel 0
    PWM.clear_channel_gpio(0, M1_A)
    PWM.clear_channel_gpio(0, M1_B)
    PWM.clear_channel_gpio(0, M2_A)
    PWM.clear_channel_gpio(0, M2_B)
    #webiopi.sleep(0.1)

def LeftMotor(dir):
    if dir == DIR_FW:
        PWM.add_channel_pulse(0, M1_B, 0, PWM_WIDTH)
        PWM.clear_channel_gpio(0, M1_A)

        webiopi.debug("Left FW")
    elif dir == DIR_BW:
        PWM.add_channel_pulse(0, M1_A, 0, PWM_WIDTH)
        PWM.clear_channel_gpio(0, M1_B)

        webiopi.debug("Left BW")
    else:
        PWM.clear_channel_gpio(0, M1_A)
        PWM.clear_channel_gpio(0, M1_B)

def RightMotor(dir):
    if dir == DIR_FW:
        PWM.add_channel_pulse(0, M2_B, 0, PWM_WIDTH)
        PWM.clear_channel_gpio(0, M2_A)
        
        webiopi.debug("Right FW")
    elif dir == DIR_BW:
        PWM.add_channel_pulse(0, M2_A, 0, PWM_WIDTH)
        PWM.clear_channel_gpio(0, M2_B)

        webiopi.debug("Right BW")
    else:
        PWM.clear_channel_gpio(0, M2_A)
        PWM.clear_channel_gpio(0, M2_B)
