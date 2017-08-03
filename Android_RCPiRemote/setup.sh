#RCPiRemote Installation Scripts
# by fendergold@gmail.com , www.rasplay.org

# Install WebIOPi
cd ~
wget http://downloads.sourceforge.net/project/webiopi/WebIOPi-0.7.0.tar.gz
tar xvf WebIOPi-0.7.0.tar.gz
cd WebIOPi-0.7.0
sudo ./setup.sh

# Download Server Source
cd ~
git clone https://github.com/rasplay/clickpirc.git
sudo sed -i '/^#myscript=*/c\myscript=/home/pi/clickpirc/rc_script_2.py' /etc/webiopi/config

# WebIOPi Start
sudo /etc/init.d/webiopi start
# Auto Start WebIOPi at Raspberrypi startup
sudo update-rc.d webiopi defaults


# mjpeg with mmal Drive
# Install Defendencies
sudo apt-get install git cmake libjpeg8-dev imagemagick -y
sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h
# Install mjpg-streamer
cd ~
git clone https://github.com/liamfraser/mjpg-streamer
cd ~/mjpg-streamer/mjpg-streamer-experimental
make clean all
# Run mjpg-streamer
echo 'STREAMER_PATH=/home/pi/mjpg-streamer/mjpg-streamer-experimental' >> ~/runmjpgstream.sh
echo 'export LD_LIBRARY_PATH=$STREAMER_PATH' >> ~/runmjpgstream.sh
echo '$STREAMER_PATH/mjpg_streamer -i "input_raspicam.so -d 200 " -o "output_http.so -w $STREAMER_PATH/www -p 8080" &' >> ~/runmjpgstream.sh
sh ~/runmjpgstream.sh

