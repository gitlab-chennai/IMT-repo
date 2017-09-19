import os
import sys
import socket
from time import sleep
import time

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

PORT = 50123

class Socket(object):
    def __init__(self,socket_type):
        print ("Initializing the Socket Class Constructor")
        self.socket_type = socket_type
        localsocket = ""
    
    def CreateSocket(self,PORT=50123, whoami = "slave"):
        self.localsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print ("This is your port %s"%PORT)
            self.localsocket.bind(('',PORT))
        except socket.error:
            print ("Bind Failed")
            return -1
        if ( whoami == "slave"):
            self.localsocket.listen(20)
        return self.localsocket
    
    def DestroySocket(self,conn):
        conn.close()

class Util(Socket):
    def __init__(self):
        self.SocketObj = Socket("socket.AF_INET")
    
    def WaitForXMinutes(self,time_in_mts):
        seconds = 60 * time_in_mts
        time.sleep(seconds)
