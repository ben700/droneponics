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
