
#include "droneInclude.h"

void setup() {
  Serial.begin(9600);
  EEPROM.begin(512);
  Wire.begin(); 
  setupDroneStatic();   

  //int writeNetworkToEEPROMResult = writeNetworkToEEPROM(sssid, spassword);
 // int writeNetworkToEEPROMResult = writeNetworkToEEPROM("HA", "HA");
  // Reading
  pinMode(LED_BUILTIN, OUTPUT);
  setupCloudIoT(); // Creates globals for MQTT

  pinMode(EN_PH, OUTPUT);                                                         //set enable pins as outputs
  pinMode(EN_EC, OUTPUT);
  pinMode(EN_RTD, OUTPUT);
  pinMode(EN_AUX, OUTPUT);
  digitalWrite(EN_PH, LOW);                                                       //set enable pins to enable the circuits
  digitalWrite(EN_EC, LOW);
  digitalWrite(EN_RTD, HIGH);
  digitalWrite(EN_AUX, LOW);
  
    ThingSpeak.begin(client);               //enable ThingSpeak connection
   if(WiFi.status() == WL_CONNECTED){
    print_help();                           //print our options on startup

    Serial.println("Starting automatic datalogging to thinkspeak.");
    start_datalogging();
   }  

}


//static unsigned long lastMillis = 0;

void loop() {
  server.handleClient();

       
 if(WiFi.status() == WL_CONNECTED){
  if (!mqtt->loop())
  {
    mqtt->mqttConnect();
    publishState();
  }
 
  if (send_to_thingspeak == true) {
    if (justBoot) {
 
        while(!timeClient.update()) {
          timeClient.forceUpdate();
        }
        Serial.println("---------------------------------------------");
        Serial.print("String(timeClient.getEpochTime()) = " + String(timeClient.getEpochTime()) + "\n");
     
        String outputStr = "{ \"bootTime\": \"" + String(timeClient.getEpochTime())+ "\", \"deviceMAC\": \"" +  WiFi.macAddress(); 
        outputStr =outputStr + "\",\"deviceName\": \""+device_id+ "\", \"deviceIP\": \"" +  WiFi.localIP().toString() + "\"}";
        publishBootDataTelemetry(outputStr);
        justBoot=false;



      } 
  }
  user_commands();                        //function which handles all the user commands

  if (polling == true) {                                                            //if we enabled polling
    switch (current_step) {                                                         //selects what to do based on what reading_step we are in
      //------------------------------------------------------------------

      case REQUEST_TEMP:                                                            //when we are in the first step
        if (millis() >= next_step_time) {                                           //check to see if enough time has past, if it has
          RTD.send_read_cmd();
          next_step_time = millis() + reading_delay; //set when the response will arrive
          current_step = READ_TEMP_AND_COMPENSATE;       //switch to the receiving phase
        }
        break;

      //------------------------------------------------------------------
      case READ_TEMP_AND_COMPENSATE:
        if (millis() >= next_step_time) {

          receive_reading(RTD);             //get the reading from the RTD circuit

          if ((RTD.get_error() == Ezo_board::SUCCESS) && (RTD.get_last_received_reading() > -1000.0)) { //if the temperature reading has been received and it is valid
            PH.send_cmd_with_num("T,", RTD.get_last_received_reading());
            EC.send_cmd_with_num("T,", RTD.get_last_received_reading());
            DO.send_cmd_with_num("T,", RTD.get_last_received_reading());
            ThingSpeak.setField(3, String(RTD.get_last_received_reading(), 2));                 //assign temperature readings to the third column of thingspeak channel
          } else {                                                                                      //if the temperature reading is invalid
            PH.send_cmd_with_num("T,", 20.0);
            EC.send_cmd_with_num("T,", 20.0);                                                          //send default temp = 25 deg C to EC sensor
            DO.send_cmd_with_num("T,", 20.0);
            ThingSpeak.setField(3, String(20.0, 2));                 //assign temperature readings to the third column of thingspeak channel
          }

          Serial.print(" ");
          next_step_time = millis() + short_delay; //set when the response will arrive
          current_step = REQUEST_DEVICES;        //switch to the receiving phase
        }
        break;

      //------------------------------------------------------------------
      case REQUEST_DEVICES:                      //if were in the phase where we ask for a reading
        if (millis() >= next_step_time) {
          //send a read command. we use this command instead of PH.send_cmd("R");
          //to let the library know to parse the reading
          PH.send_read_cmd();
          EC.send_read_cmd();
          DO.send_read_cmd();

          next_step_time = millis() + reading_delay; //set when the response will arrive
          current_step = READ_RESPONSE;              //switch to the next step
        }
        break;

      //------------------------------------------------------------------
      case READ_RESPONSE:                             //if were in the receiving phase
        if (millis() >= next_step_time) {  //and its time to get the response

          receive_reading(PH);             //get the reading from the PH circuit
          if (PH.get_error() == Ezo_board::SUCCESS) {                                          //if the PH reading was successful (back in step 1)
            ThingSpeak.setField(1, String(PH.get_last_received_reading(), 2));                 //assign PH readings to the first column of thingspeak channel
          }
          Serial.print("  ");
          receive_reading(EC);             //get the reading from the EC circuit
          if (EC.get_error() == Ezo_board::SUCCESS) {                                          //if the EC reading was successful (back in step 1)
            ThingSpeak.setField(2, String(EC.get_last_received_reading(), 0));                 //assign EC readings to the second column of thingspeak channel
          }
          Serial.print("  ");
          receive_reading(DO);             //get the reading from the DO circuit
          if (DO.get_error() == Ezo_board::SUCCESS) {                                          //if the DO reading was successful (back in step 1)
            ThingSpeak.setField(4, String(DO.get_last_received_reading(), 2));                 //assign DO readings to the fourth column of thingspeak channel
          }

          Serial.println();

          if (send_to_thingspeak == true) {                                                    //if we're datalogging

            if (WiFi.status() == WL_CONNECTED) {                                               //and we're connected to the wifi
              Serial.print("Sending to Thinkspeak: ");

              return_code = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);                 //upload the data to thingspeak, read the return code

              if (return_code == 200) {                                                             //check thingspeak return code if it is 200 then the upload was a success
                Serial.println("success");                                                          //print "success"
              }
              else {                                                                                //if the thingspeak return code was not 200
                Serial.println("upload error, code: " + String(return_code));                       //print "upload error, code:" and whatever number is in the return_code var
              }

 if (RTD.get_error() == Ezo_board::SUCCESS and \
     PH.get_error() == Ezo_board::SUCCESS and \
     EC.get_error() == Ezo_board::SUCCESS and \
     DO.get_error() == Ezo_board::SUCCESS
     ) {
           
             while(!timeClient.update()) {
               timeClient.forceUpdate();
             }
            
              String outputStr = "{ \"deviceTime\": \"" + String(timeClient.getEpochTime()) +"\", ";
              outputStr = outputStr + "\"deviceMAC\": \"" +  WiFi.macAddress() +"\", ";
              outputStr = outputStr + "\"temperature\": \"" +String(RTD.get_last_received_reading(), 1) +"\", ";
              outputStr = outputStr + "\"pH\": \"" +String(PH.get_last_received_reading(), 2) +"\", ";
              outputStr = outputStr + "\"conductivity\": \"" + String(EC.get_last_received_reading(), 0) +"\", ";
              outputStr = outputStr + "\"dissolvedOxygen\": \"" +String(DO.get_last_received_reading(), 0) + "\"}";

              publishSensorDataTelemetry(outputStr);
     }
     else
     {

         Serial.println("No Sensors connected, cannot send to Google");
      
     }

              Serial.println();                                                                     //print a new line so the output string on the serial monitor is easy to read
            } else {
              Serial.println("No Wifi connection, cannot send to Thingspeak");
            }
          }

          next_step_time =  millis() + poll_delay;
          current_step = REQUEST_TEMP;                                                          //switch back to asking for readings
        }
        break;
        }
    }
  }
}
