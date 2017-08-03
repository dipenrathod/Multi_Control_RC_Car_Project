3axi3gyro
=========

3accelerator, 3gyro Sensor for Raspberrypi RC-Car

Project by www.rasplay.org - Multi-Control-RCCar

The original source code is https://github.com/cTn-dev/PyComms.git

This includes MPU6050 Control library, it's map based on Jeff Rowberg <jeff@rowberg.net> source code at
https://github.com/jrowberg/i2cdevlib/blob/master/Arduino/MPU6050/MPU6050.h

and PyComms MPU6050-i2c Control source Code, and RC Car with Raspberry-pi.

Dependency
I. HardWare
 1. RC Car with DC Motor
 2. Two Raspberry-pi, it is ultra-low-cost ($35) credit-card sized computer, can run Linux.
 3. Multi-Pi, it is Raspberry-pi extension Board, easy to connect DC Motor and it is like breadboard. Some sample in www.rasplay.org
 4. MPU6050 I2C Module, i2c protocol

II. SoftWare
 1. Using Python source code

III. Using Code
 1. at RaspberryPi on RC-Car
  $ git clone https://github.com/rasplay/3axi3gyro.git
  $ sudo python ./rccar_carside.py
  ( rccar side source needs only rccar_carside.py. other .py not used )
  ( Can insert Custom IP 
    - Usage : sudo python ./rccar_carside.py [192.168.0.2] )

 2. at RaspberryPi with MPU6050
  $ git clone https://github.com/rasplay/3axi3gyro.git
  $ sudo python ./rccar_contside.py 
  ( Can insert Custom IP 
    - Usage : sudo python ./rccar_contside.py [192.168.0.2] )

Enjoy!!
