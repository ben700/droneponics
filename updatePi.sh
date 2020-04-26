pip3 freeze > /home/pi/droneponics/requirements.txt
python3 /home/pi/droneponics/replace.py /home/pi/droneponics/requirements.txt
pip3 install -r /home/pi/droneponics/requirements.txt --upgrade
rm /home/pi/droneponics/requirements.txt


echo "Update PI"
sudo apt full-upgrade -y
sudo apt update
sudo apt full-upgrade -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo apt autoclean -y
/home/pi/updateDroneponics.sh

