import re
import os
import sys
import subprocess
import logging
import datetime
import time

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Util.Fabric import Fabric
from Util.Util import Util
from Util.Fabric import FileTransfer
from Util.Fabric import FileTransferUb
from Util import Find_IP_Nmap

logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG)

PORT_NUM = 50005
ipmac_dic={}
ipmac_fail = []
ipmac_work_win = []
ipmac_work_livm = []
ip_not_work={}

exception_li=["10.102.29.120"]

class Master(Util):
    
    def __init__(self):
        self.UtilObj = Util()
    
    def InitializeMaster(self):
        while(True):
            #self.clone_IMT_Repo()
            t=time.time()
            print ('starting time is:',t)
            self.SlaveType()
            self.SlaveOps()
            time.sleep(5)
            self.collectSlaveInfo()
            print ('Ending time is:',time.time())
            print ('Difference is:',time.time()-t)
            print ("ipmac_fail was:",ipmac_fail)
            print ("-----------------------Program Ended----------------------..........................Thank You...........................")
            self.UtilObj.WaitForXMinutes(1)
    
    def clone_IMT_Repo(self):
        print ("Cloning IMT Repo locally ...")
        os.system("git clone git@gitlab-chennai:IMT/IMT.git /opt/IMT")
    
    def SlaveType(self):
        logger.info("Finding Slave type <Windows/Linux/VMware> IP's using nmap")
        print ("Finding Slave type <Windows/Linux/VMware> IP's using nmap")
        Run_nmap = Find_IP_Nmap.nmap_fun()
        ipmac_fail.extend(Find_IP_Nmap.ipmac_fail)
        ipmac_work_win.extend(Find_IP_Nmap.ipmac_work_win)
        ipmac_work_livm.extend(Find_IP_Nmap.ipmac_work_livm)
        
        #os_list = ['Windows','windows','Linux','linux','VMware','Host seems down']
        #for mac in ipmac_all:
         #   p = subprocess.Popen(['nmap', '-F','-O','--osscan-guess',mac],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
          #  out_data = str( p.communicate() )
           # out_type = out_data.split("TCP/IP fingerprint:")[0]
            #slave_type = "Not Working or Powered Off"
            #for os_type in os_list:
            #	if(re.search(os_type, out_type)):
             #       slave_type = os_type
            #logger.info("%s Slave OS is %s "%(mac,slave_type))
            #print ("%s Slave OS is %s "%(mac,slave_type))
            #if (slave_type != "Not Working or Powered Off"):
            #	if (slave_type != 'Host seems down'):
            #		if ((slave_type == "Windows") or (slave_type == "windows")):
             #  			ipmac_work_win.append(mac)
              #          else:
               #                 ipmac_work_livm.append(mac)
                #else:
		#	ipmac_fail.append(mac)
            #else:
             #   ipmac_fail.append(mac)
    
    def SlaveOps(self):
        #print ("slaveOps ip's are:",ipmac_work_livm)
        
        print ("List before remove ip:",ipmac_work_livm)
        for i in ipmac_work_livm:
             if i in exception_li:
                        ipmac_work_livm.remove(i)
        print ("List after remove ip:",ipmac_work_livm)

        for mac in ipmac_work_livm:
            try:
                logger.info("Probing started for the slave %s"%mac)
                print ("Probing started for the slave %s"%mac)
                check = self.find_os_start_slave(mac)
                print ("check is %s"%check)
                if (check == "invalid"):
                    ipmac_work_livm.remove(mac)
                else:
                    print ("Login Completed with %s"%check)
                    ipmac_dic[mac]=check
                    #return check 
                    #self.collectSlaveInfo(user)
            except:
                logger.info("Exception Occurred during file_copy/search/process_running/firewall_disable : Exiting from the current Execution of %s"%mac)
                print ("Exception Occurred during file_copy/search/process_running/firewall_disable : Exiting from the current Execution of %s"%mac)
        print (ipmac_dic)
    
    def find_os_start_slave(self,slave_ip):
        FabricObj = Fabric()
        logonuser=""
        logonuser = FabricObj.connect_host(slave_ip)
        #logger.info("Connected to the host %s with %s"%slave_ip,logonuser)
        print ("Connected to the host %s with %s"%(slave_ip,logonuser))
        if ( logonuser != "invalid"):
            unix_variant = self.getLinuxVariant(FabricObj)
            logger.info("Check Whether Slave agent is running or not")
            print ("Check Whether Slave agent is running or not")
            status = self.IsSlaveRunning(FabricObj,unix_variant)
        else:
            print ("Slave Agent can't be Started : Invalid User")
        if(status):
            logger.info("Slave Agent is already Running on the Remote Host %s"%slave_ip)
            print ("Slave Agent is already Running on the Remote Host %s"%slave_ip)
        else:
            logger.info("Slave Agent is not Running on the Remote Host %s"%slave_ip)
            print ("Slave Agent is not Running on the remote Host %s"%slave_ip )
            if ((logonuser == "ubuntu") or (logonuser=="sesqa")):
                status = self.CheckIfSlaveAgentPresentUb(FabricObj,logonuser)
                if ( status != True):
                    logger.info("Pushing Slave Agent into the Machine")
                    print ("Pushing ubuntu Slave Agent into the Machine ")
                    self.PushSlaveAgentUb(FabricObj,unix_variant,slave_ip,logonuser)
                    logger.info("Successfully Pushed Slave Agent into the Machine ")
                    print ("Successfully Pushed Slave Agent into the Machine")
                    firewall_status=self.StopFirewall(FabricObj,slave_ip,logonuser)
                    status = self.StartSlaveAgentUb(FabricObj,logonuser)
            else:
                status = self.CheckIfSlaveAgentPresent(FabricObj)
                if ( status != True):
                    logger.info("Pushing Slave Agent into the Machine")
                    print ("Pushing Slave Agent into the Machine")
                    self.PushSlaveAgent(FabricObj,unix_variant,slave_ip)
                    logger.info("Successfully Pushed Slave Agent into the Machine")
                    print ("Successfully Pushed Slave Agent into the Machine")   
                    firewall_status=self.StopFirewall(FabricObj,slave_ip,logonuser)
                    status = self.StartSlaveAgent(FabricObj)
            print ("Status after Staring the Machine IP %s is %s"%(slave_ip,status))
            if ( status == True):
                logger.info("Started Slave Successfully in the Machine %s"%slave_ip)
                print ("Started Slave Successfully in the Machine %s"%slave_ip)
        return (logonuser)
    
    def getLinuxVariant(self,FabricObj):
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
    
    def CheckIfSlaveAgentPresent(self,FabricObj):
        status = FabricObj.execute(
                                "ls /opt | grep \"^IMT$\"",
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
    
    def CheckIfSlaveAgentPresentUb(self,FabricObj,user):
        status = FabricObj.execute(
                                "ls /home/%s | grep \"^IMT$\""%(user),
                                path='.',
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )
        if (re.search('IMT',status)):
            print "IMT slave agent was present"
            return True
        else:
            print "IMT slave agent was not present"
            return False
    
    def PushSlaveAgent(self,FabricObj,unix_variant,hostname):
        status = FabricObj.execute(
                                "mkdir /opt/IMT",
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )
        logger.info("Created directory /opt/IMT")
        print ("Created directory /opt/IMT")
        status = FabricObj.execute(
                                "mkdir /opt/IMT/IMT_Automation",
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                )
        logger.info("Created directory /opt/IMT/IMT_Automation")
        print ("Created directory /opt/IMT/IMT_Automation")
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
        logger.info("Successfully Pushed Slave Agent into the Slave Host")
        print ("Successfully Pushed Slave Agent into the Slave Host")
        return True
    
    def PushSlaveAgentUb(self,FabricObj,unix_variant,hostname,user):
        status = FabricObj.execute(
                                "mkdir /home/%s/IMT"%(user),
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                disconnect=False
                              )
        logger.info("Created directory /home/%s/IMT"%(user))
        print ("Created directory /home/%s/IMT"%(user))
        status = FabricObj.execute(
                                "mkdir /home/%s/IMT/IMT_Automation"%(user),
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                )
        logger.info("Created directory /home/%s/IMT/IMT_Automation"%(user))
        print ("Created directory /home/%s/IMT/IMT_Automation"%(user))
        status = FabricObj.execute(
                               "mkdir /home/%s/IMT/IMT_Automation/Slave"%(user),
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                )
        status = FabricObj.execute(
                                "mkdir /home/%s/IMT/IMT_Automation/Util"%(user),
                                ignore_err=True,
                                hide_opt=None,
                                out_stream=None,
                                err_stream=None,
                                )
        self.ftp_client  = FileTransferUb(hostname,user)
        self.ftp_client.push_slave(user)
        logger.info("Successfully Pushed Slave Agent into the Slave Host")
        print ("Successfully Pushed Slave Agent into the Slave Host")
        return True
    
    def StopFirewall(self,FabricObj,slave_ip,user):
        vm_check = FabricObj.execute("vmware -v",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
        vm_status = re.search('VMware',vm_check)
        if(vm_status == None): 
            fire_status = FabricObj.execute("cat /etc/issue",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
            if(re.search('SUSE',fire_status)):
                fire_status = FabricObj.execute("rcSuSEfirewall2 stop",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                logger.info("Firewall Disabled for this SUSE Machine")
                print ("Firewall Disabled for this SUSE Machine")
            elif(re.search('Ubuntu',fire_status)):
                fire_status = FabricObj.firewal(slave_ip,user)
                logger.info("Firewall Disabled for this Ubuntu Machine")
                print ("Firewall Disabled for this Ubuntu Machine")
            else:
		try:
                	fire_status = FabricObj.execute("systemctl stop firewalld",path='.',ignore_err=False,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                except:
			#FabricObj.execute("cd")
			fire_status = FabricObj.execute("service iptables stop",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
		logger.info("Firewall Disabled for this RHEL/CentOs Machine")
                print ("Firewall Disabled for this RHEL/CentOs Machine")
        else:
            FabricObj.execute("esxcli network firewall unload")
            logger.info("Firewall Disabled for this VMware Machine")
            print ("Firewall Disabled for this VMware Machine")
    
    def StartSlaveAgent(self,FabricObj):
        logger.info("Executing Slave Agent")
        print ("Executing slave agent")
        status = FabricObj.execute(
                                "(nohup python Slave.py > /dev/null < /dev/null &)&",
                                path='/opt/IMT/IMT_Automation/Slave/',
                                ignore_err=True,
                                hide_opt=1,
                                out_stream=None,
                                err_stream=None,
                                disconnect=True
                              )
        logger.info("Started Slave Agent")
        print ("Started Slave Agent")
        return status
    
    def StartSlaveAgentUb(self,FabricObj,user):
        logger.info("Executing Slave Agent")
        print ("Executing Slave Agent")
        status = FabricObj.execute(
                                "(nohup python Slave.py > /dev/null < /dev/null &)&",
                                path='/home/%s/IMT/IMT_Automation/Slave/'%(user),
                                ignore_err=True,
                                hide_opt=1,
                                out_stream=None,
                                err_stream=None,
                                disconnect=True
                              )
        logger.info("Started Slave Agent")
        print ("Started Slave Agent")
        return status
    
    def collectSlaveInfo(self):
        port_num = PORT_NUM
        logger.info("collectSlaveInfo :: Function Started")
        print ("collectSlaveInfo :: Function Started")
        print ("Have got these many Machines %s"%ipmac_work_livm)
        try:
            #for mac in ipmac_work_livm:
            for mac in ipmac_dic:
                try:
                    logger.info("Monitor Log Server Started for Master-Slave Communication %s and user is %s"%(mac,ipmac_dic[mac]))
                    print ("Monitor Log Server Started for Master-Slave Communication %s and user is %s"%(mac,ipmac_dic[mac]))
                    self.handle_slave(port_num,mac,ipmac_dic[mac])
                except:
                    logger.info("Exception Occurred during Master-Slave Communication : Exiting from the current Execution of %s"%mac)
                    print ("Exception Occurred during Master-Slave Communication : Exiting from the current Execution of %s"%mac)
                port_num = port_num + 1
        except:
            logger.info("Exception Occurred during Consolidated Log File Generation : Exiting from the current Execution of %s"%mac)
            print ("Exception Occurred during Consolidated Log File Generation : Exiting from the current Execution of %s"%mac)
        self.consolidateLogGenerate()
        port_num = PORT_NUM
    
    def handle_slave(self,port_num,slave_ip,user): 
        logger.info("Creating socket to connect to the Slave %s"%slave_ip)
        print ("Creating socket to connect to the Slave %s"%slave_ip)
        local_socket = self.UtilObj.SocketObj.CreateSocket(port_num,whoami="master")
        logger.info("Created local socket on the port number,%s"%port_num)        
        print ("Created local socket on the port number %s"%port_num)
        if (local_socket == None):
            logger.info("Socket Creation Failure")
            print ("Socket Creation Failure")
            return -1
        else:
            logger.info("Socket Creation Successful")
            print ("Socket Creation Successful")
            logger.info("About to send socket message : prepare_%s to the Slave %s"%(user,slave_ip))
            print ("About to send socket message : \"prepare_%s\" to the Slave %s"%(user,slave_ip))
            msg = "prepare_"+user
            print ("message is:",msg)
            local_socket.connect((slave_ip,40197))
            logger.info("Connected to the Slave Socket %s"%slave_ip)
            print ("Connected to the Slave Socket %s"%slave_ip)
            no_of_bytes = local_socket.send(msg)
            print ("Have had sent " + str(no_of_bytes) + " bytes to the Master")
            while(True):
                logger.info("Waiting for Slave Response")
                print ("Waiting for Slave Response")
                data = local_socket.recv(1024)
                logger.info("Received Message from Slave IP")
                print ("Received message from the Slave IP %s and the Message is : %s"%(slave_ip,data))
                slave_msg = "windows_root_ubuntu"
                if(re.search(data,slave_msg)):
                    local_socket.send("done")
                    logger.info("Breaking Communication from Slave %s"%slave_ip)
                    print ("Breaking Communication from Slave %s"%slave_ip)
                    break
                elif not data:
                    local_socket.send("prepare_"+user)
                    continue
                else:
                    reply = "prepare_"+user
                    continue
            if(re.search(data,"ubuntu")):
                self.ftp_client = FileTransferUb(slave_ip,user)
                status = self.ftp_client.get_log(slave_ip,user)
            else:
                self.ftp_client = FileTransfer(slave_ip)
                status = self.ftp_client.get_log(slave_ip)
            self.UtilObj.SocketObj.DestroySocket(local_socket)
            if ( status ):
                logger.info("____________________------------------------Slave Log File Download Completed-------------------------____________________")
                print("____________________------------------------Slave Log File Download Completed-------------------------____________________")
                return 0
            else:
                logger.info("____________________------------------------Slave Log File Download Failed-------------------------____________________")
                print ("____________________------------------------Slave Log File Download Failed-------------------------____________________")
                return -1
    
    def consolidateLogGenerate(self):
        path = "/opt/repo"
        list_dir = []
        list_dir = os.listdir(path)
        header1 = ""
        header = ["IP","No_of_PCI_Devices","NICs","Ram_size","OS_Version","Processor_no_of_cores","Remarks"]
        for i in header:
            header1 = header1 + "," + i
        header1 = header1[1:]
        filename = "Consolidated_Log_File_Report"
        logfile = '%s-%s.csv'%(filename,datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        path1 = "/opt/"
        f2 = open("%s%s"%(path1,logfile),"w+")
        f2.write(header1)
        f2.write("\n")
        for file in list_dir:
            print "name of the file is ",file
            if file.endswith(".csv"):
                print "opened the file",file
                f = open(path+"/"+file)
                lines = f.readlines()
                f2.write(lines[1])
                f.close()
                #os.system("rm -rf %s/%s"%(path,file))
        #os.system("rm -rf %s/*"%("/opt/repo"))
        os.system("rm -rf /opt/repo/*")
	time.sleep(2)
        #print ("Not Working IP Mac's are : "+str(ipmac_fail))
        for mac in ipmac_fail:
            footer1 = ""
            footer = [mac,"N/A","N/A","N/A","N/A","N/A","Unable to login with credentials"]
            for j in footer:
                footer1 = footer1 + "," + j
            footer1 = footer1[1:]
            f2.write(footer1)
            f2.write("\n")
        logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Successfully Generated the Consolidated Slave Log Report!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Successfully Generated the Consolidated Slave Log Report!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        f2.close()
    
def logStart(path, filename):
    if( not os.path.exists(path)):
        os.makedirs(path) 
    formatter = logging.Formatter("%(asctime)s : %(message)s \n")
    infoFileHandler = logging.FileHandler(filename, mode='a')
    infoFileHandler.setLevel(logging.INFO)
    infoFileHandler.setFormatter(formatter)
    logger.addHandler(infoFileHandler)

if  __name__ == "__main__":
    print ("-------------------Program Started------------------......................Welcome World.......................")
    filename = 'Log_Report'
    logfile='%s-%s.log'%(filename,datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    log_path = os.getcwd()
    resultsHandler = logStart(log_path, logfile)
    logger.info("Log File Report Started and Path Location is %s"%log_path)
    print ("Log File Report Started and Path Location is %s"%log_path)
    mainObj = Master()
    #t=time.time()
    #print ('starting time is:',t)
    mainObj.InitializeMaster()
    #print ('Ending time is:',time.time()-t)
