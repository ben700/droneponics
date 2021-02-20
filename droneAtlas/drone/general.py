
import socket
import time
from getmac import get_mac_address
import drone
import os

# get mac address
def get_mac(interface="wlan0", p=0):
    #return value
    return get_mac_address(interface)

def gethostname():
    return socket.gethostname()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getBootPayload(__payload):
    __payload["bootTime"] = int(time.time())
    __payload["deviceMAC"] = drone.get_mac()
    __payload["deviceIP"] = drone.get_ip()
    __payload["gethostname"] = drone.gethostname()

def fixMe():
    os.system('sh /home/pi/updateDroneponics.sh')
    os.system('sudo reboot')

def noSUDO():
    os.system("sudo chmod 777 /dev/serial0")
    os.system("sudo chown pi:pi /dev/serial0")
