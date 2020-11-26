echo "Installing User Mods"
pip3 install blynklib

#Cairo graphics library
apt-get install libcairo2-dev -y 
# TSL2591 high precision light sensor
sudo pip3 install adafruit-circuitpython-tsl2591
#think python one is unused
sudo pip3 install python-tsl2591
#needed for droneAir
pip3 install adafruit-blinka
sudo pip3 install adafruit-blinka
sudo pip3 install --force-reinstall adafruit-blinka

sudo pip3 install board
sudo pip3 install digitalio
#SSD1306 OLED Display Module
sudo pip3 install Adafruit-SSD1306
pip3 install adafruit-circuitpython-ssd1306
#Python Imaging Library
sudo apt-get install python3-pil
#BME sensors
sudo pip3 install adafruit-circuitpython-bme280
sudo pip3 install adafruit-circuitpython-bme680
#meteocalc used to do colour
sudo pip3 install meteocalc
#Triple-Axis Accelerometer I think unused
pip3 install adafruit-circuitpython-lis3dh
#analog to digital converters
pip3 install adafruit-circuitpython-ads1x15
#CO2 Sensor
sudo pip3 install mh-z19
#used colours
sudo pip3 install colour
sudo pip3 install configparser
# display used for crystal display
sudo pip3 install RPLCD
#used to access I2C for displays 
sudo pip3 install smbus2
#Display used for liquid crystal display - this is the one used by display class for droneFeedv2
pip3 install https://github.com/pl31/python-liquidcrystal_i2c/archive/master.zip
sudo pip3 install https://github.com/pl31/python-liquidcrystal_i2c/archive/master.zip

#green soil moisture
pip3 install adafruit-circuitpython-seesaw
#This script updates all submodules to the latest tag  https://github.com/adafruit/Adafruit_CircuitPython_Bundle/blob/master/update-submodules.sh
git submodule init
git submodule update
git submodule foreach git fetch --all
git submodule foreach "tag=\$(git rev-list --exclude='*-*' --tags --max-count=1); git checkout -q \$tag"
