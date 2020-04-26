echo "Installing User Mods"
pip3 install blynklib

sudo pip3 install adafruit-circuitpython-tsl2591
sudo pip3 install python-tsl2591
pip3 install adafruit-blinka

pip3 install adafruit-circuitpython-bme280
pip3 install adafruit-circuitpython-lis3dh
pip3 install adafruit-circuitpython-ads1x15
sudo pip3 install mh-z19
sudo apt-get install lxde
sudo apt-get install xterm -y


pip3 install adafruit-circuitpython-seesaw
git submodule init
git submodule update
git submodule foreach git fetch --all
git submodule foreach "tag=\$(git rev-list --exclude='*-*' --tags --max-count=1); git checkout -q \$tag"


pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U
