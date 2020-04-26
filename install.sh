cp /home/pi/droneponics/updateDroneponics.sh /home/pi/updateDroneponics.sh

sudo apt full-upgrade -y
sudo apt update
sudo apt full-upgrade -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo apt autoclean -y

cd /tmp
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
cd
sudo apt-get install wiringpi
sudo apt-get install python-pip
sudo apt-get install xterm -y
sudo apt-get install lxde
sh /home/pi/droneponics/installUsr.sh
echo "Going to Reboot now"
sudo reboot
