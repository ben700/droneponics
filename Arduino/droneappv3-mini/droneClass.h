class Channel
{
private:
  int currentStatus;
  unsigned int state = 0;
  String Name;
  int Num;

public:
  // Constructor
  Channel(String _Num, String _Name)
  {

    Wire.beginTransmission(i2c_address);
    Wire.write(0x00);
    Wire.write(0x01);
    Wire.endTransmission();   
    this->Num = _Num;
    this->Name =_Name;
  }
  // Destructor
  ~Channel()
  {
    this->Name ="";
  }

  void switchOn() {this.state=1;}
  void switchOff() {this.state=0;}
  unsigned int  getState() {return this.state;}
  
  String getPayload(){

    return "\t\t" + this->Name + " : " + Sring(getState()) + ",\n";
  }
    
  
};

class Board
{
private:

  Channel[16] _Channels;
  String Name;
  
public:
  // Constructor
  Channel(String _Name)
  {
      Wire.beginTransmission(i2c_address);
      Wire.write(0x00);            // A register
      Wire.write(0x00);            // set all of port A to outputs
      Wire.endTransmission();

      Wire.beginTransmission(i2c_address);
      Wire.write(0x01);            // B register
      Wire.write(0x00);            // set all of port B to outputs
      Wire.endTransmission();      

    this->Name = _Name;
    for (int i =0 ; i < 16 ; i ++) {
      this->_Channels[i] = new Channel(i, "Channel " + String(i)); 
    }
    
  }
  // Destructor
  ~Channel()
  {
    this->Name ="";
    delete []Channel;
  }

  void turnOn(int num){
    this->_Channels[i].switchOn();
    commmit();
  }
  void turnOff(int num){
    this->_Channels[i].switchOff();
    commmit();
  }
  
  void turnOn(String Name)
  {
    for (int i =0 ; i < 16 ; i ++) {
      if(this->_Channels[i].Name == Name) this->_Channels[i].switchOn(); 
    }
    commmit();    
  }
  
  void turnOff(String Name)
  {
    for (int i =0 ; i < 16 ; i ++) {
      if(this->_Channels[i].Name == Name) this->_Channels[i].switchOff(); 
    }  
    commmit();
  }
  
  void turnAllOn(String Name)
  {
    for (int i =0 ; i < 16 ; i ++) {
      this->_Channels[i].switchOn(); 
    }
    commmit();    
  }
  
  void turnAllOff(String Name)
  {

    for (int i =0 ; i < 16 ; i ++) {
      this->_Channels[i].switchOff(); 
    }
    commmit();
  }
  
  void commmit(){

    unsigned int i2c_register = 0b;
    for (int i =0 ; i < 16 ; i ++) {
      i2c_register += this->_Channels[i].getState(); 
    }
    
    unsigned char variable_LOW = lowByte(i2c_register);
    unsigned char variable_HIGH = highByte(i2c_register);

    Wire.beginTransmission(i2c_address);
    Wire.write(0x12);                     // address bank A
    Wire.write(variable_LOW);
    Wire.endTransmission();
     
    Wire.beginTransmission(i2c_address);
    Wire.write(0x13);                     // address bank B
    Wire.write(variable_HIGH);
    Wire.endTransmission();
  }

  String getPayload (){
    String payload = "Device : {" + this->Name;
  
    for (int i =0 ; i < relayBoardSize ; i ++) {
      payload += relayBoard[i]->getPayload(); 
    }
    payload = payload.subString(0,payload.length() - 2);
    payload += "}"
    return payload;
  }

  
};


class Network
{
private:
  int _arrSize=0;
  int currentSize;
  String *_mySSIDList;

public:
  // Constructor
  Network(int arrSize)
  {
     this->currentSize =0;
    _arrSize = arrSize;
    _mySSIDList = new String[arrSize];
  }

  // Destructor
  ~Network()
  {
    this->currentSize =0;
    delete []_mySSIDList;
  }

  void addElement(const String *element)
  {    
    if(!findElement(element))
    {
      _mySSIDList[this->currentSize] = *element;
      this->currentSize++;
    }
  }

  String& getElement(int position) const
  {
    return _mySSIDList[position];
  }
  
  bool findElement(const String *element) const
  {
    
   for (int i = 0; i < this->currentSize ; i++)
   {
        if(_mySSIDList[i] == *element){
          return true;
        }
    }
    
    return false;
  }
  
  int getCurrentSize()
  {
    return this->currentSize;
  }
  
  void printAll()
  {
   Serial.print("Network list size = " + String(this->currentSize) + "\n");
    
   for (int i = 0; i < _arrSize; i++)
   {
         Serial.print("Network id = " + String(_mySSIDList[i]) + "\n");
   }
    
  }
};
