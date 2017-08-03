touchpirc
=========

Touch Control for Raspberrypi RC-Car

Project by www.rasplay.org - Multi-Control-RCCar

The original source code is http://sebleedelisle.com/2011/04/multi-touch-game-controller-in-javascripthtml5-for-ipad,
git hub https://github.com/sebleedelisle/JSTouchController.



This is HTML5 Source Code for touch-pad device, and RC Car with Raspberry-pi.

Dependency
HW 
 1. RC Car with DC Motor
 2. Raspberry-pi, it is ultra-low-cost ($35) credit-card sized computer, can run Linux.
 3. Multi-Pi, it is Raspberry-pi extension Board, easy to connect DC Motor and it is like breadboard. Some sample in www.rasplay.org

SW
 1. Webiopi, it is Raspberry IO Web Software using Python, HTML5, JS.

I'm using in webiopi.
```
$ cd /usr/share/webiopi/htdocs/app
$ sudo git clone https://github.com/rasplay/touchpirc.git
```

Top of this file, you definite GPIO Number, ex.
4 = OUT
```
$ sudo vi /etc/webiopi/config
```

Run Web Brower, supported HTML5 (like Chrome browser)
```
http://[raspberrypi-IP:8000]/app/touchpirc/
```
You must type last '/'. 

Enjoy!!  
