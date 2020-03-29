from datetime import datetime
import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)



answer = input("Are you sure you want to calibrate (y/n)")
print(answer)
if answer is None or answer != 'y':
    quit()
