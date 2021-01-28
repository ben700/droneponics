#include "droneInclude.h"

void handleDroneponics()
{
  int scanResult;
  String ssid;
  int32_t rssi;
  uint8_t encryptionType;
  uint8_t* bssid;
  int32_t channel;
  bool hidden;
  bool foundSSID = false;

  scanResult = WiFi.scanNetworks(/*async=*/false, /*hidden=*/true);
 // Print unsorted scan results
  
  String web =""; 
  web += "<!DOCTYPE html><html>";
  web += "<head>";
  web += "<title>Droneponics WiFi Configuration Page</title>";  
  web += "</head>";

  web += "<body>";
//  web += "<img src="+logo+" >";

  web += "<script>";
  //web += "document.getElementById(\"ssidList\").onselect = function() {myFunction()};";

  web += "function myFunction() {";
  web += "  var x = document.getElementById(\"ssidList\").selectedIndex";
  web += "  alert(document.getElementsByTagName(\"option\")[x].value)";

  web += "  document.getElementById(\"ssid\").value = document.getElementsByTagName(\"option\")[document.getElementById(\"ssidList\").selectedIndex].value";
  web += "}";
  web += "</script>";

  int readNetworkFromEEPROMResult = readNetworkFromEEPROM(&eSsid, &ePassword);
  Network mySSIDList(scanResult);
  for (int8_t i = 0; i < scanResult; i++) 
  {
      WiFi.getNetworkInfo(i, ssid, encryptionType, rssi, bssid, channel, hidden);
      mySSIDList.addElement(&ssid); 
  }
  
  web += "<H1>WIFI Configuration<\H1><br>";
  web += "<style>select:invalid { color: gray; }</style>";

  web += "<form action=\"/droneponics\" method=\"post\">";
  web += "<label for=\"ssid\">ssid:</label><br>";
  web += "<select id=\"ssidList\" name=\"ssidList\" onselect=\"JavaScript:myFunction()\" required>";
  
  for (int8_t i = 0; i < mySSIDList.getCurrentSize(); i++) {
      web += "<option value=\"" + mySSIDList.getElement(i) + "\""; 
      if(mySSIDList.getElement(i) == sssid){
         web +=  " selected";
         foundSSID = true;
      }
      web +=  ">"+ String(mySSIDList.getElement(i)) + "</option>";                    
  }
  
  if(!foundSSID){
      web += "<option value=\"\" disabled selected hidden>Please Choose...</option>";
  }
    
  web += "</select><br>";
  web += "<label for=\"ssid\">ssid:</label><br>";
  web += "<input type=\"text\" id=\"ssid\" name=\"ssid\" value=\""+String(sssid)+"\"><br>";
  web += "<label for=\"password\">Password:</label><br>";
  web += "<input type=\"text\" id=\"password\" name=\"password\" value=\""+String(spassword)+"\">";
  
  web += "<button type=\"submit\" value=\"Submit\">Submit</button>";  
  web += "<button type=\"reset\" value=\"Reset\">Reset</button>";
  
  web += "</form>";
  
 
  web += "</body></html>";
  server.send(200, "text/html", web);

}

void handleDroneponicsUpdate() { 

String message = "";


if (server.arg("ssid")== ""){     //Parameter not found

message += "SSID Argument not found";

}else{     //Parameter found

message += "ssid Argument = ";
message += server.arg("ssid");     //Gets the value of the query parameter
message += "\n";
}


if (server.arg("password")== ""){     //Parameter not found

message += "Password Argument not found";

}else{     //Parameter found

message += "Password Argument = ";
message += server.arg("password");     //Gets the value of the query parameter

}

message += "<form action=\"/confirmDroneponics\" id=\"confirm\"  method=\"post\">";
message += "<input type=\"submit\" value=\"Submit\">";

message += "<input type=\"hidden\" id=\"ssid\" name=\"ssid\" value=\""+server.arg("ssid")+"\">";
message += "<input type=\"hidden\" id=\"password\" name=\"password\" value=\""+server.arg("password")+"\">";


message += "</form>";


message += "<form action=\"/\" id=\"cancel\"  method=\"post\">";
message += "<button type=\"cancel\" form=\"cancel\">Cancel</button>"; 
message += "</form>";
  
server.send(200, "text/html", message);          //Returns the HTTP response
}

void handleConfirmDroneponics()
{
  int writeNetworkToEEPROMResult = writeNetworkToEEPROM(server.arg("ssid"), server.arg("password"));
  int readNetworkFromEEPROMResult = readNetworkFromEEPROM(&eSsid, &ePassword);
  //restart
  resetFunc();
}


void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";

  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }

  server.send(404, "text/plain", message);

}

void startWebServer() {


   if (WiFi.status() != WL_CONNECTED) 
   { 
        send_to_thingspeak = false;
        
  Serial.print("Failed WIFI : Removing old configuration ... ");
  Serial.println(WiFi.disconnect() ? "Completed" : "Failed!");
        

       IPAddress local_IP(1,1,1,1);
       IPAddress gateway(1,1,1,0);
       IPAddress subnet(255,255,255,0);

  Serial.print("Failed WIFI : Configuring access point ... ");
  Serial.println(WiFi.softAPConfig(local_IP, gateway, subnet) ? "Done" : "Failed!");

  Serial.print("Droneponics access point is ... ");
  Serial.println(WiFi.softAP(apssid) ? "Ready" : "Failed!");

  Serial.print("Device congifuration address = http://");
  Serial.println(WiFi.softAPIP());
    
   }
    

  Serial.print("Setting esp8266 MDNS responder server  ... ");
  Serial.println(MDNS.begin("esp8266") ? "Started!" : "Failed!");

  server.begin();
  Serial.print("HTTP server ... Started\n");
  
    
    server.on("/", handleDroneponics);
    server.onNotFound(handleNotFound);
    server.on("/droneponics", handleDroneponicsUpdate);
    server.on("/confirmDroneponics", handleConfirmDroneponics);
  //  server.on("/logo", HTTP_GET, [](){
  //    server.send(SPIFFS, "/store_logo.png", "image/png");
  //  });
  
}


static void setupWifi()
{
  int readNetworkFromEEPROMResult = readNetworkFromEEPROM(&eSsid, &ePassword);

  WiFi.mode(WIFI_STA);
  Serial.print("Connecting to network " + eSsid);
  WiFi.begin(sssid, spassword);
    
  for(int16_t i = 0; i < 500; i++){
      if (WiFi.status() != WL_CONNECTED) { 
         Serial.print(".");
         delay(10);
      }else{
          Serial.print("... Connected  " + String(i));
          break;
      }
    }
  
  Serial.println("");
  Serial.println("Waiting on time sync..." + time(nullptr));
  
  if(WiFi.status() == WL_CONNECTED){
      digitalWrite(LED_BUILTIN, LOW);

      Serial.print("Droneponics time client:- ");
       timeClient.begin() ;
    
      Serial.println("Configured Time servers to " +  String(ntp_primary));
      configTime(0, 0, ntp_primary, ntp_secondary);

    }else{
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("Failed to connect to Wifi");
      Serial.println("setupWifi : Status of connection is = " + String(wifiStatusToString(WiFi.status())));
      Serial.println("setupWifi : Connecting to WiFi = " + WiFi.SSID());
      Serial.println("setupWifi : Connecting to using ssid = " + eSsid);
      Serial.println("setupWifi : Connecting to using password = " + ePassword);

    }

  startWebServer();
  Serial.println("Droneponics WiFi Connection Configuration has completed.");
   
}
