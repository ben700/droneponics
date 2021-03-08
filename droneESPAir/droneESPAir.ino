#include <DroneWiFiConnect.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <Ticker.h>
#include <WiFiUdp.h>
#include <NTPClient.h>


#include "droneConfig.h"
#include "droneGoogle.h"


#include <WiFiClient.h>
#ifdef ARDUINO_ARCH_ESP8266
#include <ESP8266HTTPClient.h>
#else
#include <HTTPClient.h>
#endif




WiFiConnect wc;

// For internet connection
WiFiClient client;
HTTPClient http;

void configModeCallback(WiFiConnect *mWiFiConnect) {
  Serial.println("Entering Access Point");
}


void startWiFi(boolean showParams = false) {

  wc.setDebug(true);

  /* Set our callbacks */
  wc.setAPCallback(configModeCallback);

  //wc.resetSettings(); //helper to remove the stored wifi connection, comment out after first upload and re upload

  /*
     AP_NONE = Continue executing code
     AP_LOOP = Trap in a continuous loop - Device is useless
     AP_RESET = Restart the chip
     AP_WAIT  = Trap in a continuous loop with captive portal until we have a working WiFi connection
  */
  if (!wc.autoConnect()) { // try to connect to wifi
    /* We could also use button etc. to trigger the portal on demand within main loop */
    wc.startConfigurationPortal(AP_WAIT);//if not connected show the configuration portal
  }
}



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  delay (5000);
  if(!SPIFFS.begin()){
        Serial.println("An Error has occurred while mounting SPIFFS");
        return;
  }
  
  wc.setDeviceId(device_id);
  startWiFi();
 
  flasher = new DroneFlasher(DroneState::SETUP);
  pinMode(LED_BUILTIN, OUTPUT);
  if (WiFi.status() == WL_CONNECTED) {
    timeClient.begin();
    setupCloudIoT();
  }
  
  relays = new DroneSwitch(i2c_address, StartRelay);
  sensors = new DroneSensor(WiFi.macAddress(), WiFi.localIP().toString(), device_id, false);
  flasher->update(DroneState::OPS);

}

void loop() {


  // Wifi Dies? Start Portal Again
  if (WiFi.status() != WL_CONNECTED) {
    if (!wc.autoConnect()) wc.startConfigurationPortal(AP_WAIT);
  }
  else
  {
    if (!mqtt->loop())
    {
       mqtt->mqttConnect();
    }

    if (justBoot) {
      DroneDevice_debug ? Serial.println("Debuggind On") : Serial.println("Debuggind Off");
      processBoot();
      processState();
      justBoot = false;
      next_step_time = millis();
    }

    if (millis() >= next_step_time) {
      processSensor();
      next_step_time = millis() + 60000;
      }
  }
}
