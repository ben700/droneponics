cd /tmp
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
cd
sudo apt-get install wiringpi
sudo apt-get install python-pip
sudo apt-get install xterm -y
sudo apt-get install lxde


sudo apt full-upgrade -y
sudo apt update
sudo apt full-upgrade -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo apt autoclean -y


sh /home/pi/droneponics/installUsr.sh
