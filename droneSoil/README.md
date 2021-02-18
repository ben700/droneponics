
<h1>Install</h1>
cd to install before installing 

ch install
chmod +x install.sh
./install.sh


<h1>Tests</h1>
cd to test before running tests

cd test/
python3 readConfig.py
python3 soilSensor.py
python3 google.py

<h1>Deploy</h1>
cp desktop file from desktop/ to ~/.config/autostart

cp desktop/* ~/.config/autostart/
