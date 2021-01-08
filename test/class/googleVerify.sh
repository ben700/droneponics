#/home/pi/google-cloud-sdk/bin/gcloud beta pubsub subscriptions pull --auto-ack droneOxy
#!/bin/bash
for i in 1 2 3 4 5 6 7
do
   echo "Message $i from dronePH"
   /home/pi/google-cloud-sdk/bin/gcloud beta pubsub subscriptions pull --auto-ack dronePH
   echo "Message $i  from doser"
   /home/pi/google-cloud-sdk/bin/gcloud beta pubsub subscriptions pull --auto-ack doser
done
