
--------SDK
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-325.0.0-linux-x86_64.tar.gz
tar -xf google-cloud-sdk-325.0.0-linux-x86_64.tar.gz

./google-cloud-sdk/install.sh
./google-cloud-sdk/bin/gcloud init

gcloud config set project drone-302200
gcloud config set compute/zone europe-west2-a
gcloud config set compute/region europe-west2
gcloud components update


----CERTS
openssl req -x509 -newkey rsa:2048 -keyout d1mini_private.pem -nodes -out d1mini_public.pem -subj "/CN=droneponics"
openssl req -x509 -nodes -newkey rsa:2048 -keyout droneponics_rsa_private.pem -out droneponics_rsa_public.pem -subj "/CN=droneponics"
    
---Create a CA private key
openssl genpkey -algorithm RSA -out pixelbook_ca_private.pem -pkeyopt rsa_keygen_bits:2048
openssl req -x509 -new -nodes -key pixelbook_ca_private.pem -sha256 -out pixelbook_ca_cert.pem -subj "/CN=droneponics"
openssl genpkey -algorithm RSA -out pixelbook_rsa_private.pem -pkeyopt rsa_keygen_bits:2048
openssl req -new -sha256 -key pixelbook_rsa_private.pem -out pixelbook_rsa_cert.csr -subj "/CN=droneponics-device"
openssl x509 -req -in pixelbook_rsa_cert.csr -CA pixelbook_ca_cert.pem -CAkey pixelbook_ca_private.pem -CAcreateserial -sha256 -out pixelbook_rsa_cert.pem

--- the topic needs to exist
gcloud pubsub subscriptions create projects/drone-302200/subscriptions/deviceEventsSubscription --topic=projects/drone-302200/topics/deviceEventsTopic
    
--- these add few messages and then read them     
node cloudiot_mqtt_example_nodejs.js mqttDeviceDemo --projectId=drone-302200 --cloudRegion=europe-west1 --registryId=droneDevice --deviceId=pixelbook --privateKeyFile=pixelbook_private.pem --numMessages=25 --algorithm=RS256
gcloud pubsub subscriptions pull --auto-ack projects/drone-302200/subscriptions/deviceEventsSubscription

-----Need this with service_account.json
wget https://pki.goog/roots.pem

---start server
export GOOGLE_APPLICATION_CREDENTIALS="/home/benslittlebitsandbobs/.ssh/droneponicsserviceaccount_service_account.json"
python3 cloudiot_pubsub_example_server.py --project_id=drone-302200 --pubsub_subscription=deviceEventsSubscription --service_account_json=service_account.json

./google-cloud-sdk/bin/gcloud iot devices create "Pixelbook3" --region=europe-west1  --registry=droneDevice --public-key path=droneponics_public.pem,type=rsa-x509-pem



export GOOGLE_APPLICATION_CREDENTIALS="/home/benslittlebitsandbobs/python-docs-samples/iot/api-client/end_to_end_example/service_account.json"
python3 cloudiot_pubsub_example_mqtt_device.py --cloud_region=europe-west1 --project_id=drone-302200 --registry_id=droneDevice --device_id=Pixelbook3 --private_key_file=droneponics_private.pem --algorithm=RS256


python3 cloudiot_pubsub_example_server.py --project_id=drone-302200 --pubsub_subscription=deviceEventsSubscription --service_account_json=service_account.json
python3 cloudiot_pubsub_example_mqtt_device.py --cloud_region=europe-west1 --project_id=drone-302200 --registry_id=droneDevice --device_id=Pixelbook3 --private_key_file=droneponics_private.pem --algorithm=RS256











----------WEBSITE
git clone https://github.com/GoogleCloudPlatform/nodejs-docs-samples
cd nodejs-docs-samples/appengine/hello-world/standard
cat app.js
cat app.yaml
export PORT=8080 && npm install
npm start
gcloud app create
gcloud app deploy
