#!/usr/bin/python

import os
import sys
import logging
import datetime


from threading import Thread, Condition
from threading import Lock as threadLock
from multiprocessing import Process

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

#from LogServer.log_server import log_server
from Util.Fabric import Fabric
from Util.Util import Util
from Util.Fabric import FileTransfer 
import time
import os
from Queue import Queue
import random
import subprocess
import re

#Create logger to be used accross all modules
logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG)

PORT_NUM = 50005

class Master(Util):

    def __init__(self):
        """ 
           Description
                   Constructor method which will be called during the
                   creation of the object. Will take in all possible
                   class attributes for performing object specific
                   intialization.

           Method Arguments,
                   TBD

           Returns,
                   Returns None.
        """
        #super(Master,self).__init__()
        # log server object.
        self.UtilObj = Util()
        # data structure carrying IP and mac information
        self.ipmac = {}
        self.ipmac_old = {}
        self.ipmac_queue = Queue()
        self.ipmac_condition = Condition()

        self.logger_queue = Queue()
        self.logger_condition = Condition()
        self.signal_queue = Queue()


    def MonitorDiskSize(self):
        """
           Description,
                   Will check if the size of the disk given in the input
           parameter exceeds the threshold and if it exceeds there should
           be critical warning message logged and the script should stop 
           running. This method can be used to monitor the disk size 
           of the log server repository. This method will also log 
           warning messages if the disk size comes closer to the threshold 
           limit specified.

           Method Arguments,
                   disk name, threshold limit.

           Returns,
                   0 on success and -1 on failure.

        """
        while True:
            try:
                self.tlock.acquire()    
                #print " Lock acquired by Monitoring disk. Started \n"
                
                #time.sleep(5)
                # Code to be executed here
                self.tlock.release()
                #print " Lock released by Monitoring disk.  \n"
                self.logObj.WaitForXMinutes("X")

            except Exception, e:
                print e
                self.tlock.release()       

    def MonitorLogServer(self):
        """
           Description,
                   Will check if the log server process is running. This will 
           be a thread that will be running continuously. If the log server 
           process is not running this method will call RestartLogServer
           method.

           Method Arguments,
                   process ID of the log server, logserver name, IP

           Returns,
                   0 on success and -1 on failure.

        """
        while True:
            try:
                tlock.acquire()
                #print " Lock acquired by Monitoring LogServer. Started \n"
               #time.sleep(5)
                # Code to be executed here
                tlock.release()
#                print " Lock released by Monitoring LogServer. \n"
                self.logObj.WaitForXMinutes("X")

            except Exception, e:
                print e
                tlock.release()

    def RestartLogServerSocket(self):
        """
           Description,
                   This method is meant for restarting the log server
           socket, if the master could not establish a connection with the 
           log server the log server socket should be restarted.

           Method Arguments,
                   log server socket and port address.

           Returns,
                   0 on success and -1 on failure

        """
        pass

    def RestartLogServer(self):
        """
           Description
                  This method is meant for restarting the log server. 

           Method Arguments,
                  Process ID of the log server, logserver name, IP address

           Returns,
                  0 on success and -1 on failure

        """
        pass

    def ReportLogServerFailure(self):
        """
           Description,
                  This method is meant for sending a mail to the administrator 

           Method Arguments,
                  email Id of the administrator,
                  message, 
                  Log Server Process ID/IP/Name, 
                  No of Retries

           Returns,
                  0 on success and -1 on failure

        """
        host = "mySMTP.server.com"
        subject = "Log Server Failure"
        to_addr = email_admin
        from_addr = email_log
        text = message
        body = string.join(("From: %s" % from_addr, "To: %s" % to_addr,
                                        "Subject: %s" % subject  ,
                                        "",
                                        text
                                        ), "\r\n")
        server = smtplib.SMTP(host)

        for i in range(retries):
            if self.RestartLogServer() == 0:
                print " Log Server Restarted"
                break
        else:
            try:
                server.sendmail(from_addr, [to_addr], body)
                server.quit()
                return 0
            except Exception, e:
                print e
                return -1  

    def clone_IMT_Repo(self):
        print "Cloning IMT Repo locally ..."
        os.system("git clone git@gitlab-chennai:IMT/IMT.git /opt/IMT")

    def cleanup(self):
        print "Performing Cleanup Tasks ..."
        os.system("rm -rf /opt/IMT")

    def InitializeMaster(self):
        """
           Description,  
                  This method is meant for starting the master process 
           and all the sub processes.

           Method Arguments,
                  None

           Returns,
                  0 on Success and -1 on Failure.

        """
        # starting the Log Server
        #cmd = "path of log server exe"
        #os.system(cmd)
        
        # Starting thread to get IP and MAC information.
        # This thread would run as daemon for ever and its task is to 
        # get IP and MAC information for the list of subnets provided.

        #IPMAC_container_thread = Thread(target=self.get_IPMAC_info, args=())
        #IPMAC_container_thread.daemon = True
        #print "get_IPMAC_info read started"
        #IPMAC_container_thread.start()

        # starting thread to Update Slave Agent 
        # Marking this thread to run as a ever running daemon.

        #updateSlaveAgentThread = Thread(target=self.SlaveOps, args=())
        #updateSlaveAgentThread.daemon = True
        #print "SlaveOps Thread Started"
        #updateSlaveAgentThread.start()

        #getSlaveInfo = Thread(target=self.collectSlaveInfo, args=())
        #getSlaveInfo.daemon = True
        #print "CollectSlaveInfo Started"
        #getSlaveInfo.start()

        while(True):

            self.clone_IMT_Repo()
            self.SlaveOps()
            time.sleep(5)
            self.collectSlaveInfo()
            self.UtilObj.WaitForXMinutes(1)
            #self.cleanup()

        # starting thread to convert info to Json
        # Marking this thread to run as a ever running daemon.
        # convertToJsonThread = Thread(target=self.ConvertSlaveInfo, args=(),daemon=True)
        # print " Convert Info To Json Started"
        # convertToJsonThread.start()

        #convertToJsonThread.join()
        # print " Update Slave Agent ended"
       
        #print "Wait for all 3 threads completion "
        #IPMAC_container_thread.join()

        #updateSlaveAgentThread.join()

        #getSlaveInfo.join()
      
    def GetSlaveInfo(self):
        """
           Description,
                  This method is meant for checking whether slave is up and
           running and will get the OS currently running on the slave machine.

           Method Arguments,
                  List of all slave IPs

           Returns,
                  Alive slave list, down slave list

        """
        pass

    def ScanAllPorts(self):
        """
           Description,
                  This method is meant for checking all the ports in the 
           lab to see if they are connected to a slave. Will get the MAC and 
           the IP address.
                  
           Method Arguments,
                  None

           Returns,
                  A list of connected ports, a list of unused ports.
                  Modified : A dictionary with MAC as the key and IP as the value for all the hosts present in the subnet.
          

        """
        pass
                         
    def getLinuxVariant(self,FabricObj):
        """
           Description,
                  This method is meant for checking if the slave 
           agent/process in the slave machine is up and running.

           Method Arguments,
                   slave IP

           Returns,
                  0 on success and -1 on failure.

        """
        os_variant = FabricObj.execute(
                                "uname -s",
                                path='.',
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )

        if(os_variant != None):
            return os_variant  

    def IsSlaveRunning(self,FabricObj,unix_variant):
        """
           Description,
                  This method is meant for checking if the slave 
           agent/process in the slave machine is up and running.

           Method Arguments,
                   slave IP

           Returns,
                  0 on success and -1 on failure.

        """
        cmd_string = ""
        if(unix_variant == "VMkernel"):
            cmd_string = "ps -c | grep \"Slave.py\" | grep -v grep"
        else:
            cmd_string = "ps -eaf | grep \"Slave.py\" | grep -v grep"

        status = FabricObj.execute(
                                cmd_string,
                                path='.',
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )

        ret_status = re.search('Slave.py',status)
        if(ret_status != None):
            return True 
        return False
    def StopFirewall(seld,FabricObj):
         status = FabricObj.execute(
                                "cat /etc/issue",
                                path='.',
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )

         ret_status = re.search('SUSE',status)
         if(ret_status != None):
             status = FabricObj.execute(
                                "rcSuSEfirewall2 stop",
                                path='.',
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                                 )
         status1 = FabricObj.execute(
                                "systemctl stop firewalld",
                                path='.',
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )
         print "status--------",status

    def CheckIfSlaveAgentPresent(self,FabricObj):
        """
           Description,
                  This method is meant for checking if the slave agent file
           is present in the slave machine.

           Method Arguments,
                  Slave IP

           Returns,
                  0 on success and -1 on failure

        """
        status = FabricObj.execute(
                                "ls /opt | grep [I]MT",
                                path='.',
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )

        if (re.search('IMT',status)):
            return True
        else:
            return False


    def PushSlaveAgent(self,FabricObj,unix_variant,hostname):
        """
           Description,
                  This method is meant for copying all the required files 
           to run the slave agent in a path in the slave machine

           Method Arguments,
                  Slave IP, Slave type

           Returns,
                  0 on success and -1 on failure 
        """

        status = FabricObj.execute(
                                "mkdir /opt/IMT",
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )
        logger.info("Created directory /opt/IMT")
        print "Created directory /opt/IMT"

        status = FabricObj.execute(
                                "mkdir /opt/IMT/IMT_Automation",
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                )

        logger.info("Created directory /opt/IMT/IMT_Automation")
        print "Created directory /opt/IMT/IMT_Automation"

        status = FabricObj.execute(
                               "mkdir /opt/IMT/IMT_Automation/Slave",
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                )

        status = FabricObj.execute(
                                "mkdir /opt/IMT/IMT_Automation/Util",
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                )

        self.ftp_client  = FileTransfer(hostname)
        self.ftp_client.push_slave()
        logger.info("Successfully pushed slave agent into the slave host")
        print "Successfully pushed slave agent into the slave host"
        return True

    def log_message(self):
        """
           This logger method logs any message from any function, thread or any ! 
           Method Argument, msg

           Returns,
                  Nothing

        """

        self.File_Handle = open("Generic_Log.log","w+")

        while(True):
            self.logger_condition.acquire()
            while(self.logger_queue.empty()):
                # Lets wait for the logger queue to receive some data.
                self.logger_condition.wait()

            thread_msg = self.logger_queue.get()
            self.File_Handle.write(thread_msg)
            self.logger_condition.release()

        close(self.File_Handle) # Will never get here ! 

    def find_os_start_slave(self,mac,slave_ip):

        p = subprocess.Popen(
                             ['ping', '-c 1',slave_ip],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                            )
        out_stream, err_stream = p.communicate()
        
        logger.info("find os start slave %s"%out_stream)
        print "find os start slave ",out_stream

        pattern = re.compile('ttl=(.+?) ')
        if(re.search('1 received',out_stream)):
           logger.info("%s  found alive"%slave_ip)
           print slave_ip," found alive "
           matched_string  = re.search(pattern,out_stream)
           ttl_value = matched_string.group(1)
           logger.info("This is your TTL value :::  %s"%ttl_value)
           print "This is your TTL value ::: ",ttl_value
           if ( int(ttl_value) > 64 ):
               slave_type = "WINDOWS"
               logger.info("WINDOWS Slave , Hence Keeping it on HOLD ")
               print "INFO","WINDOWS Slave , Hence Keeping it on HOLD "
               return "windows"
           else:
               slave_type = "linux_vmware"
               logger.info("This is a LINUX or VMWARE Machine with ip address %s"%slave_ip)
               print "This is a LINUX or VMWARE Machine with ip address ", slave_ip

        # Keeping fabric object private to each thread as
        # thread share their globals data access.
        FabricObj = Fabric()
        status = FabricObj.connect_host(slave_ip)

        logger.info("Connected to the host %s"%slave_ip)

        print "Connected to the host, ",slave_ip

        unix_variant = self.getLinuxVariant(FabricObj)

     
        logger.info("check if slave agent is running ?")
        print " check if slave agent is running ?" 
        status = self.IsSlaveRunning(FabricObj,unix_variant)
        if(status):
            logger.info("Slave running on the remote host")
            print "Slave running on the remote host " 
            return True
        else:
            logger.info("Slave agent is not running on the remote host %s"%slave_ip)
            print "Slave agent is not running on the remote host ",slave_ip 
            status = self.CheckIfSlaveAgentPresent(FabricObj)
            if ( status != True):
                logger.info("Pushing slave agent into the machine")
                print "Pushing slave agent into the machine "
                self.PushSlaveAgent(FabricObj,unix_variant,slave_ip)
                logger.info("Successfully pushed slave agent into the machine ")
                print "Successfully pushed slave agent into the machine "
        
            firewall_status=self.StopFirewall(FabricObj)
            status = self.StartSlaveAgent(FabricObj)

            print "Status after staring the machine ip ",slave_ip," and status ",status

            if ( status == True):
                logger.info("Started slave successfully in the machine %s"%slave_ip)
                print "Started slave successfully in the machine",slave_ip
                # Generate Logs saying success.
                return 1
            else:
                return -1

    def SlaveOps(self):
        """
           Description,

           Method Arguments,
                  Slave IP 

           Returns,
                  0 on success and -1 on failure 
        """
        # The below lock is declared above the master class.

        # ipmac data structure is used by getipmac_info() thread
        # which will clear after wait for x minutes.
        # Accidental access during the clearing the data structure
        # is meaning less, hence this while ensures that it not that
        # way.

        #while (True):
            #self.ipmac_condition.acquire() 
            #while(self.ipmac_queue.empty()):
            #    self.ipmac_old = {"MAC1":"10.102.29.109"}
            #    print "SlaveOperations: Queue Empty , Lets Wait ! "
            #    print "Producer thread data :::: ",self.ipmac_old
            #    self.ipmac_condition.wait()
            #self.ipmac_old = self.ipmac_queue.get()
            #print "Producer thread data :::: ",self.ipmac_old
            #self.ipmac_condition.release()

            # Steps :
            # Check if slave agent is present in the slave machine ?
            # If present ?
            #    Check if slave agent is running in the remote host ?
            #    If not,
            #        Push slave agent and start slave agent.
            # Do some thing to start the slave agent in the remote host.
            # If running, kill slave.
            # Start slave agent from the /opt/SlaveAgent/ Directory.

        self.ipmac_old = {"MAC1":"10.102.28.89","MAC2":"10.102.28.135","MAC3":"10.102.28.27","MAC4":"10.102.28.191","MAC5":"10.102.28.203"}
        #self.ipmac_old = {"MAC2":"10.102.28.203"}
        thread_list = []
        thread_num = 0
        for mac in self.ipmac_old:
            logger.info("Probing started for the slave %s"%self.ipmac_old[mac])
            print "Probing started for the slave ",self.ipmac_old[mac]
            #thread_list.append(Thread(target=self.find_os_start_slave, args=(mac,self.ipmac_old[mac])))
            #thread_list[-1].start()
            self.find_os_start_slave(mac,self.ipmac_old[mac])
            

#        for thread in thread_list:
 #           thread.join()

        #print "SlaveOps : Waiting for 1 minute "
        #self.UtilObj.WaitForXMinutes(1)

    def handle_slave(self,port_num,slave_ip,mac):

        #FabricObj = Fabric()
        #status = FabricObj.connect_host(slave_ip)
        
        logger.info("Creating socket to connect to the slave %s"%slave_ip)
        print "Creating socket to connect to the slave ",slave_ip
        local_socket = self.UtilObj.SocketObj.CreateSocket(port_num,whoami="master")
        logger.info("Created local socket on the port number,%s"%port_num)        
        print "Created local socket on the port number, ",port_num
        if (local_socket == None):
            logger.info("Socket Creation failure ! ")
            print "Socket Creation failure ! "
            return -1
        
        logger.info("Socket Creation successful ! ")
        print "Socket Creation successful ! "
        logger.info("About to send socket message prepare data to the slave %s"%slave_ip)
        print "About to send socket message \"prepare_data\" to the slave,",slave_ip
        msg = "prepare_data"
        local_socket.connect((slave_ip,40197))
        logger.info("Connected to the Slave Socket %s"%slave_ip)
        print "Connected to the Slave Socket ", slave_ip

        no_of_bytes = local_socket.send(msg)
        print "Have sent, " + str(no_of_bytes) + " bytes to the master "

        while(True):
            #Receiving from client
            logger.info("Waiting for slave response ")
            print "Waiting for slave response "
            data = local_socket.recv(1024)
            print "Received message from the slave ip, ",slave_ip, " MSG : ",data
            if(data == "done"):
                #Call Send Slave Information.
                local_socket.send("done")
                logger.info("Breaking communication from slave ")
                print "Breaking communication from slave "
                break
            elif(data == "no_data"):
                #Self Terminate.
                reply = "prepare_data"
            elif not data:
                local_socket.send("prepare_data")
                self.logger_queue.put(msg)
                continue
            else:
                reply = "prepare_data"
                continue

        self.UtilObj.SocketObj.DestroySocket(local_socket)

        self.ftp_client  = FileTransfer(slave_ip)
        status=self.ftp_client.get_log(mac)

        #status = FabricObj.get_file(mac)

        #FabricObj.quit_connection()

        if ( status ):
             logger.info("Slave log file download complete ! ")
             print "Slave log file download complete ! "
             return 0
        else:
             logger.info("Slave Log file download failure ! ")
             print "Slave Log file download failure ! "
             return -1 

    def StartSlaveAgent(self,FabricObj):

        logger.info("Executing slave agent ")
        print "Executing slave agent "
        status = FabricObj.execute(
                                "(nohup python Slave.py > /dev/null < /dev/null &)&",
                                #"(nohup python Slave.py &)&",
                                path='/opt/IMT/IMT_Automation/Slave/',
                                ignore_err=True,
                                hide_opt=1,
                                out_stream=None,
                                err_stream=None,
                                disconnect=True
                              )
        logger.info("started slave agent ")
        print "started slave agent "
        return status

    def CheckSlaveTargetRunning(self):
        """ 
           Description,
                  This method is meant for checking if the slave machine 
           is up and running.

           Method Arguments,
                  Slave IP / host name.

           Returns,
                  0 on success and -1 on failure 
        """
        while True:
            try:
                self.tlock.acquire()
        #       print " Lock acquired by Check Slave . Check Slave running.\n "
                # code to be executed 
                self.tlock.release()
                #print " Lock released by Check Slave. \n"
                self.logObj.WaitForXMinutes("X")

            except Exception, e:
                print e
                self.tlock.release()

    def ConvertSlaveInfo(self, repopath, jsonpath):
        """
           Description,
                  This method is meant for converting the collected slave information from the repository to json format
                  and sending it to upper layer. The file repository and json repository is assumed to be on the same
                  machine.

           Method Arguments,
                  path of file/repository
                  path of json files

           Returns,
                  None

        """
        while True:
            try:
                self.tlock.acquire()
                if os.path.exists(repopath) and os.path.exists(jsonpath):
                    fileList = os.listdir(repopath)
                    for file in fileList:
                        filepath= repopath + file
                        if os.path.isfile(filepath):
                            if logObj.ConvertInfoToJSON(
                                                        file, 
                                                        filepath, 
                                                        jsonPath
                                                       ) == -1:
                                print "File ", file, " not converted"

                    jsonFiles = os.listdir(jsonpath)
                    for file in jsonFiles:
                        "send the files to upper layer"
                self.tlock.release()
                self.logObj.WaitForXMinutes("X")

            except Exception, e:
                print e
                self.tlock.release()

    def collectSlaveInfo(self):

        thread_list = []
         
        port_num = PORT_NUM

        logger.info("collectSlaveInfo :: Function Start ")
        print "collectSlaveInfo :: Function Start "
        logger.info("Starting to collect slaveinfo -- from collectSlaveInfo function ")
        print "Starting to collect slaveinfo -- from collectSlaveInfo function "
        self.ipmac_old = {"MAC1":"10.102.28.89","MAC2":"10.102.28.135","MAC3":"10.102.28.27","MAC4":"10.102.28.191","MAC5":"10.102.28.203"}
        #self.ipmac_old = {"MAC1":"10.102.28.191","MAC2":"10.102.28.135"}
        #self.ipmac_old = {"MAC2":"10.102.29.12"}
        #self.ipmac_old = {"MAC2":"10.102.28.203"}
        #while(True):
        print "Have got these many machines, ",self.ipmac_old
        for mac in self.ipmac_old:
            HandleClient = Thread(target=self.handle_slave, args=(port_num,self.ipmac_old[mac],mac))
            logger.info("Monitor Log Server Started")
            print " Monitor Log Server Started"
            HandleClient.start()
            thread_list.append(HandleClient)
            port_num = port_num + 1

        for thread in thread_list:
            thread.join()

        port_num = PORT_NUM

    def get_IPMAC_info(self):
        print "Inside function, get_IPMAC_info"
        # The below constant needs to be moved to constants file.
        #subnet_list = ["10.102.29.1/24", "10.102.28.1/24"]
        subnet_list = ["10.102.29.1/24" ]
        #global self.ipmac
        for subnet in subnet_list:
            # Will update more hosts & their macs if subnets are added.
            print "Calling method the Gather_IPMAC_Informaton, in util class"
            self.ipmac =  self.Gather_IPMAC_Informaton(subnet)
        self.ipmac_condition.acquire()
        while(self.ipmac_queue.full()):
            print "get_IPMAC_info: Queue Full ! Lets wait ! "
        self.ipmac_queue.put(self.ipmac)
        self.ipmac_condition.notify()
        self.ipmac_condition.release()
        # Wait for 5 minutes.
        print "get_IPMAC_info: Lets sleep for 300 seconds "
        self.UtilObj.WaitForXMinutes(5)
        # Emptying the entire data strucutre and refilling it again in 
        # the next thread run.

def logStart(path, filename):
    """
    Create a logger that accepts messaged of info or higher and print them to a file
    
    Args:
        path - str - the path to where the file should be created
        filename - str - the name of the file to be created
    Returns:
    """
    #Make Logs Directory
    if( not os.path.exists(path)):
        os.makedirs(path) 

    #Initialize the results logger 
    #formatter = logging.Formatter("%(asctime)s; %(levelname)s; %(message)s \n")
    formatter = logging.Formatter("%(asctime)s : %(message)s \n")
    infoFileHandler = logging.FileHandler(filename, mode='a')
    infoFileHandler.setLevel(logging.INFO)
    infoFileHandler.setFormatter(formatter)
    logger.addHandler(infoFileHandler)


if  __name__ == "__main__":


    mainObj = Master()

    #mainObj.logger_queue.put("INFO","Started Logger Thread Successfully !")

    #Logger_Thread = Thread(target=mainObj.log_message, args=())
    #Logger_Thread.daemon = True
    #print " Monitor Log Server Started"
    #Logger_Thread.start()

    filename = 'Report_log'
        #Framing the output log file name with current timestamp
    logfile='%s-%s.log'%(filename,datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    log_path = os.getcwd()
    resultsHandler = logStart(log_path, logfile)
    logger.info("outputPath is %s"%log_path)

    # starting the Initialize IMT processes
    mainObj.InitializeMaster()

    #Logger_Thread.join() # Will never get here 
    
    print "---------------Exiting --------------"

