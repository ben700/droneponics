echo "--------update pip3---------------------------------------------"
apt-get install libcairo2-dev -y
sudo pip3 freeze > /home/pi/droneponics/requirements.txt
sudo python3 /home/pi/droneponics/replace.py /home/pi/droneponics/requirements.txt
sudo pip3 install -r /home/pi/droneponics/requirements.txt --upgrade

echo "--------installUsr---------------------------------------------"
/home/pi/droneponics.installUsr.sh

echo "---------------------------------------------"Update PI---------------------------------------------""
sudo apt full-upgrade -y
sudo apt update
sudo apt full-upgrade -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo apt autoclean -y
echo "---------------------------------------------"Update droneponics---------------------------------------------""
/home/pi/updateDroneponics.sh
echo "---------------------------------------------"reboot---------------------------------------------""
sudo reboot
