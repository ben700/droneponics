echo "Update PI"
sudo apt full-upgrade -y
sudo apt update
sudo apt full-upgrade -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo apt autoclean -y
/home/pi/updateDroneponics.sh
sudo reboot
