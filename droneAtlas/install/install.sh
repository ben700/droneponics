sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
pip3 install -r requirements.txt --user
sudo apt-get --purge -y autoremove
sudo apt-get clean
