
#ifndef DEVICEID
#define DEVICEID "HUZZAHESP8266-2"
#endif

#ifndef APSSID
#define APSSID "DroneponicsAP"
#endif

String eSsid;
String ePassword;


/* Set these to your desired credentials. */
const char *apssid = APSSID;
const char *appassword = "";

const char* sssid = "HartleyAvenue";
const char* spassword = "33HartleyAvenue";

const long myChannelNumber = 1280631;                            //Your Thingspeak channel number
const char * myWriteAPIKey = "74NEO0MNO4J3OYNI";                 //Your ThingSpeak Write API Key


// Cloud iot details.
const char* project_id = "drone-302200";
const char* location = "europe-west1";
const char* registry_id = "droneDevice";
const char* device_id = DEVICEID;

// Configuration for NTP
const char* ntp_primary = "time.google.com";
const char* ntp_secondary = "time1.google.com";

// Time (seconds) to expire token += 20 minutes for drift
const int jwt_exp_secs = 3600; // Maximum 24H (3600*24)


const char* deviceBootTopic = "/deviceBoot";
const char* sensorReadingTopic = "";

 
byte addressEEPROM =0;

bool polling = false;                     //we start off not polling, change this to true if you want polling on startup
bool send_to_thingspeak = false;


// To get the private key run (where private-key.pem is the ec private key
// used to create the certificate uploaded to google cloud iot):
// openssl ec -in <private-key.pem> -noout -text
// and copy priv: part.
// The key length should be exactly the same as the key length bellow (32 pairs
// of hex digits). If it's bigger and it starts with "00:" delete the "00:". If
// it's smaller add "00:" to the start. If it's too big or too small something
// is probably wrong with your key.

unsigned char private_key[] = {
    0x5b, 0x65, 0xbc, 0xc0, 0x9f, 0xf5, 0x63, 0x74, 0xe3, 0xa3, 0x0f, 0x7d, 0x93, 0x8b, 0xc1,
    0xeb, 0x46, 0xc6, 0x59, 0xdb, 0xa5, 0xdb, 0xf0, 0xbf, 0x85, 0x98, 0xd6, 0x44, 0x8d, 0xed,
    0xe7, 0x63};
  
const unsigned char  Drone_private_key[] = {
  0x2c, 0x8d, 0x87, 0xaf, 0x93, 0xaa, 0x7a, 0x54, 0x80, 0xde, 0xc4, 0xd8, 0x73, 0xf6, 0xe1,
  0x4c, 0xa4, 0xce, 0x07, 0x80, 0xb0, 0x6b, 0x37, 0xfc, 0x2f, 0x61, 0xdf, 0x2a, 0xfb, 0x77,
  0x14, 0xf4};
  
const unsigned char  HUZZAHESP8266_private_key[] = {
  0x97, 0x76, 0x3f, 0x15, 0x0a, 0xe0, 0x93, 0xfa, 0x8a, 0xd7, 0x3c, 0x34, 0x74, 0x26, 0x2f, 
  0xc5, 0x9f, 0xa8, 0x0c, 0xe0, 0x4e, 0x9c, 0xfa, 0x62, 0xb7, 0x87, 0xbb, 0xe1, 0x8b, 0x4f, 
  0x77, 0x0c};

const unsigned char  HUZZAHESP82662_private_key[] = {
    0x5b, 0x65, 0xbc, 0xc0, 0x9f, 0xf5, 0x63, 0x74, 0xe3, 0xa3, 0x0f, 0x7d, 0x93, 0x8b, 0xc1,
    0xeb, 0x46, 0xc6, 0x59, 0xdb, 0xa5, 0xdb, 0xf0, 0xbf, 0x85, 0x98, 0xd6, 0x44, 0x8d, 0xed,
    0xe7, 0x63};

    

// Certificates for SSL on the LTS server
const char* primary_ca = "-----BEGIN CERTIFICATE-----\n"
    "MIIBxTCCAWugAwIBAgINAfD3nVndblD3QnNxUDAKBggqhkjOPQQDAjBEMQswCQYD\n"
    "VQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExMQzERMA8G\n"
    "A1UEAxMIR1RTIExUU1IwHhcNMTgxMTAxMDAwMDQyWhcNNDIxMTAxMDAwMDQyWjBE\n"
    "MQswCQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExM\n"
    "QzERMA8GA1UEAxMIR1RTIExUU1IwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATN\n"
    "8YyO2u+yCQoZdwAkUNv5c3dokfULfrA6QJgFV2XMuENtQZIG5HUOS6jFn8f0ySlV\n"
    "eORCxqFyjDJyRn86d+Iko0IwQDAOBgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUw\n"
    "AwEB/zAdBgNVHQ4EFgQUPv7/zFLrvzQ+PfNA0OQlsV+4u1IwCgYIKoZIzj0EAwID\n"
    "SAAwRQIhAPKuf/VtBHqGw3TUwUIq7TfaExp3bH7bjCBmVXJupT9FAiBr0SmCtsuk\n"
    "miGgpajjf/gFigGM34F9021bCWs1MbL0SA==\n"
    "-----END CERTIFICATE-----\n";

const char* backup_ca = "-----BEGIN CERTIFICATE-----\n"
    "MIIB4TCCAYegAwIBAgIRKjikHJYKBN5CsiilC+g0mAIwCgYIKoZIzj0EAwIwUDEk\n"
    "MCIGA1UECxMbR2xvYmFsU2lnbiBFQ0MgUm9vdCBDQSAtIFI0MRMwEQYDVQQKEwpH\n"
    "bG9iYWxTaWduMRMwEQYDVQQDEwpHbG9iYWxTaWduMB4XDTEyMTExMzAwMDAwMFoX\n"
    "DTM4MDExOTAzMTQwN1owUDEkMCIGA1UECxMbR2xvYmFsU2lnbiBFQ0MgUm9vdCBD\n"
    "QSAtIFI0MRMwEQYDVQQKEwpHbG9iYWxTaWduMRMwEQYDVQQDEwpHbG9iYWxTaWdu\n"
    "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEuMZ5049sJQ6fLjkZHAOkrprlOQcJ\n"
    "FspjsbmG+IpXwVfOQvpzofdlQv8ewQCybnMO/8ch5RikqtlxP6jUuc6MHaNCMEAw\n"
    "DgYDVR0PAQH/BAQDAgEGMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFFSwe61F\n"
    "uOJAf/sKbvu+M8k8o4TVMAoGCCqGSM49BAMCA0gAMEUCIQDckqGgE6bPA7DmxCGX\n"
    "kPoUVy0D7O48027KqGx2vKLeuwIgJ6iFJzWbVsaj8kfSt24bAgAXqmemFZHe+pTs\n"
    "ewv4n4Q=\n"
    "-----END CERTIFICATE-----\n";
