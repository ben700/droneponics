#ifndef DroneConfig_h
#define DroneConfig_h

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif
#include <DroneSensor.h>
#include <DroneFlasher.h>
#include <DroneSwitch.h>

#define StartRelay 10
#define i2c_address 0x27

#define DroneDevice_debug false
#define deviceAction "pump"

// Configuration for NTP
// Define NTP Client to get time
const char* ntp_primary = "time.google.com";
const char* ntp_secondary = "time1.google.com";
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

const char* project_id = "drone-302200";
const char* location = "europe-west1";
const char* registry_id = "droneDevice";
const char* device_id = "droneESPDoser";

// Time (seconds) to expire token += 20 minutes for drift
const int jwt_exp_secs = 3600; // Maximum 24H (3600*24)


const char* deviceBootTopic = "/deviceBoot";
const char* sensorReadingTopic = "/sensorReading";
const char* dosedTopic = "/dosed";

DroneSensor *sensors;
DroneFlasher *flasher;
DroneSwitch *relays;
bool justBoot = true;
uint32_t next_step_time = 0;

Ticker doserMQTTTicker;
cppQueue  _doserQ = cppQueue(sizeof(int), 16, FIFO);

    

#endif
