 
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pip
sudo apt-get install xterm -y
sudo apt full-upgrade -y
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo apt autoclean

pip3 install blynklib
pip3 install blynklib

pip3 install python-tsl2591
pip3 install board
pip3 install adafruit-circuitpython-bme280
pip3 install adafruit-circuitpython-lis3dh
pip3 install mh-z19
sudo apt-get install lxde

pip3 install adafruit-circuitpython-seesaw
git submodule init
git submodule update
git submodule foreach git fetch --all
git submodule foreach "tag=\$(git rev-list --exclude='*-*' --tags --max-count=1); git checkout -q \$tag"


mkdir /home/pi/.config/autostart
cp env.desktop /home/pi/.config/autostart/