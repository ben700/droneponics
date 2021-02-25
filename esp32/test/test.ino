#include <ESP8266WiFi.h>
 
const char* ssid = "HartleyAvenue"; // fill in here your router or wifi SSID
const char* password = "33HartleyAvenue"; // fill in here your router or wifi password



WiFiServer server(80);
 
void setup() 
{
  Serial.begin(9600); // must be same baudrate with the Serial Monitor
 
  pinMode(RELAY,OUTPUT);
  digitalWrite(RELAY, LOW);
  WiFi.hostname("droneTest")
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
    return;
  }

  // Read the first line of the request
  client.flush();

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  this is a must
  
  client.println("<html>");
 
  client.println("<head>");
  client.println("<link rel=\"stylesheet\" type=\"text/css\" href=\"html/style.css\">");
  client.println("<title>Droneponics WiFi Configuration Page</title>");
  client.println("<link rel=\"icon\" href=\"html/favicon.ico\">");
  client.println("</head>");
  
  client.println("<br><br>");
  client.print("Test ico ");
  client.println("<br><br>");
  client.print("Test title ");
  client.println("<br><br>");
  client.print("Test style");
  client.println("<br><br>");
  client.print("Test ip");
  
 
  client.println("</html>");
 
}
