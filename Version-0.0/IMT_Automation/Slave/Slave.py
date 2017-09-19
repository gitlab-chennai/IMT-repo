#!/usr/bin/python
    
import re
import os
import sys
import subprocess

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Util.Util import Util

Cpu_Info = {}
listOf_Cpu_Info = []
Nic_info = {}
RamInfolist = []
RamInfo_perslot = {}
hard_disk_list = []
hard_disk_info = {}

class Slave(Util):

    def __init__(self):
        ''' 
           Description
                   Constructor method which will be called during the
                   creation of the object. Will take in all possible
                   class attributes for performing object specific
                   intialization.
    
           Method Arguments,
                   TBD
    
           Returns,
                   Returns None.
        '''    
        self.UtilObj = Util()
        self.SocketObj = self.UtilObj.SocketObj

    def filewrite_for_CpuInfo(self):
        with open('abc.txt', 'w') as f:
            subprocess.Popen(['cat', '/proc/cpuinfo'], stdout = f).wait()

    def fileread_From_CpuInfo(self):
        with open('abc.txt', 'r') as f:
            data = f.readlines()
            for line in data:
                #print line
                line = line.strip()
                print line
                #list.append(line)
                words = line.split(":")
                #key = line[0:9]
                #value = line[9:]
                listOf_Cpu_Info.append(words)

    def Cpu_Info_Dictionary(self):
        counter = 0
        for item in  listOf_Cpu_Info :

            for keys in item:
                if 'processor' in keys:
                    keys = keys + "-->" + str(counter)
                    counter = counter + 1

                value = item[1]
                Cpu_Info.update({keys:value})
                break

    def fileWrite_ForNicInfo(self):
        with open('abc.txt', 'w') as f:
            subprocess.Popen(['esxcfg-nics','-l'], stdout = f).wait()

    def fileRead_ForNicInfo(self):
        with open('abc.txt', 'r') as f:
             data = f.readlines()


        for line in data:
            if 'Name' in line:
                line = line.strip()
                key = line[0:4]
                value = line[4:]
                Nic_info.update({key:value})
                #print "\n"
                #line = line.split()
                #print line,'\n'
            else:
                line = line .strip()
                #pattern = re.compile(r'(.+?)\s+')

                #matchobj = re.search('(.+?)\s+',str)
                key =  line[0:6]
                value = line [6:]
                #print value
                Nic_info.update({key:value})

    
    def Nic_information(self,arg):
        if arg == 'vmnic0':
            print "\t\tListing the information of nic card 0\n"
        if arg == 'vmnic1':
            print "\t\tListing the information of nic card 1\n"

    def finalCall_ForNicInformation(self):
        fileWrite_ForNicInfo()
        fileRead_ForNicInfo()

        for key,value in Nic_info.iteritems():
            print "\n"
            Nic_information(key)
            print '\t\t{0}{1}'.format(key ,value)
            print "\n"

    def fileWrite_RamInfo(self):
        with open('abc.txt', 'w') as f:
            subprocess.Popen(['smbiosDump'], stdout = f).wait()

    def fileRead_RamInfo(self):
        with open('abc.txt', 'r') as f:
            data = f.readlines()
            for line in data:
                line = line.strip()
                print line
                words = line.split(":")
                RamInfolist.append(words)

    def RamDict1(self):
        for item in RamInfolist[39:46]:
            #print lists


            key = item[0]
            #if key == 'Feactures':

            value = item[1]
            RamInfo_perslot.update({key : value})

    def RamDict2(self):
        str = RamInfolist[46] + RamInfolist[47] + RamInfolist[48]
        key = str[0]
        value = str[1:]
        RamInfo_perslot.update({key : value})

    def finalcall_ForRamInfo(self):
        fileWriteRam_Info()
        fileReadRam_Info()
        RamDict1()
        RamDict2()

        for key,value in  RamInfo_perslot.iteritems():
            print "\t\t\t{0:30}{1:30}".format(key,value)

    def fileWriteFor_Hard_disk(self):
        with open('abc.txt', 'w') as f:
            subprocess.Popen(['fdisk', '-l'], stdout = f).wait()

    def fileRead_For_Hard_disk(self):
        with open('abc.txt', 'r') as f:
            data = f.readlines()
            for line in data[0:9]:
                line = line.strip()
                print line
                words = line.split(':')
                hard_disk_list.append(words)

            for line in data[9:]:
                line = line.strip()
                print line
                words = line.split()
                hard_disk_list.append(words)


    def general_hard_disk_information(self):
        hard_disk_list0 = hard_disk_list[0]
        hard_disk_list2 = hard_disk_list[2]
        hard_disk_list3 = hard_disk_list[3]
        hard_disk_list4 = hard_disk_list[4]
        hard_disk_list5 = hard_disk_list[5]
        hard_disk_list6 = hard_disk_list[6]
        hard_disk_list8 = hard_disk_list[8]
        print "\n"
        print "\t\t", hard_disk_list0[0]
        print "\t\t", hard_disk_list2[0] + hard_disk_list2[1]
        print "\t\t", hard_disk_list3[0] + hard_disk_list3[1]
        print "\t\t", hard_disk_list4[0]
        print "\t\t", hard_disk_list5[0]
        print "\t\t", hard_disk_list6[0]
        print "\n\n"
        print "\t\t", hard_disk_list8[0]


    def hard_DiskInfo_dictionary(self):
        for lists in  hard_disk_list[9:]:

            key = lists.pop(0)
            value = ' '
            for item in lists:
                value = value  + item + "\t"
                value = '{0:<21}'.format(value)

            hard_disk_info.update({key:value})

    def finalcall_hard_diskInformation(self):
        self.fileWriteFor_Hard_disk()
        self.fileRead_For_Hard_disk()
        self.general_hard_disk_information()
        self.hard_DiskInfo_dictionary()

        for key in sorted(hard_disk_info.keys()):
            print  '\t\t{0:<5} {1:<19}'.format(key,hard_disk_info[key])

    def finalcallCpuInfo(self):
        self.filewrite_for_CpuInfo()
        self.fileread_From_CpuInfo()
        self.Cpu_Info_Dictionary()
        for key,value in Cpu_Info.iteritems():
            print "\t\t\t\t\t\t{0:20}{1:20}".format(key,value)
            print "\n"

    def CreateSlaveLogs(self):
    
        '''
          Description,
                  This method is meant for creating a folder in the log server
          repository for the slave.
    
          Method Arguments,
                  Log Server IP , log server repository path.
    
          Returns,
                  0 on success and -1 on failure.
        '''
        pass

    def CollectSlaveInformation(self):

        '''
          Description,
                  This method is meant for collecting information from the
          slave machine. 
    
          Method Arguments,
                  None
    
          Returns,
                  Dictionary containing the slave information
        '''
        pass

    def windows_client(self):

        """ This function will collect the following system information from the Windows
        Client machine:
        1. OS information
        2. Processor information
        3. Memory information
        4. Network information
        5. PCI/PCIe information
        """

        info = ['Host Name', 'OS Name', 'OS Manufacturer', 'OS Configuration', 'OS Build Type',
            'Registered Owner', 'Registered Organization', 'Product ID', 'Original Install Date',
            'System Boot Time', 'System Directory', 'Boot Device', 'System Locale', 'Input Locale',
            'Time Zone', 'Domain', 'Logon Server', 'Total Physical Memory', 'Available Physical Memory',
            'Virtual Memory: Max Size', 'Virtual Memory: Available', 'Virtual Memory: In Use',
            'Page File Location(s)', 'System Manufacturer', 'System Model', 'System Type', 'BIOS Version',
            'Windows Directory']

        output = subprocess.check_output("systeminfo", shell=True)
        num_info = len(info)
        OS_information = {}
        for row in output.split('\n'):
	    for i in range(num_info):
		    if info[i] in row:
			    key,value = row.split(info[i])
			    value = value.strip(':')
			    OS_information[info[i]] = value.strip()

        op = subprocess.check_output("wmic nic where PhysicalAdapter=TRUE get name", shell=True)
        a = op.split('\n')
        NIC = []
        for i in range(1,len(a)-2):
            NIC.append(a[i].strip())
            OS_information['Network Card(s)'] = NIC

        op = subprocess.check_output("wmic cpu get Name", shell=True)
        cpu = op.split('\n')
        Processor = cpu[1].strip()
        OS_information['Processor(s)'] = Processor

    def vmware_client(self):
	
        '''
        This function will collect the following information from the Linux client machine
        1. PCI/PCIe information
        2. Processor information
        3. Network cards information
        4. IP information
        5. OS information
        '''

        '''PCI/PCIe information'''

        info = {}
        p1 = subprocess.Popen(["lspci"], stdout=subprocess.PIPE)
        output = str(p1.communicate()[0])
        if sys.version_info > (3,0):
            outone = (output[2:-3].strip("\n")).split("\\n")
            info['No_of_PCI_Devices'] = str(len(outone))
        else:
            outtwo = (output.strip("\n")).split("\n")
            info['No_of_PCI_Devices'] = str(len(outtwo))

        '''Processor information'''
    
        p1 = subprocess.Popen("vim-cmd hostsvc/hosthardware |grep -i 'description =' |awk 'NR'==1|awk -F '=' '{print $2}'", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = str(p1.communicate()[0])
        processor_info3 =output.strip('b')
        processor_info2 =processor_info3.strip("'")
        processor_info1 =processor_info2.strip('\\n')
        processor_info  =processor_info1.replace(','," ")
        
        p1 = subprocess.Popen("vim-cmd hostsvc/hosthardware |grep -i numcpucores |awk 'NR'==1|awk -F '=' '{print $2}'", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = str(p1.communicate()[0])
        no_of_cores1=output.split(',')
        no_of_cores2=no_of_cores1[0].strip('b')
        no_of_cores=no_of_cores2.strip('\'')
        abt_processor = processor_info[2:-4]+"_"+ no_of_cores
        info['Processor_no_of_cores'] = abt_processor

        '''Network Cards information'''
        p1 = subprocess.Popen(
            ["lspci | grep 'Network controller'"],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
            )
        nic = str(p1.communicate()[0])
        if sys.version_info > (3,0):
            items = (nic[2:-3].strip("\n")).split("\\n")
        else:
            items = (nic.strip("\n")).split("\n")
        new_items = [item for item in items if item != ""]
        nic_string = ((new_items[0].split(":")[3]).split("[")[0]).strip(" ")
        nic = nic_string.replace(" ","_")
        info['NICs'] =  nic+"_"+str(len(new_items)) 

        '''IP information'''
        p1 = subprocess.Popen(
            ["esxcli network ip interface ipv4 get"],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
            )
        ip_address = str(p1.communicate()[0])
        ip_address = ip_address.strip("\n")
        if sys.version_info > (3,0):
            ver35 = (ip_address.split("\\n")[2]).split("  ")[1]
            info['IP'] = str(ver35)
        else:
            ver27 = (ip_address.split("\n")[2]).split("  ")[1]
            info['IP'] = str(ver27)

        '''OS information'''
        p1=subprocess.Popen(
            ["vmware -v"],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
            )
        os_ver = str(p1.communicate()[0])
        os_ver = os_ver.strip("\n")
        if sys.version_info > (3,0):
            info['OS_Version'] = (os_ver[2:-3])
        else:
            info['OS_Version'] = (os_ver)

        return info
    def linux_client(self):

        '''
        This function will collect the following information from the Linux client machine
        1. OS information
        2. Procesor information
        3. Memory information
        4. Network information
        5. PCI/PCIe information
        '''

        '''PCI/PCIe information'''

        info = {}
        p1 = subprocess.Popen(["lspci"], stdout=subprocess.PIPE)
        output = p1.communicate()[0]
        output = output.strip('\n')

        nol = 0
        for line in output.split("\n"): 
            nol = nol + 1

        info['No_of_PCI_Devices'] = str(nol)

        '''Processor information'''
        p1 = subprocess.Popen(
                              ["dmidecode --type processor | grep 'Version' |  awk 'NR == 1' | awk -F':' '{print $2}'"], 
                              shell=True, 
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE
                             )
        output = p1.communicate()[0]
        processor_info = output.strip('\n')
        processor_info = processor_info[1:]
        processor_info = processor_info.replace(" ","_")

        p1 = subprocess.Popen(["nproc --all"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p1.communicate()[0]
        no_of_cores = output.strip('\n')

        abt_processor = processor_info + "_" + no_of_cores
        info['Processor_no_of_cores'] = abt_processor

        '''Network Cards information'''
        p1 = subprocess.Popen(
                              ["lspci | grep 'Ethernet controller'"],
                              shell=True,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE
                             )
        nic = p1.communicate()[0]

        items = nic.split("\n")
        new_items = [item for item in items if item != ""]
        nic_string = new_items[0].split(":")[2]
        nic_string = nic_string[1:]
        nic = nic_string.replace(" ","_")
        info['NICs'] =  nic+"_"+str(len(new_items)) 

        '''IP information'''
        p1 = subprocess.Popen(
             ["cat /etc/*-release | grep -w NAME"],
             shell=True,
             stdin=subprocess.PIPE,
             stdout=subprocess.PIPE
             )
        name=((p1.communicate()[0]).split("\n")[0]).split("=")[1]
        if (name[1:-1]=="SLES"):
	    p3 = subprocess.Popen(
	            ["hostname -i | awk '{print $1}'"],
	            shell=True,
	            stdin=subprocess.PIPE,
	            stdout=subprocess.PIPE
        	    )
            ip_address = p3.communicate()[0]
        else:
            p2 = subprocess.Popen(
           	 ["hostname -I | awk '{print $1}'"],
	        shell=True,
        	stdin=subprocess.PIPE,
	        stdout=subprocess.PIPE
        	)
	    ip_address = p2.communicate()[0]        

        info['IP'] = str(ip_address)

        '''OS information'''
        p1=subprocess.Popen(
                             ["cat /etc/*-release | grep -w NAME"],
                             shell=True,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE
                             )
        p2=subprocess.Popen(
                            ["cat /etc/*-release | grep -w VERSION"],
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE
                            )
        name=((p1.communicate()[0]).split("\n")[0]).split("=")[1]
        version=(((p2.communicate()[0]).split("\n")[0]).split("=")[1]).split()[0]
        if (name[1:-1]=="SLES"):
	    opsys=str(name[1:-1])+" "+str(version[:])
        else:
	    opsys=str(name[1:-1])+" "+str(version[1:])

        info['OS_Version'] = opsys

        return info

    def ValidateSlaveInformation(self):
        '''
          Description,
                  This method is meant for validating all information 
          collected from the slave before copying the information 
          to the log server repository.
    
          Method Arguments,
                  A dictionary of the slave information
    
          Returns,
                  0 on success and -1 on failure.
        '''
        pass

    def PostSlaveInformation(self):
        '''
          Description,
                 This method is meant for copying the slave log file in the log 
          server repository.
    
          Method Arguments,
                 Log Server IP, Slave Repo path, slave log file
    
          Returns,
                 0 on success and -1 on failure.
        '''
        pass

    def PrepareSlavelog(self):
        '''
          Description,
                 This method is meant for preparing a detailed report
          of all the information collected by the method 
          "CollectSlaveInformation".
    
          Method Arguments,
                 A dictionary containing the slave information.
    
          Returns,
                 0 on success and -1 on failure.
        '''
        pass

    def handle_incoming_socket(self,master_socket_conn,addr):
        print "Created Log Handle"
        while True:
            print "this is master socket address ",master_socket_conn
            data = master_socket_conn.recv(1024)
            print "Received data from the master ",data
            if(data == "prepare_data"):
                #Call Send Slave Information.
                reply = "done"
                if (os.uname()[0] == "Linux"):
                    log_handle = open("/opt/IMT/log.csv","w+")
                    info = SlaveObj.linux_client()
                    header = ",".join( info.keys())
                    data = ",".join( info.values())
                    log_handle.write(header)
                    log_handle.write("\n")
                    log_handle.write(data)
                    log_handle.write("\n")
                    log_handle.close()
                    no_of_bytes = master_socket_conn.send(reply)
                    continue
                elif ("VM" in os.uname()[0]):
                    log_handle = open("/opt/IMT/log.csv","w+")
                    info = SlaveObj.vmware_client()
                    header = ",".join( info.keys())
                    data = ",".join( info.values())
                    log_handle.write(header)
                    log_handle.write("\n")
                    log_handle.write(data)
                    log_handle.write("\n")
                    log_handle.close()
                    no_of_bytes = master_socket_conn.send(reply)
                    continue
                else:
                    print "Windows "
            elif(data == "kill_slave"):
                # You are Terminated ;)
                reply = "done"
                no_of_bytes = master_socket_conn.send(reply)
                break
            elif not data:
                break # Broken Pipe
            else:
                continue
                # Lets do a retry.
            print "no of bytes sent to the master ",no_of_bytes
        master_socket_conn.close()

if  __name__ == "__main__":

    PORT_NUM = 40197

    p1 = subprocess.Popen(
                              ["lsof | grep -i 40197"],
                              shell=True,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE
                         )

    running_instance = p1.communicate()[0]
    if(running_instance != ""):
        if(os.uname()[0] == "VMkernel"):
            pid = running_instance.split()[0]
        else:
            pid = running_instance.split()[1]
            print "-------------------------------the os is linux-----------------------"

        kill_process = "kill -9 " + pid
        os.system(kill_process)

    if ("VM" in os.uname()[0]):
        os.system("esxcli network firewall unload")

    SlaveObj = Slave()

    local_socket = SlaveObj.SocketObj.CreateSocket(PORT_NUM)

    if (local_socket == None):
        print("Unable to create the local socket")
        sys.exit()

    while(1):
        master_socket,addr = local_socket.accept()
        print "Connected to master "
	SlaveObj.handle_incoming_socket(master_socket,addr)
