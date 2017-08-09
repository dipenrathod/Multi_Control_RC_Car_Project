# How to  wii remote & nun-chuck for Raspberrypi
```
$ sudo apt-get install bluetooth vorbis-tools python-cwiid wminput
```
```
$ sudo nano /etc/udev/rules.d/wiimote.rules
```
> **add line :**   
   KERNEL=="uinput", MODE:="0666"
  exit : ctrl + x save
```
$ git clone https://github.com/rasplay/wii_rpi
```
```
$ cd wii_rpi
```
```
$ sudo chmod 775 /home/pi/attachwii.sh
```
```
$ sudo nano /etc/rc.local
```
> **add line** :
   su -c pi /home/pi/attachwii.sh
   sleep 3
   su -c pi /home/pi/DCMotorJoystickControl/rc_joy_1.py

exit : ctrl + x save
