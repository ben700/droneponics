gcloud init && git config --global credential.https://source.developers.google.com.helper gcloud.sh
git remote add google https://source.developers.google.com/p/drone-302200/r/droneDevice-esp8266
git push --all google
