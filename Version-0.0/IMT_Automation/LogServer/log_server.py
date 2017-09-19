#!/usr/bin/python

import os
import sys

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Util.Util import Util
import constants as C

import time

PORT_NUM = 40123

'''
Module,
       LogServer.py

Description,
       This module contains the log server class which will have 
       methods through which all interactions with log server will
       be made.   
'''

class log_server(Util):

    def __init__(self):
        print " Got here log _server constructor "
        '''
        Description,
                 Constructor method for the class, log_server. All
        attributes related to log_server will be initialized and 
        caller will have to make sure that all required arguments are 
        passed in during object initialization.

        '''
        #super(log_server,self).__init__()
        #Util.__init__(self) 
        self.UtilObj = Util()
        self.SocketObj = self.UtilObj.SocketObj

    def PushLogs(self, hostname):
        '''
        Description,
                 This method is meant for pushing the logs/activities
        which it has performed during the course of run. It has to make sure
        that  prepared for its own sake and post it to the log server through
        the slave repo.

        Method Arguments,
                  Log Server IP/Host name

        Returns,
                  On Success, returns 0.
                  On Failure, returns negative integer.

        '''
        pass
        

    def CheckSlaveTargetRunning(self, hostname):
        '''
        Description,
                 This method is meant for checking if the slave machine is up
        and running.

        Method Arguments,
                 Slave IP / Host Name

        Returns,
                 0, On Success.
                 Negative Number, on failure.
        '''

        if self.utilObj.PingPeer(hostname):
            return 0

        else:
            return -1

    def CreateMasterRepo(self, RepoPath, EmacsFile):
        '''
        Description,
                 This method is meant is for creating generic log file 
        for master and slave which will be a placeholder for capturing all
        activities of slave and master.

        Method Arguments,
                 Generic Log File Name

        Returns,
                 0, On Success.
                 Negative Number, on failure.

        '''
        try:
            if not os.path.exists("%s"%RepoPath):
                os.makedirs("%s"%RepoPath)

            fp1 = open("%s"%EmacsFile,'r')
            IpList = fp1.readlines()

            os.chdir("%s"%RepoPath)
            IpListDir = glob.glob("[0-9]*[0-9]")

            for ip in IpList:
                if not ip.strip("\n") in IpListDir:
                    os.makedirs("%s"%ip.strip("\n"))

            return 0

        except:
            return -1

    def CheckSlaveLogFilePresence(RepoPath,SlaveLogFile,MacId):
        '''
        Description,
                 This method checks if slave has correctly copied its log
        file into its repository. This should also ensure that the log file
        copied is latest (or) recent based on the time stamp.

        Method Arguments,
                 Slave IP/Host Name (or)
                 Slave MAC Address

        Returns,
                 0, On Success.
                 Negative Number, on failure.

        '''
        Path = "%s/%s"%(RepoPath,MacId)

        if not os.path.exists("%s"%Path):
            print "Slave log path doesnot exist!!!"
            return -1

        os.chdir("%s"%Path)
        output = subprocess.check_output("ls -Art | tail -n 1", shell=True)

        timeCreated = os.path.getctime(SlaveLogFile)      #Checking the file creation time
        fileTime = d.datetime.fromtimestamp(timeCreated)
    
        interval = d.timedelta(minutes=-20) #Time Interval of 20minutes from Current time by using timedelta
        currentTime = d.datetime.now()
        checkTime = currentTime + interval  #Time after deducting 20minutes from Current time

        if fileTime >= checkTime:
            print "Latest logs updated or copied.."
            return 0
        else:
            print "Latest logs not copied.."
            return -1

    def UpdateSlaveInfo(self):
        '''
        Description,
                This method is to report that the slave agent has not
        updated its log file and that information needs to be recorded
        in the generic log file.

        Method Arguments,
                Master Log File Location,
                Slave Machine(Whose log file is missing) 

        Returns,
                0, On Success.
                Negative Number, on failure.

        '''
        pass

    def ArchiveLogs(self):
        '''
        Description,
                This method is to archive slave logs periodically from its 
        repository. It has to periodially do this activity for every X minutes.

        Method Arguments,
                Log File Repo Path
                Threshold Size Limit

        Returns,
                0, On Success.
                Negative Number, on failure.

        '''
        pass

    def LogServerMain(self):
        pass
        
        """ Starting the log object
        masterRepo = "location of repo"
        inactiveSlave = {}
        while True:
            if os.path.exists(masterRepo):
                self.utilObj(WaitForXMinutes())
                ipMac = self.utilObj.Gather_IPMAC_Informaton("10.102.29.1/24")
                for key, value in ipMac.iteritems():
                    if self.CheckSlaveLogFilePresence(ip, mac)
                        continue
                    else:
                        inactiveSlave[mac] = ip
                queue.put(inactiveSlave)
        """
    def handle_incoming_socket(self,master_socket_conn,addr):
        while True:
            #Receiving from client
            data = master_socket_conn.recv(1024)
            if(data == "send_data"):
                print "Give overall slave status "
                self.slave_inventory_check()
                self.send_inactive_slave_info()
                reply="done"
            elif(data == "kill"):
                #Self Terminate.
                reply = "done"
            elif(data == "hello_ping"):
                reply = "hello_ping"
            else:
                continue
                # Lets do a retry.
            master_socket_conn.sendall(reply)
        master_socket_conn.close()

    #Function for handling connections. This will be used to create threads
    def connect2Master(self):
        self.local_socket = self.SocketObj.CreateSocket(PORT_NUM)

        if (self.local_socket != None):
            return -1

        #infinite loop so that function do not terminate and thread does not end.
        while True:
            master_socket,addr = self.local_socket.accept()
            HandleClient = Thread(target=handle_incoming_client, args=(master_socket,addr))
             #print " Monitor Log Server Started"
            HandleClient.start()

        self.local_socket.close()

if __name__ == "__main__":
    
    lgserver = log_server()
    print "Log object created"

    '''
       Listing log server action items

    '''   

    # master_repo_exists = check_master_repo()
    # if ( master_repo_exists == False ):
    #     lgserver.CreateMasterRepo()

    lgserver.connect2Master()


       
