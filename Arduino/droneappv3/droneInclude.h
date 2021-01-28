#ifndef DRONEPONICS_IDENTIFIER
#define DRONEPONICS_IDENTIFIER
    #include <Wire.h>
    #include <EEPROM.h>

    #include <ESP8266WebServer.h>
    #include <ESP8266mDNS.h>
    #include <ESP8266WiFi.h>
    #include <WiFiUdp.h>
    #include <NTPClient.h>
    #include <time.h>
    #include "FS.h"
    #include <CloudIoTCore.h>
    #include "WiFiClientSecureBearSSL.h"

    #include <MQTT.h>
    #include <CloudIoTCoreMqtt.h>

    #include <Ezo_i2c.h>
    #include <HashMap.h>
    #include <CloudIoTCore.h>
    #include "ThingSpeak.h"
    
    #include <Base64.h>

    #include "droneINI.h" 
    #include "droneClass.h"
    #include "droneStatic.h"
    #include "droneWeb.h"
    #include "droneInput.h"
    #include "droneponics.h"
#endif
