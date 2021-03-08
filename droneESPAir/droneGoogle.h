#include <jwt.h>

#ifndef DroneGoogle_h
#define DroneGoogle_h

#include <CloudIoTCore.h>
#include "droneConfig.h"
#include <DroneSensor.h>
#include <ESP8266WiFi.h>
#include "FS.h"
#include <ArduinoJson.h>

// You need to set certificates to All SSL cyphers and you may need to
// increase memory settings in Arduino/cores/esp8266/StackThunk.cpp:
//   https://github.com/esp8266/Arduino/issues/6811
#include "WiFiClientSecureBearSSL.h"
#include <time.h>

#include <MQTT.h>

#include <CloudIoTCore.h>
#include <CloudIoTCoreMqtt.h>


#include <Base64.h>

#define TRACE true

// Initialize WiFi and MQTT for this board
static MQTTClient *mqttClient;
static BearSSL::WiFiClientSecure netClient;
static BearSSL::X509List certList;
static CloudIoTCoreDevice device(project_id, location, registry_id, device_id);
CloudIoTCoreMqtt *mqtt;

bool publishTelemetry(String data)
{
  return mqtt->publishTelemetry(data);
}

bool publishTelemetry(const char *data, int length)
{
  return mqtt->publishTelemetry(data, length);
}

bool publishTelemetry(String subfolder, String data)
{
  return mqtt->publishTelemetry(subfolder, data);
}

bool publishTelemetry(String subfolder, const char *data, int length)
{
  return mqtt->publishTelemetry(subfolder, data, length);
}

 
String getJwt()
{
  // Disable software watchdog as these operations can take a while.
  ESP.wdtDisable();
  time_t iat = time(nullptr);
  Serial.println("Refreshing JWT");
  String jwt = device.createJWT(iat, jwt_exp_secs);
  ESP.wdtEnable(0);
  return jwt;
}


void processState()
{
      String data = sensors->deviceStatePayload();
      Serial.print("Sending Droneponics state data to goolge ... ");
      Serial.println(mqtt->publishState(data.substring(0,482)) ? "Success!" : "Failed!");
}
void processBoot()
{

  while (!timeClient.update()) {
    timeClient.forceUpdate();
  }

  Serial.print("Sending Droneponics boot data to goolge ... ");
  Serial.println(publishTelemetry(String(deviceBootTopic), String(sensors->bootPayload(String(timeClient.getEpochTime())))) ? "Ready" : "Failed!");



}

void processSensor (){
  
   while (!timeClient.update()) {
      timeClient.forceUpdate();
   }
 
    String payload = sensors->sensorPayload(String(timeClient.getEpochTime()));
    bool returnCode = mqtt->publishTelemetry(sensorReadingTopic, payload);
    Serial.print("Sending telemetry sensor topic: ");
    Serial.println(returnCode ? "Success!" : "Failed!");
    if(!returnCode){
      Serial.print("Payload was : ");
      Serial.println(payload);
    }
 
}
/*
{"pump1":"On",
"pump2":"On",
"pump3":"On",
"pump4":"On",
"pump5":"On",
"pump6":"On"
}*/
void processDose (){
  
   if (_doserQ.isEmpty()){ 
    return;
   }
   int _relayPin;
   _doserQ.pop(&_relayPin);
     
   while (!timeClient.update()) {
      timeClient.forceUpdate();
   }
   StaticJsonDocument<1000> _doc;
   _doc["deviceTime"] =int(timeClient.getEpochTime());
   _doc["doser"] =deviceAction+String(_relayPin+1);
   _doc["name"] =relays->doser_list[_relayPin]._name;
   _doc["volume"] =relays->doser_list[_relayPin]._volume;
   
   if (DroneDevice_debug) {
    serializeJsonPretty(_doc,Serial); 
   }
    
   String payload;
   Serial.print("Recording details of dose to database : ");
   Serial.println(publishTelemetry(String(dosedTopic), String(payload)) ? "Success!" : "Failed!");

   relays->addDose(_relayPin+1, relays->doser_list[_relayPin]._volume);

}


void messageReceivedAdvanced(MQTTClient *client, char topic[], char bytes[], int length){
  if (length > 0){
    Serial.printf("incoming: %s - %s\n", topic, bytes);
  } else {
    Serial.printf("0\n"); // Success but no message
  }
  
  StaticJsonDocument<1000> doc;
  DeserializationError error = deserializeJson(doc, bytes);
  if (error)
     Serial.println(F("Failed to read file, using default configuration"));

  
}




static void readDerCert(const char *filename) {
  File ca = SPIFFS.open(filename, "r");
  if (ca)
  {
    size_t size = ca.size();
    uint8_t cert[size];
    ca.read(cert, size);
    certList.append(cert, size);
    ca.close();

    Serial.println("Success to open ca file ");
  }
  else
  {
    Serial.println("Failed to open ca file ");
  }
}

void setupCloudIoT()
{
  configTime(0, 0, ntp_primary, ntp_secondary);
  Serial.println("Waiting on time sync...");
  while (time(nullptr) < 1510644967)
  {
    delay(10);
  }

   if (!SPIFFS.begin())
  {
    Serial.println("Failed to mount file system");
    return;
  }

  readDerCert("/gtsltsr.crt"); // primary_ca.pem
  readDerCert("/GSR4.crt"); // backup_ca.pem
  netClient.setTrustAnchors(&certList);
  Serial.println("Success: Loaded primary_ca and backup_ca");


  File f = SPIFFS.open("/private-key.der", "r");
  Serial.println("Success: Opened private-key.der");

  if (f) {
    size_t size = f.size();
    uint8_t data[size];
    f.read(data, size);
    f.close();
    Serial.println("Success: Opened private-key.der");
    BearSSL::PrivateKey pk(data, size);
    device.setPrivateKey(pk.getEC()->x);

    Serial.println("Success to open private-key.der");
  } else {
    Serial.println("Failed to open private-key.der");
  }

  SPIFFS.end();



  mqttClient = new MQTTClient(512);
  mqttClient->setOptions(180, true, 1000); // keepAlive, cleanSession, timeout
  mqtt = new CloudIoTCoreMqtt(mqttClient, &netClient, &device);
  mqtt->setUseLts(true);
  mqtt->startMQTTAdvanced(); // Opens connection using advanced callback
}






#endif
