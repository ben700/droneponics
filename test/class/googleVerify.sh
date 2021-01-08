#/home/pi/google-cloud-sdk/bin/gcloud beta pubsub subscriptions pull --auto-ack droneOxy
#!/bin/bash
for i in 1 2 3 4 5
do
   echo "Welcome $i times"
   /home/pi/google-cloud-sdk/bin/gcloud beta pubsub subscriptions pull --auto-ack dronePH
done
