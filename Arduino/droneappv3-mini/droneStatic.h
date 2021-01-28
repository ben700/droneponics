#include "droneInclude.h"


// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

ESP8266WebServer server(80);

WiFiClient  client;                                              //declare that this device connects to a Wi-Fi network,create a connection to a specified internet IP address

void(* resetFunc) (void) = 0;

//storage
HashType<char*,char*> ledStatusRawArray[2];
HashMap<char*,char*> ledStatus = HashMap<char*,char*>( ledStatusRawArray , 2 );

HashType<char*,char*> restartCodesRawArray[5];
HashMap<char*,char*> restartCodes = HashMap<char*,char*>( restartCodesRawArray , 5 );


void setupDroneStatic()
{
   ledStatus[0]("0","Off");
   ledStatus[1]("1","On");

   restartCodes[0]("P","Powered Off");
   restartCodes[1]("S","Software Reset");
   restartCodes[2]("B","Brown Out");
   restartCodes[3]("W","Watchdog");
   restartCodes[4]("U","Unknown");

}

char* string2char(String command){
    if(command.length()!=0){
        char *p = const_cast<char*>(command.c_str());
        return p;
    }
}

int writeNetworkToEEPROM(const String &strNetwork, const String &strPassword)
{
  byte lenNetwork = strNetwork.length();
  byte lenPassword = strPassword.length();
  
  EEPROM.write(addressEEPROM, lenNetwork);
  EEPROM.write(addressEEPROM+1, lenPassword);
  
  for (int i = 0; i < lenNetwork; i++)
  {
    EEPROM.write(addressEEPROM + 2 + i, strNetwork[i]);
  }
  
  for (int j = 0; j < lenPassword; j++)
  {
    EEPROM.write(addressEEPROM + lenNetwork + 2 + j, strPassword[j]);
  }
  
 if (EEPROM.commit()) {
      Serial.println("EEPROM successfully committed");
    } else {
      Serial.println("ERROR! EEPROM commit failed");
    }
  
  return addressEEPROM + 2 + lenPassword + lenNetwork;
}

int readNetworkFromEEPROM(String *strNetwork, String *strPassword)
{

  byte lenNetwork = EEPROM.read(addressEEPROM);
  byte lenPassword = EEPROM.read(addressEEPROM+1);


  char dataNetwork[lenNetwork + 1];
  char dataPassword[lenPassword + 1];

  for (int i = 0; i < lenNetwork; i++)
  {
    dataNetwork[i] = EEPROM.read(addressEEPROM + 2 + i);

  }
  dataNetwork[lenNetwork] = '\0'; // the character may appear in a weird way, you should read: 'only one backslash and 0'
  *strNetwork = String(dataNetwork);

  for (int i = 0; i < lenPassword; i++)
  {
    dataPassword[i] = EEPROM.read(addressEEPROM + lenNetwork + 2 + i);

  }
  dataPassword[lenPassword] = '\0'; // the character may appear in a weird way, you should read: 'only one backslash and 0'
  *strPassword = String(dataPassword);
 
  return lenNetwork;

}


int clearNetworkToEEPROM()
{
  
  for (int i = addressEEPROM; i < 512; i++)
  {
    EEPROM.write(i, '\0');
  }
  
 if (EEPROM.commit()) {
      Serial.println("EEPROM successfully committed");
    } else {
      Serial.println("ERROR! EEPROM commit failed");
    }
  
  return 512;
}

String wifiStatusToString(wl_status_t status) {
  switch (status) {
    case WL_NO_SHIELD: return "WL_NO_SHIELD";
    case WL_IDLE_STATUS: return "WL_IDLE_STATUS";
    case WL_NO_SSID_AVAIL: return "WL_NO_SSID_AVAIL";
    case WL_SCAN_COMPLETED: return "WL_SCAN_COMPLETED";
    case WL_CONNECTED: return "WL_CONNECTED";
    case WL_CONNECT_FAILED: return "WL_CONNECT_FAILED";
    case WL_CONNECTION_LOST: return "WL_CONNECTION_LOST";
    case WL_DISCONNECTED: return "WL_DISCONNECTED";
  }
}
