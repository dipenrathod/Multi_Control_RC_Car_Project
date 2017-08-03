DCMotorKeyControl
=========

Simple Keyboard Control for Raspberrypi RC-Car

Project by www.rasplay.org - Multi-Control-RCCar

This is C Source Code for RC Car with Raspberry-pi.

Dependency

HW

 1. RC Car with DC Motor
 2. Raspberry-pi, it is ultra-low-cost ($35) credit-card sized computer, can run Linux.

SW

 1. wiringPi, Library for Raspberry Pi GPIO Control

Installation wiringPi Source

  ```
  $ git clone git://git.drogon.net/wiringPi
  $ cd wiringPi
  $ ./build
  ```

Test wiringPi

  ```
  $ gpio -v
  ```

DCMotorKeyControl Clone

  ```
  $ git clone https://github.com/rasplay/DCMotorKeyControl.git
  $ cd DCMotorKeyControl
  ```

choose one source code and compile/run.

  * rc_key_1.c use two motors, one is front-rear motor, the other is left-right motor.

  ```
  $ gcc -o rc_key rc_key_1.c -lwiringPi
  $ sudo ./rc_key
  ```

  * rc_key_2.c use two motors, one is left motor, the other is right motor.

  ```
  $ gcc -o rc_key rc_key_2.c -lwiringPi
  $ sudo ./rc_key
  ```

  * rc_key_2.py use two motors, one is left motor, the other is right motor.

  ```
  $ sudo python rc_key_2.py
  ```

Enjoy!!  
