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
./google-cloud-sdk/install.sh --disable-prompts 
./google-cloud-sdk/bin/gcloud init --no-launch-browser --account

#4/1AY0e-g67mG0kFmGRFUu0-dI3QHUg8HPawRIuMFGDCxpi_QenCIdCSRrUP9E


mkdir .ssh
cd .ssh
openssl req -x509 -newkey rsa:2048 -keyout droneponics_private.pem -nodes -out droneponics.pub -subj '/CN=unused'
wget https://pki.google.com/roots.pem


cd
./google-cloud-sdk/bin/gcloud iot devices create $HOSTNAME --region=europe-west1  --registry=droneAir --public-key path=/home/pi/.ssh/droneponics.pub,type=rsa-x509-pem

