#include <ESP8266WiFi.h>
 
const char* ssid = "HartleyAvenue"; // fill in here your router or wifi SSID
const char* password = "33HartleyAvenue"; // fill in here your router or wifi password
 #define RELAY 0 // relay connected to  GPIO0
WiFiServer server(80);
 
void setup() 
{
  Serial.begin(9600); // must be same baudrate with the Serial Monitor
 
  pinMode(RELAY,OUTPUT);
  digitalWrite(RELAY, LOW);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
  }
  
  // Start the server
  server.begin();
  
}
 
void loop() 
{
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) 
  {
    return;
  }
 
  // Wait until the client sends some data
  while(!client.available())
  {
    delay(1);
  }

  // Read the first line of the request
  client.flush();
 
  // Match the request
  int value = LOW;
  if (request.indexOf("/RELAY=ON") != -1)  
  {
    digitalWrite(RELAY,LOW);
    value = LOW;
  }
  if (request.indexOf("/RELAY=OFF") != -1)  
  {
    digitalWrite(RELAY,HIGH);
    value = HIGH;
  }
  
  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  this is a must
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
 
  client.println("<head>");
  client.println("<link rel=\"stylesheet\" type=\"text/css\" href=\"html/style.css\">");
  client.println("<title>Droneponics WiFi Configuration Page</title>");
  client.println("<link rel=\"icon\" href=\"html/favicon.ico\">");
  client.println("</head>");
                 
  client.print("Relay is now: ");
 
  if(value == HIGH) 
  {
    client.print("OFF");
  } 
  else 
  {
    client.print("ON");
  }
  client.println("<br><br>");
  client.println("Turn <a href=\"/RELAY=OFF\">OFF</a> RELAY<br>");
  client.println("Turn <a href=\"/RELAY=ON\">ON</a> RELAY<br>");
  client.println("</html>");
 
}
