#include <NTPClient.h>

#ifndef DEVICEID
#define DEVICEID "D1Mini-2"
#endif

#define NETWORK_LED 2      // led "NETWORK" on pcb
#define i2c_address 0x27   // i2c slave address for chip expander


// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

const char* sssid = "HartleyAvenue";
const char* spassword = "33HartleyAvenue";

// Cloud iot details.
const char* project_id = "drone-302200";
const char* location = "europe-west1";
const char* registry_id = "droneDevice";
const char* device_id = DEVICEID;

const char* deviceBootTopic = "/deviceBoot";
const char* sensorReadingTopic = "";
