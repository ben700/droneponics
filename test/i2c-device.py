import io
import sys
import fcntl
import time
import copy
import string

num_of_bytes=31
I2C_SLAVE = 0x703


file_read = io.open(file="/dev/i2c-1", mode="rb", buffering=0)
for addr in range (11,15):
    fcntl.ioctl(file_read, I2C_SLAVE, addr)
    raw_data = self.file_read.read(num_of_bytes)
    print(raw_data)

