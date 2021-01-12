mkdir .ssh
cd .ssh
openssl req -x509 -newkey rsa:2048 -keyout droneponics_private.pem -nodes -out droneponics.pub -subj '/CN=unused'
wget https://pki.google.com/roots.pem



gcloud iot devices create droneMonitorPro --region=europe-west1  --registry=droneMonitorPro
--public-key \
    path=/home/pi/.ssh/droneponics_private.pem,type=rsa-x509-pem
cd
