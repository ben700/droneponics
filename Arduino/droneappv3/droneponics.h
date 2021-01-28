#include "droneInclude.h"

bool returnCode = false;

bool justBoot = true;
String readNetworkFromEEPROMResult; 


// Initialize WiFi and MQTT for this board
static MQTTClient *mqttClient;
static BearSSL::WiFiClientSecure netClient;
static BearSSL::X509List certList;
static CloudIoTCoreDevice device(project_id, location, registry_id, device_id);
CloudIoTCoreMqtt *mqtt;

///////////////////////////////
// Helpers specific to this board
///////////////////////////////
String getDefaultSensor()
{
  return "Wifi: " + String(WiFi.RSSI()) + "db";
}

String getJwt()
{
  // Disable software watchdog as these operations can take a while.
  ESP.wdtDisable();
  time_t iat = time(nullptr);
  Serial.println("Refreshing JWT");
  Serial.println(device_id);
  
  String jwt = device.createJWT(iat, jwt_exp_secs);
  ESP.wdtEnable(0);
  return jwt;
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

    Serial.print("Success to open ca file ");
  }
  else
  {
    Serial.print("Failed to open ca file ");
  }
  Serial.println(filename);
}

static void setupCertAndPrivateKey()
{
  // Set CA cert on wifi client
  // If using a static (pem) cert, uncomment in ciotc_config.h:f
  certList.append(primary_ca);
  certList.append(backup_ca);
  netClient.setTrustAnchors(&certList);

  device.setPrivateKey(HUZZAHESP82662_private_key);

  return;

  // If using the (preferred) method with the cert and private key in /data (SPIFFS)
  // To get the private key run
  // openssl ec -in <private-key.pem> -outform DER -out private-key.der

  if (!SPIFFS.begin())
  {
    Serial.println("Failed to mount file system");
    return;
  }

  readDerCert("/gtsltsr.crt"); // primary_ca.pem
  readDerCert("/GSR4.crt"); // backup_ca.pem
  netClient.setTrustAnchors(&certList);


  File f = SPIFFS.open("/private-key.der", "r");
  if (f) {
    size_t size = f.size();
    uint8_t data[size];
    f.read(data, size);
    f.close();

    BearSSL::PrivateKey pk(data, size);
    device.setPrivateKey(pk.getEC()->x);

    Serial.println("Success to open private-key.der");
  } else {
    Serial.println("Failed to open private-key.der");
  }

  SPIFFS.end();
}

///////////////////////////////
// Orchestrates various methods from preceeding code.
///////////////////////////////


bool publishBootDataTelemetry(String data)
{
  Serial.print("Sending to Google boot topic: ");

  returnCode = mqtt->publishTelemetry(deviceBootTopic, data);
  
  if (returnCode) {                                                             //check thingspeak return code if it is 200 then the upload was a success
    Serial.println("success");                                                          //print "success"
  }else {
    Serial.println("publishBootDataTelemetry =" + data);
    Serial.print("publishBootDataTopic =" + String(deviceBootTopic));
    Serial.println("upload error, code: " + String(returnCode));                       //print "upload error, code:" and whatever number is in the return_code var
  }
  return false;
}

bool publishSensorDataTelemetry(String data)
{
  Serial.print("Sending to Google sensor topic: ");

  returnCode = mqtt->publishTelemetry(sensorReadingTopic, data);
  
  if (returnCode) {                                                             //check thingspeak return code if it is 200 then the upload was a success
    Serial.println("success");                                                          //print "success"
  }else {
    Serial.println("publishSensorDataTelemetry =" + data);
    Serial.print("sensorReadingTopic =" + String(sensorReadingTopic));
    Serial.println("upload error, code: " + String(returnCode));                       //print "upload error, code:" and whatever number is in the return_code var
  }
  return false;
}
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

// TODO: fix globals
void setupCloudIoT()
{
  Serial.println("Waiting on setupCloudIoT...");

  // ESP8266 WiFi setup
  setupWifi();
  if(WiFi.status() == WL_CONNECTED){
        
    // ESP8266 WiFi secure initialization and device private key
    Serial.println("Waiting on setupCertAndPrivateKey...");
    setupCertAndPrivateKey();
    
    mqttClient = new MQTTClient(512);
    mqttClient->setOptions(180, true, 1000); // keepAlive, cleanSession, timeout
    mqtt = new CloudIoTCoreMqtt(mqttClient, &netClient, &device);
    mqtt->setUseLts(true);
    mqtt->startMQTTAdvanced(); // Opens connection using advanced callback
    Serial.println("Waiting on mqttClient...");
  }
}

String calError(String sError){
     return "{\"Error\":\"" + sError + "\", \"Calibration Commands\":{  \"Temperature\": { \
          \"deviceID\": \"102\", \
          \"Clear\": \"Cal,clear\",\
          \"Set to t\": \"Cal,t\" \
       }, \
       \"Dissolved Oxygen\": { \
          \"deviceID\": \"97\", \
          \"Clear\": \"Cal,clear\", \
          \"Atmospheric\": \"Cal\", \
          \"Solution\": \"Cal,0\" \
       }, \
       \"Oxidation Reduction Potential\": { \
          \"deviceID\": \"98\", \
          \"Clear\": \"Cal,clear\", \
          \"Set to n\" : \"Cal,n\" \
       }, \
       \"Conductivity\": { \
          \"deviceID\": \"100\", \
          \"Clear\": \"Cal,clear\", \
          \"Atmospheric\": \"Cal,dry\", \
          \"Single Point\": \"Cal,n\", \
          \"Low\": \"Cal,low,n\", \
          \"High\": \"Cal,high,n\", \
          \"probe Type\": \"K,n\"    \
       }, \
       \"pH\": { \
          \"deviceID\": \"99\", \
          \"Clear\": \"Cal,clear\", \
          \"Mid\": \"Cal,mid,7\", \
          \"Low\": \"Cal,low,4\", \
          \"High\": \"Cal,high,10\" \
       }";
       
}

String singleDeviceStatePayload (Ezo_board &Device){

  String command = "I";
  String cmdReply;
  String payload;
  payload = "";

  char receive_buffer[32];
  Device.send_cmd(command.c_str());
  select_delay(command);
  if(Device.receive_cmd(receive_buffer, 32) == Ezo_board::SUCCESS){   //if the reading is successful
    cmdReply = String(receive_buffer);        //parse the reading into a float
  }
  else{
    Serial.print(String(Device.get_name()) + " is not connected }"+ ",\n");    
    return "Not Connected";
  }

  String type = cmdReply.substring(cmdReply.indexOf(",")+1, cmdReply.indexOf(",",4));
  String firm = cmdReply.substring(cmdReply.indexOf(",",4)+1);
  payload = payload + String(Device.get_name()) + " " + type + "{" + "\t";
  payload = payload + "\tFirmware:" + firm + ", \n\t\t";
  
  
  command = "CAL,?";
  Device.send_cmd(command.c_str());
  select_delay(command);
  if(Device.receive_cmd(receive_buffer, 32) == Ezo_board::SUCCESS){   //if the reading is successful
    cmdReply = String(receive_buffer);        //parse the reading into a float
  }
  
  String calibrationPoints = cmdReply.substring(cmdReply.indexOf("CAL,")+4);
  payload = payload + "Calibration Points:" + calibrationPoints + ", \n\t\t";
 
    
  command = "Status";
  Device.send_cmd(command.c_str());
  select_delay(command);
  if(Device.receive_cmd(receive_buffer, 32) == Ezo_board::SUCCESS){   //if the reading is successful
    cmdReply = String(receive_buffer);        //parse the reading into a float
  }

  String reasonForRestart = cmdReply.substring(cmdReply.indexOf(",")+1,cmdReply.indexOf(",", cmdReply.indexOf(",")+1) );
  String VoltageatVcc = cmdReply.substring(cmdReply.indexOf(",", cmdReply.indexOf(",")+1)+1);
  payload = payload + "Reason for restart:" + restartCodes.getValueOf("P") + ", \n\t\t";
  payload = payload + "VoltageatVcc:" + VoltageatVcc + ", \n\t\t";
    
  command = "L,?";
  Device.send_cmd(command.c_str());
  select_delay(command);
  if(Device.receive_cmd(receive_buffer, 32) == Ezo_board::SUCCESS){   //if the reading is successful
    cmdReply = String(receive_buffer);        //parse the reading into a float
  }

  String LED = cmdReply.substring(cmdReply.indexOf("L,")+2);
  payload = payload + "LED:" + ledStatus.getValueOf("1") + ", \n\t\t";

  command = "R";
  Device.send_cmd(command.c_str());
  select_delay(command);
  if(Device.receive_cmd(receive_buffer, 32) == Ezo_board::SUCCESS){   //if the reading is successful
    cmdReply = String(receive_buffer);        //parse the reading into a float
  }

  float reading = cmdReply.toInt(); 
  payload = payload + "Reading: "+String(reading,2) +", \n\t\t";

  payload = payload + "},\n";
  return payload;
}


bool publishState (){
  String payload = payload + singleDeviceStatePayload(RTD);
  payload = payload + singleDeviceStatePayload(PH);
  payload = payload + singleDeviceStatePayload(EC);
  payload = payload + singleDeviceStatePayload(DO);

  
  int lengthSize =455;
  bool returnCode = false;
  while(lengthSize < payload.length())
  {
       String _payload = String(payload.length())  + ":" + payload.substring(0, lengthSize-4);

       int lengthData = _payload.length();
       char decodedString[lengthSize];     
       payload.toCharArray( decodedString, lengthSize);
       int decodedLength = Base64.decodedLength(decodedString, lengthSize);
       char outputString[decodedLength];
       Base64.decode(outputString, decodedString, lengthSize);
 

       Serial.print("Sending " + String(lengthSize)+ " char from total of [" + String(payload.length()) +"]\n");
     
       Serial.print("payload [" + String(payload) +"]\n");
       
       
       Serial.print("Sending Droneponics data to goolge ... ");
       Serial.println(mqtt->publishState(_payload) ? "Ready" : "Failed!");
       

       lengthSize += 1;     
       
       delay(10000);
  }

    return returnCode;
}


void logDroneponicsCommandCallback(String data){
  String sError;

  
     Serial.print("logDroneponicsCommandCallback data = " + data +"\n");
     if(data.substring(0,3) == "cal"){
       String calDevice = data.substring(4,data.indexOf("#",4));
       String calCommand = data.substring(calDevice.length()+5,data.indexOf("#",data.indexOf("#",4)+1));
         
       if(strcmp(calDevice.c_str(), (const char*) RTD.get_address())==0){
          Serial.print("RTD Device =" + calDevice + "\n");
           RTD.send_cmd(calDevice.c_str());
           if (RTD.get_error() != Ezo_board::SUCCESS) {
            sError = "Calibration Command "+ calCommand +" Not Found"; 
           }
       }
       
       else if(strcmp(calDevice.c_str(),(const char*) EC.get_address())==0){
          Serial.print("EC Device =" + calDevice + "\n");
           PH.send_cmd(calDevice.c_str());
           if (PH.get_error() != Ezo_board::SUCCESS) {
            sError = "Calibration Command "+ calCommand +" Not Found"; 
           }
      }
       else if(strcmp(calDevice.c_str(),(const char*) PH.get_address())==0){
          Serial.print("PH Device =" + calDevice + "\n");
           PH.send_cmd(calDevice.c_str());
           if (PH.get_error() != Ezo_board::SUCCESS) {
            sError = "Calibration Command "+ calCommand +" Not Found"; 
           }
       }
       else if(strcmp(calDevice.c_str(),(const char*) DO.get_address())==0){
          Serial.print("DO Device =" + calDevice + "\n");
          DO.send_cmd(calDevice.c_str());
          if (DO.get_error() != Ezo_board::SUCCESS) {
            sError = "Calibration Command "+ calCommand +" Not Found"; 
          }
       }
       else
       {
         sError = "Calibration Device "+ calDevice +" Not Found";
         Serial.print(sError);
       }
       
       
       
       String sError = "";
       sError = "Calibration Device "+ calDevice +" Not Found";
      if (sError.length() > 0){
        String payload = calError(sError );
        Serial.print(payload);
        //publishState(payload);
       }
     }
     publishState();
}

void logDroneponicsConfigCallback(String data){
     Serial.print("logDroneponicsCommandCallback data = " + data +"\n");
     publishState();

}
// !!REPLACEME!!
// The MQTT callback function for commands and configuration updates
// Place your message handler code here.
void messageReceived(String &topic, String &payload){
  Serial.println("###########################################messageReceived");
  Serial.println("incoming: " + topic + " - " + payload);
   
   
   if(String(topic).indexOf("command") > 0){
    logDroneponicsCommandCallback(payload);
   }
   else if(String(topic).indexOf("config") > 0){
    logDroneponicsConfigCallback(payload);
   }
  
}

void messageReceivedAdvanced(MQTTClient *client, char topic[], char bytes[], int length)
{
  Serial.println("###########################################messageReceivedAdvanced");
   Serial.printf("incoming: Topic %s - \n", topic);
   Serial.printf("incoming: Data %s - \n" , bytes);

   if(String(topic).indexOf("command") > 0){
    logDroneponicsCommandCallback(bytes);
   }
   else if(String(topic).indexOf("config") > 0){
    logDroneponicsConfigCallback(bytes);
   }

   
}
///////////////////////////////
