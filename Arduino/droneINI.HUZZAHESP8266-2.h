#include <NTPClient.h>

#ifndef DEVICEID
#define DEVICEID "HUZZAHESP8266-2"
#endif

// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

const char* sssid = "HartleyAvenue";
const char* spassword = "33HartleyAvenue";

const long myChannelNumber = 1280631;                            //Your Thingspeak channel number
const char * myWriteAPIKey = "74NEO0MNO4J3OYNI";                 //Your ThingSpeak Write API Key


// Cloud iot details.
const char* project_id = "drone-302200";
const char* location = "europe-west1";
const char* registry_id = "droneDevice";
const char* device_id = DEVICEID;

const char* deviceBootTopic = "/deviceBoot";
const char* sensorReadingTopic = "";

bool polling = false;                     //we start off not polling, change this to true if you want polling on startup
bool send_to_thingspeak = false;


// To get the private key run (where private-key.pem is the ec private key
// used to create the certificate uploaded to google cloud iot):
// openssl ec -in <private-key.pem> -noout -text
// and copy priv: part.
// The key length should be exactly the same as the key length bellow (32 pairs
// of hex digits). If it's bigger and it starts with "00:" delete the "00:". If
// it's smaller add "00:" to the start. If it's too big or too small something
// is probably wrong with your key.
