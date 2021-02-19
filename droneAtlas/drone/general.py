
import socket
import time
from getmac import get_mac_address
import drone

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

def payload(payload):
    payload["bootTime"] = int(time.time())
    payload["deviceMAC"] = drone.get_mac()
    payload["deviceIP"] = drone.get_ip()
    payload["gethostname"] = drone.gethostname()
