pip3 install blynklib

sudo pip3 install python-tsl2591
pip3 install adafruit-blinka

pip3 install adafruit-circuitpython-bme280
pip3 install adafruit-circuitpython-lis3dh
pip3 install Adafruit-ADS1x15
pip3 install mh-z19
sudo apt-get install lxde

pip3 install adafruit-circuitpython-seesaw
git submodule init
git submodule update
git submodule foreach git fetch --all
git submodule foreach "tag=\$(git rev-list --exclude='*-*' --tags --max-count=1); git checkout -q \$tag"
