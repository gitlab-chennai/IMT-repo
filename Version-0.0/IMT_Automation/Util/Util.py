#!/usr/bin/python

import os
import subprocess
import sys
import re
import json
import socket
from time import sleep
import pprint
import time
import select

#from collections import OrderedDict

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

import constants as C

"""
     Module Name , Util.py
     Description , 
                   This module contains Class Util, which will have methods
                   related to network maintenance, querying the network 
                   information and about all existing machines in the network.
"""

PORT = 50123

class Socket(object):

    def __init__(self,socket_type):
        """
           Description, 
                   Constructor method which will be called during the 
                   creation of the object. Will Take in all possible 
                   class attributes for performing object specific 
                   intialization.

           Returns, None
        """
        print "Initializing the socket class constructor  "
        # Nothing much to instantiate.
        self.socket_type = socket_type
        localsocket = ""
        
    def CreateSocket(self,PORT=50123, whoami = "slave"):
        """
           Description,
                   This method is meant for creating a socket connection
                   with well known fixed port.
                   By default it creates a IPV4 Socket address and uses TCP/IP
                   for tranporting data from one node to another node.
                   This method would create the socket and bind the socket
                   with a particular port and then go in listening mode.

           Method Arguments, 
                   Nothing.

           Returns,
                   On Successful creation, this method should return 0.
                   On Failure, method will return a negative integer.

        """
     
        # This is a listener socket.
        # create a socket object
        self.localsocket = socket.socket()
	#        socket.AF_INET, socket.SOCK_STREAM)

        try:
            print "This is your port ",PORT
            self.localsocket.bind(('',PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            return -1

        # bind to the port
        if ( whoami == "slave"):
            # queue up to 20 requests
            # Making slave as listener and master always as a client socket.
            self.localsocket.listen(20)

        return self.localsocket

    def DestroySocket(self,conn):
        """
           Description,
                   This method is meant for closing the socket connection
                   which was created.
                   This has to check if the connection is still alive and 
                   then perform socket closure.

           Method Arguments,
                   socket connection address.

           Returns,
                   On Success, this method should return 0.
                   On Failure, method will return a negative integer.

        """
        conn.close()

    def SendSocketMessage(self,conn):
        """
           Description,
                   This method is meant for sending the socket message from
                   one host socket to another remote socket using the IP
                   address of the remote socket.

                   Socket can receive data of any size (in bytes)from its 
                   caller, but it can send data to the another remote socket
                   in a data chunk of 1024 bytes.

                   If incoming buffer is > 1024, then buffer needs to be
                   sent in chunks to the remote host.

                   After sending all the chunks(from the incoming buffer),
                   function can return to the caller.

           Method Arguments,
                   Remote Host IP Address,
                   Incoming buffer which can be of any size.

           Returns,
                   On Successful transporting the socket buffer, this method
                   should return 0.
                   On Failure, method will return a negative integer.

        """
        conn.sendall(msg)

    def ReceiveSocketMessage(self):
        """
           Description,
                   This method is meant for receiving the incoming buffer
                   from the remote socket and holding it in a buffer and sending 
                   it to the listener.

           Method Arguments,
                   Socket Buffer(That needs to be filled).

           Returns,
                   On Successful restart, this method should return 0.
                   On Failure, method will return a negative integer.

        """
        while(True):
            conn,addr = self.socketObj.accept()
            self.clients[addr] = c


    def IsSocketAlive(self):
        """
           Description,
                   This method is meant for checking if the socket 
                   connection is alive and usable.

           Method Arguments,
                   socket address

           Returns,
                   On Success(If alive), this method should return 0.
                   On Failure(If dead), method will return a negative integer.

        """
        return self.localsocket.isAlive()

   
    def dummy_socket_method(self):

        return "I am dummy socket class string "

class Util(Socket):

    def __init__(self):
        """
           Description, 
                   Constructor method which will be called during the 
                   creation of the object. Will Take in all possible 
                   class attributes for performing object specific 
                   intialization.

           Returns, None
        """
        self.SocketObj = Socket("socket.AF_INET")
   
    def RestartLogServerSocket(self):
        """
           Description,
                   This method is meant for restarting the log
                   server socket, if it is not reachable for
                   the master. Master after detecting the log server
                   socket is not reachable, will restart the
                   log server socket.

           Method Arguments,
                   Log Server Process ID,
                   Log Server Process IP,
                   Log Server Process Name

           Returns,
                   On Successful restart, this method should return 0.
                   On Failure, method will return a negative integer.

        """
        pass

    def PingPeer(self):
        """
           Description,
                  This method is meant for pinging/checking if the host IP 
                  is responding back to ping messages.

           Method Arguments,
                  Hostname as registered with the DNS (or)
                  IP Address of the host machine

           Returns,
                  On Successful Ping, this method should return 0
                  On Failure, method will return a negative integer.
        """
        with open(os.devnull, "w") as limbo:
            resp = subprocess.Popen([C.PING, C.PING_COUNT, C.PING_TIMEOUT, host], stdout=limbo, stderr=limbo).wait()

        if resp == 0:
            return 0
        else:
            return -1


    def RestartSlaveAgent(self, slaveIp):
        """
           Description,
                  This method is meant for restarting the slave agent
                  which will be running in the slave machine. This method 
                  should also verify that slave agent is running in the 
                  slave host machine. 

           Method Arguments :
                  IP Address (or) Host name of the Slave host machine.

           Returns,
                  On Successful restart, this method should return 0.
                  On Failure, method will return a negative integer.

        """
        pass

    def ReportSlaveMacs(self,subnet_addr):
        """
           Description,
                  This method is meant for collecting MAC information about
                  each slave that is existing in a particular subnet.

           Method Arguments,
                  Subnet address(Say for example,xx.xx.xx.xx)

           Returns,
                  On Success, Returns the list of mac addresses.
                  On Failure, method will return a negative integer.
                       There can be no failure as whatever collected 
                       is reported by this method.
                       If it returns None, it can be considered as 
                       failure.

        """
        # Using NMAP command to get the Mac Address of the systems in subset
        process1 = subprocess.Popen("nmap -sP 10.102.28.1/24",stdout=subprocess.PIPE,shell=True)
	process2 = subprocess.Popen("grep -i MAC",stdin=process1.stdout,stdout=subprocess.PIPE,shell=True)
        result = process2.stdout.readlines()
	
        # Reading the subprocess Result in a list
        mac_list=[]
	for element in result:
            mac_list.append(element[13:30])
       
        # Returning the list/-1

	if not mac_list:
            return -1
	else:
            return mac_list          


    def ScanAllPorts(self):
        """
           Description,
                  This method is meant for scanning all ports in the 
                  jack panel of each RACK or the tables. Possible way to
                  query the port(use/un-unused state) would be done by
                  querying the router.

           Method Arguments,
                  None

           Returns,
                  On Success, this method should return a dictionary with
                  Port ID and its state.
                  On Failure, method will return a negative integer.

        """
        pass

    def ConvertInfoToJSON(self):
        """
           Description,
                  This method is meant for converting the actual message
                  that is sent by the sender/caller as per mandated 
                  format. 

           Method Arguments :
                  Input Message(character string)or the text file path as per the mandated format.
                  Text file name 
                  File location of the JSON file.

           Returns,
                  On Success, this method should return 0.
                  On Failure, method will return a negative integer.

        """
        jsonFile = jsonPath + filename + ".json"
        try:
            fin = open(filePath, "r")
            with open(jsonFile, "w")as fout:
                while True:
                    line = fin.readline()
                    if line == "":
                        break
                    json.dump(line, fout, indent=1)

            fin.close()  
            return 0

        except Exception:
            return -1

    def Gather_IPMAC_Informaton(self, subnet):
        """
           Description,
                  This method is meant for collecting all IP & Mac
                  associated with each mac address for any given
                  subnet.

           Method Arguments :
                  Subnet address

           Returns,
                  On Success, this method should return a dictionary
                  containing IP information and MAC address.
                  On Failure, method will return a negative integer.
        """
        #macIpDict = OrderedDict()

        try:
            with open(C.TEMP_FILE, C.WRITE_MODE) as f:
                with open(os.devnull, C.WRITE_MODE) as limbo:
                    p = subprocess.Popen([C.NMAP, C.NMAP_OPT_SN, subnet], stdout=limbo).wait()
                p1 = subprocess.Popen([C.ARP, C.NO_DNS], stdout=f).wait()

            f = open(C.TEMP_FILE, C.READ_MODE)
            while True:
                line = f.readline()
                if line == "":
                    break
                newLine = line.split()
                mac = newLine[2]
                ip = newLine[0]
                macIpDict[mac] = ""
                macIpDict[mac] = ip
            return  macIpDict

        except Exception:
            return -1


    def GetAllSlaveStatus(self):
        """
           Description,
                  This method is meant for checking if the slaves 
                  are up and running and if they are reachable.

           Method Arguments :
                  List containing all slave IPs

           Returns,
                  On Success, a dictionary containing slave IP/hostname 
                  and their status.
                  On Failure, each slave will hold its respective status
                  in its value.

        """
        pass


    def CheckoutRepo(self):
        """
           Description,
                  This method is meant for doing IMT repo checkout using 
                  GIT from its develop branch(By default).

           Method Arguments :
                  NO Arguments (GIT URL should come from configuration)

           Returns,
                  On Success, returns 1.
                  On Failure, can return negative value.

        """
        print "git link from configaration is", configuration.GITLINK
        os.system(configuration.GITLINK)
        exit(0)



    def GetSlaveAgentVersion(self):
        """
           Description,
                  This method is meant for getting the existing slave agent 
                  version. this call is internal to the slave agent which will
                  return the slave agent version alone.

           Method Arguments :
                  Nothing.

           Returns,
                  On Success, returns the slave agent version
                  On Failure, return negative integer. 

        """
        pass



    def CheckSlaveAgentVersion(self):
        """
           Description,
                  This method is meant for checking if the running slave agent
                  version is equivalent to the slave version that is there in the 
                  IMT REPO. 

           Method Arguments :
                  Slave agent version

           Returns,
                  
                  If both values are same, return True.
                  On both slave version are different, it returns -1.

        """
        if(type=="windows"):
            if(Constants.Windows_SlaveAgentVersion==version):
                print "slave agent is latest"
                return 0
            elif(Constants.Windows_SlaveAgentVersion<version):
                print "slave agent version is not updated"
                exit(0)
            else:
                print "slave agent is the older one"
                return -1
        elif(type=="linux"):
            if(Constants.Linux_SlaveAgentVersion==version):
                print "slave agent is latest"
                return 0
            else:
                print "slave agent is the older one"
                return -1
        else:
            pass


    def KillSlaveAgent(self):
        """
           Description,
                  This method is meant for killing slave agent which is
           running in the remote slave.

                  Caller will be the master which will use this method to 
           kill the slave agent. This method sends a KILL message to the 
           remote slave machine's socket and waits for a STATUS from 
           remote socket.

           Method Arguments :
                  Remote slave machine's IP address.

           Returns,
                  On Success status from the remote socket, this returns 1.
                  On Failure, it returns negative integer.

        """
        pass


    def WaitForXMinutes(self,time_in_mts):
        """
           Description,
                  This method is meant for keeping the log server to wait 
           for X minutes.

           Log server will wait for X minutes after it has received it's first
           update from the slaves.

           Method Arguments :
                  Remote slave machine's IP address.

           Returns,
                  After waiting for X minutes, it returns 0.
                  Cannot result in a failure as it is simply a wait timer.

        """
        seconds = 60 * time_in_mts

        # Wait for seconds.
        time.sleep(seconds)


    def ReportListofSilentSlaves(self):
        """
           Description,
                  This method is meant for getting the list of slaves have not
           responded to the log server.

           Method Arguments :
                  Nothing.

           Returns,
                  On Success, returns a list containing the list of slave IPs.
                  On Failure, it returns negative integer(If problem persists
                                                          while getting 
                                                            slave IP)

        """
        pass

