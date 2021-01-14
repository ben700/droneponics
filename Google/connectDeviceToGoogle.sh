sudo apt-get install build-essential
sudo apt-get install libssl-dev
sudo apt-get install python-dev
sudo apt-get install libffi-dev
sudo pip3 install paho-mqtt
sudo pip3 install pyjwt
sudo pip3 install cryptography

curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-321.0.0-linux-x86.tar.gz
tar -xf google-cloud-sdk-321.0.0-linux-x86.tar.gz
rm -f google-cloud-sdk-321.0.0-linux-x86.tar.gz
./google-cloud-sdk/install.sh --quiet 

#./google-cloud-sdk/bin/gcloud config set account ben@droneponics.com
#./google-cloud-sdk/bin/gcloud config set project droneponics-301222

./google-cloud-sdk/bin/gcloud init --no-launch-browser --account ben@droneponics.com


mkdir .ssh
cd .ssh
openssl req -x509 -newkey rsa:2048 -keyout droneponics_private.pem -nodes -out droneponics.pub -subj '/CN=unused'
wget https://pki.google.com/roots.pem


cd
./google-cloud-sdk/bin/gcloud iot devices create $HOSTNAME --region=europe-west1  --registry=droneOxy --public-key path=/home/pi/.ssh/droneponics.pub,type=rsa-x509-pem

