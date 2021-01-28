#include "droneInclude.h"

// !!REPLACEME!!
// The MQTT callback function for commands and configuration updates
// Place your message handler code here.
void messageReceived(String &topic, String &payload){
  Serial.println("incoming: " + topic + " - " + payload);
}
///////////////////////////////

// Initialize WiFi and MQTT for this board
Client *netClient;
CloudIoTCoreDevice *device;
CloudIoTCoreMqtt *mqtt;
MQTTClient *mqttClient;
unsigned long iat = 0;
String jwt;

///////////////////////////////
// Helpers specific to this board
///////////////////////////////
String getDefaultSensor(){
  return "Wifi: " + String(WiFi.RSSI()) + "db";
}

String getJwt(){
  iat = time(nullptr);
  Serial.println("Refreshing JWT");
  jwt = device->createJWT(iat, jwt_exp_secs);
  return jwt;
}

///////////////////////////////
// Orchestrates various methods from preceeding code.
///////////////////////////////
bool publishTelemetry(String data){
  return mqtt->publishTelemetry(data);
}

bool publishTelemetry(const char *data, int length){
  return mqtt->publishTelemetry(data, length);
}

bool publishTelemetry(String subfolder, String data){
  return mqtt->publishTelemetry(subfolder, data);
}

bool publishTelemetry(String subfolder, const char *data, int length){
  return mqtt->publishTelemetry(subfolder, data, length);
}

String payloadError(String sError){
     return " Error:" + sError + ",  \n";
       
}


void publishState (String sError){
  Serial.print("Sending Droneponics data to goolge ... ");
  Serial.println(mqtt->publishState(sError + relayBoard.getPayload()) ? "Ready" : "Failed!");
}


void logDroneponicsCommandCallback(String data){
  String sError;
  Serial.print("logDroneponicsCommandCallback data = " + data +"\n");  
  
  
  if(relayBoardSize<10){
    commandlength = 2 * relayBoardSize;
  }
  else{
    commandlength = 2 * 10;
    commandlength += 3 * (relayBoardSize-10);
  }

 if(data.length() == commandlength)
 {
  int x=0;
  int y=1;
  
   while(data.length() >= y+2){
    int boardChannel = data.substring(x,y);
    int command = data.substring(y+1,y+2);   
    if(command){
      relayBoard[boardChannel].turnOn();
    }else{
      relayBoard[boardChannel].turnOff();
    }      
   }
 }
 else
 {
  sError = "Command String Not Found";
 }

     publishState(payloadError(sError ));
}

void connect(){
  if(WiFi.status() == WL_CONNECTED){
    mqtt->mqttConnect();
  }else{
      setupWifi();
  }
  
}

void setupCloudIoT(){
  device = new CloudIoTCoreDevice(
      project_id, location, registry_id, device_id,
      private_key_str);

  setupWifi();
  
  if(WiFi.status() == WL_CONNECTED){
    netClient = new WiFiClientSecure();
    mqttClient = new MQTTClient(512);
    mqttClient->setOptions(180, true, 1000); // keepAlive, cleanSession, timeout
    mqtt = new CloudIoTCoreMqtt(mqttClient, netClient, device);
    mqtt->setUseLts(true);
    mqtt->startMQTT();
  }
}
