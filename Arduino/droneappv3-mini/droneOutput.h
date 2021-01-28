#include "droneInclude.h"
    
Ezo_board PH = Ezo_board(99, "pH");       //create a PH circuit object, who's address is 99 and name is "PH"
Ezo_board EC = Ezo_board(100, "Conductivity");      //create an EC circuit object who's address is 100 and name is "EC"
Ezo_board RTD = Ezo_board(102, "Temperature");    //create an RTD circuit object who's address is 102 and name is "RTD"
Ezo_board DO = Ezo_board(97, "Dienssolved Oxygen");    //create a DO circuit object who's address is 97 and name is "DO"

//array of ezo boards, add any new boards in here for the commands to work with them
Ezo_board device_list[] = {
  PH,
  EC,
  RTD,
  DO
};



//enable pins for each circuit
const int EN_PH = 14;
const int EN_EC = 12;
const int EN_RTD = 15;
const int EN_AUX = 13;

Ezo_board* default_board = &device_list[0]; //used to store the board were talking to

//gets the length of the array automatically so we dont have to change the number every time we add new boards
const uint8_t device_list_len = sizeof(device_list) / sizeof(device_list[0]);

enum reading_step {REQUEST_TEMP, READ_TEMP_AND_COMPENSATE, REQUEST_DEVICES, READ_RESPONSE };          //the readings are taken in 3 steps
//step 1 tell the temp sensor to take a reading
//step 2 consume the temp reading and send it to the devices
//step 4 tell the devices to take a reading based on the temp reading we just received
//step 3 consume the devices readings

String ezoDelay = "600";

enum reading_step current_step = REQUEST_TEMP;                                    //the current step keeps track of where we are. lets set it to REQUEST_TEMP (step 1) on startup


int return_code = 0;                      //holds the return code sent back from thingSpeak after we upload the data

uint32_t next_step_time = 0;              //holds the next time we receive a response, in milliseconds
const unsigned long reading_delay = 1000;  //how long we wait to receive a response, in milliseconds
unsigned int poll_delay = 0;              //how long we wait between reading, in milliseconds

const unsigned long thingspeak_delay = 15000;                                     //how long we wait to send something to thingspeak

const unsigned long short_delay = 300;              //how long we wait for most commands and queries
const unsigned long long_delay = 1200;              //how long we wait for commands like cal and R (see datasheets for which commands have longer wait times)

float k_val = 0;                                    //holds the k value of the ec circuit





// determines how long we wait depending on the command
void select_delay(String &str) {
  if (str.indexOf("CAL") != -1 || str.indexOf("R") != -1) {
    delay(long_delay);
  } else {
    delay(short_delay);
  }
}
// used for printing either a success_string message if a command was successful or the error type if it wasnt
void print_error_type(Ezo_board &Device, const char* success_string) {
  switch (Device.get_error()) {             //switch case based on what the response code is.
    case Ezo_board::SUCCESS:
      Serial.print(success_string);   //the command was successful, print the success string
      break;

    case Ezo_board::FAIL:
      Serial.print("Failed ");        //means the command has failed.
      break;

    case Ezo_board::NOT_READY:
      Serial.print("Pending ");       //the command has not yet been finished calculating.
      break;

    case Ezo_board::NO_DATA:
      Serial.print("No Data ");       //the sensor has no data to send.
      break;
  }
}

void get_ec_k_value(){                                    //function to query the value of the ec circuit
  char rx_buf[10];                                        //buffer to hold the string we receive from the circuit
  EC.send_cmd("k,?");                                     //query the k value
  delay(300);
  if(EC.receive_cmd(rx_buf, 10) == Ezo_board::SUCCESS){   //if the reading is successful
    k_val = String(rx_buf).substring(3).toFloat();        //parse the reading into a float
  }
}


void print_help() {
  get_ec_k_value();
  Serial.println(F("Atlas Scientific I2C hydroponics kit                                       "));
  if(k_val > 9){
     Serial.println(F("For K10 probes, these are the recommended calibration values:            "));
  }
  else if(k_val > .9){
     Serial.println(F("For K1 probes, these are the recommended calibration values:             "));
  }
  else if(k_val > .09){
     Serial.println(F("For K0.1 probes, these are the recommended calibration values:           "));
  }
  
}


// prints the boards name and I2C address
void print_device_info(Ezo_board &Device) {
  Serial.print(Device.get_name());
  Serial.print(" ");
  Serial.print(Device.get_address());
}

void print_device_response(Ezo_board &Device) {
  char receive_buffer[32];                  //buffer used to hold each boards response
  Device.receive_cmd(receive_buffer, 32);   //put the response into the buffer

  print_error_type(Device, " - ");          //print if our response is an error or not
  print_device_info(Device);                //print our boards name and address
  Serial.print(": ");
  Serial.println(receive_buffer);           //print the boards response
}

void list_devices() {
  for (uint8_t i = 0; i < device_list_len; i++) {        //go thorugh the list of boards
    if (default_board == &device_list[i]) {              //if its our default board
      Serial.print("--> ");                             //print the pointer arrow
    } else {                                            //otherwise
      Serial.print(" - ");                              //print a normal dash
    }
    print_device_info(device_list[i]);                   //then print the boards info
    Serial.println("");
  }
}

void start_datalogging() {
  polling = true;                                                 //set poll to true to start the polling loop
  poll_delay = thingspeak_delay  - reading_delay * 2 - short_delay; //polling delay is how long how often we upload to thinkspeak minus the time it takes to take the readings
  send_to_thingspeak = true;
}

//handles the processing of commmands sent by the serial interface
void user_commands() {

  String serial_receive = "";                         //reset the string before processing it

  if (Serial.available()) {                           //if theres any characters in the UART buffer
    serial_receive = Serial.readString();             //get them until its a complete command
    Serial.print("> ");                               //print whatever we received
    Serial.println(serial_receive);
    serial_receive.toUpperCase();                     //turn the command to uppercase for easier comparisions
    serial_receive.trim();                            //remove all extra spaces and newlines
    polling = false;                                  //stop polling when we commmunicate with the device
    send_to_thingspeak = false;                       //stop sending to thinkspeak as well
    current_step = REQUEST_TEMP;                      //reset the polling sequnence
  }


  // the help command prints the menu of available options
  if (serial_receive == "HELP") {
    print_help();
  }
  // the list command prints the info of all available boards and which one receives individual commands
  else if (serial_receive == "LIST") {                    //if our command is list
    list_devices();
  }

  //the all command sends a command to all available boards and shows their responses
  else if (serial_receive.startsWith("ALL:")) {                               //if the command starts with ALL:
    String cmd = serial_receive.substring(serial_receive.indexOf(':') + 1);   //get the rest of the command after the : character

    for (uint8_t i = 0; i < device_list_len; i++) {                            //then send it to every board
      device_list[i].send_cmd(cmd.c_str());
    }

    select_delay(cmd);                                                        //wait for some time depending on the command

    for (uint8_t i = 0; i < device_list_len; i++) {                            //go through our list of boards and get their response
      print_device_response(device_list[i]);
    }
  }

  // the poll commmand starts the polling and sets the wait time between polls
  else if (serial_receive.startsWith("POLL")) {
    polling = true;                                                 //set poll to true to start the polling loop
    poll_delay = 0;                                                 //reset the polling delay so it doesnt use the one we set last but the default

    int16_t index = serial_receive.indexOf(',');                    //check if were passing a polling delay parameter
    if (index != -1) {                                              //if there is a polling delay
      float new_delay = serial_receive.substring(index + 1).toFloat(); //turn it into a float
      if (new_delay >= 1.0) {                                       //make sure its greater than our minimum time
        poll_delay = (new_delay * 1000.0) - reading_delay;          //convert to milliseconds and remove the reading delay from our wait
      } else {
        Serial.println("delay too short");                          //print an error if the polling time isnt valid
      }
    }
  }

  // the poll commmand starts the polling and sets the wait time between polls
  else if (serial_receive.startsWith("DATALOG")) {
    start_datalogging();
  }

  // all other commands are passed through to the default board unless they have an address prepended
  else if (serial_receive != "" ) {                                 //if we received any other commands
    int16_t index = serial_receive.indexOf(':');                    //check if the command contains a colon character, which is used for changing addresses

    if (index != -1) {                                              //if it contains a colon character
      bool addr_found = false;
      String name_to_find = serial_receive.substring(0, index);              //get the address out of the command
      name_to_find.toUpperCase();
      if (name_to_find.length() != 0) {                                              //if its valid
        //search through list and make device match the address
        for (uint8_t i = 0; i < device_list_len; i++) {
          if (name_to_find == device_list[i].get_name()) {               //if the address matches one of the boards in the list
            default_board = &device_list[i];                        //set that board as the default
            addr_found = true;                                      //indicate we changed the address
            break;                                                  //and exit the loop
          }
        }
        if (addr_found) {                                           //then send the rest of the command to that board
          default_board->send_cmd(serial_receive.substring(index + 1).c_str());
        } else {                                                    //otherwise print that we didnt find
          Serial.print("No device named ");
          Serial.println(name_to_find);
          return;
        }
      } else {
        Serial.println("Invalid name");
      }
    }
    else {                                                          //if theres no colon just pass the command to the default board
      default_board->send_cmd(serial_receive.c_str());
    }

    select_delay(serial_receive);                                   //wait for some time depending on the command

    print_device_response(*default_board);
  }
}

void receive_reading(Ezo_board &Device) {              // function to decode the reading after the read command was issued

  Serial.print(Device.get_name()); Serial.print(": "); // print the name of the circuit getting the reading

  Device.receive_read_cmd();              //get the response data and put it into the [Device].reading variable if successful

  print_error_type(Device, String(Device.get_last_received_reading(), 2).c_str());  //print either the reading or an error message
}
