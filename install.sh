sudo apt-get update && sudo apt-get upgrade

sudo apt-get install python-pip

sudo pip3 install blynklib

sudo pip3 install python-tsl2591
sudo pip3 install board
sudo pip3 install adafruit-circuitpython-bme280
sudo pip3 install adafruit-circuitpython-lis3dh
sudo pip3 install mh-z19

sudo pip3 install adafruit-circuitpython-seesaw
git submodule init
git submodule update
git submodule foreach git fetch --all
git submodule foreach "tag=\$(git rev-list --exclude='*-*' --tags --max-count=1); git checkout -q \$tag"


sudo apt-get install xterm -y

mkdir /home/pi/.config/autostart
cp soil.desktop /home/pi/.config/autostart/