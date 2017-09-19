import re
import os
import sys
import subprocess

parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Util.Util import Util

class Slave(Util):
    def __init__(self):  
        self.UtilObj = Util()
        self.SocketObj = self.UtilObj.SocketObj
    
    def windows_client(self):
        info = ['IP','No_of_PCI_Devices','NICs','Ram_Size','OS_Version','Processor_no_of_cores']
        info['find_ubuntu'] = "windows"
    
    def vmware_client(self):
        '''PCI/PCIe information'''
        info = {}
        info['find_ubuntu'] = "root"
        FLAG = 0
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
        nic = nic_string.replace(",","")
        info['NICs'] =  nic+"("+str(len(new_items))+")" 
        if 'VMware' in info['NICs']:
            FLAG = 1
        else:
            FLAG = 0
        '''IP information'''
        li=""
        p1 = subprocess.Popen(["esxcli network ip interface ipv4 get"],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        ip_address = str(p1.communicate()[0])
        if sys.version_info > (3,0):
            out=ip_address.split("\\n")
            if len(out)>2:
                for i in range(2,len(out)-1):
                    ver35 = (ip_address.split("\\n")[i]).split("  ")[1]
                    if i==(len(out)-2):
                        li+=ver35
                    else:
                        li+=ver35+' ' 
        else:
            out=ip_address.split("\n")
            print (len(out))
            if len(out)>2:
                for i in range(2,len(out)-1):
                    ver27 = (ip_address.split("\n")[i]).split("  ")[1]
                    if i==(len(out)-2):
                        li+=ver27
                    else:
                        li+=ver27+' ' 
        info['IP'] = li
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
            abc = (os_ver[2:-3])
        else:
            abc = (os_ver)

        if FLAG==1:
            info['OS_Version']=abc+"(VM)"
        else:
            info['OS_Version']=abc
        '''Ram Information'''
        p1 = subprocess.Popen(
            ["smbiosDump | grep -A 20 'Memory Device:' | grep 'Size:' | grep -v 'Size: No Memory Installed'"],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
            )
        raminfo = str(p1.communicate()[0])
        ramval = 0
        if sys.version_info > (3,0):
            ramsize = raminfo.split("\\n")[:-1]
        else:
            ramsize = raminfo.split("\n")[:-1]
        for i in ramsize:
            j = int((i.split(": ")[1]).split(" ")[0])
            ramval += j
        info['Ram_Size'] = str(ramval)+"GB"
        info['Remarks']="N/A"
        return info
    
    def linux_client(self):
        '''PCI/PCIe information'''
        info = {}
        FLAG = 0
        p1 = subprocess.Popen(["lspci"], stdout=subprocess.PIPE)
        output = p1.communicate()[0]
        output = output.strip('\n')
        nol = 0
        for line in output.split("\n"): 
            nol = nol + 1
        info['No_of_PCI_Devices'] = str(nol)
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
        nic = nic_string.replace(","," ")
        #nic = nic.replace(" ","_")
        info['NICs'] =  nic+"("+str(len(new_items))+")"
        if 'VMware' in info['NICs']:
            FLAG = 1
        else:
            FLAG = 0
        '''OS information'''
        try:
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
                os_name = str(name[1:-1])
                if (os_name == "SLES"):
              	        opsys = os_name+" "+str(version[:])
                else:
            	        opsys = os_name + " " + str(version[1:])
        except:
                p1=subprocess.Popen(["cat /etc/*-release"], shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
                (out,error)=p1.communicate()
                try:
                        os_name1=re.search("Red Hat",out)
                        if (os_name1.group()=="Red Hat"):
                                os_name=os_name1.group()
                                version=re.search("Red Hat .* ([0-9]+\.*[0-9]*)",out)
                                version=version.group(1)
                                opsys = os_name + " " + str(version)
                except:
                        os_name2=re.search("CentOS",out)
                        if (os_name2==None):
                                os_name="SLES"
                                out=re.search("SUSE .* ([0-9]+\.*[0-9]*)",out)
                                version=out.group(1)
                                opsys = os_name + " " + str(version)
                        elif (os_name2.group()=="CentOS"):
                                os_name=os_name2.group()
                                version=re.search("CentOS .* ([0-9]+\.*[0-9]*)",out)
                                version=version.group(1)
                                opsys = os_name + " " + str(version)
        
        if (re.search("Ubuntu",os_name)):
            	info['find_ubuntu'] = "ubuntu"
        else:
            	info['find_ubuntu'] = "root"
		
        if FLAG == 1:
            	info['OS_Version'] = opsys+"(VM)"
        else:
             	info['OS_Version'] = opsys 
        '''Processor information'''
        if(info['find_ubuntu'] =="ubuntu"):
            p1 = subprocess.Popen(
                              ["cat /proc/cpuinfo  | grep 'name'| uniq|  awk 'NR == 1' | awk -F':' '{print $2}'"], 
                              shell=True, 
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE
                             )
        else:
            p1 = subprocess.Popen(
                              ["dmidecode --type processor | grep 'Version' |  awk 'NR == 1' | awk -F':' '{print $2}'"], 
                              shell=True, 
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE
                             )
        output = str(p1.communicate()[0])
        processor_info = (output.strip('\n')).strip(" ")
        processor_info = processor_info[:]
        #processor_info = processor_info.replace(" ","_")
        p1 = subprocess.Popen(["nproc --all"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output = str(p1.communicate()[0])
        no_of_cores = output.strip('\n')
        abt_processor = processor_info + "_" + no_of_cores
        info['Processor_no_of_cores'] = abt_processor
        '''IP information'''
        if (os_name=="SLES"):
                ip_address=''
                p3 = subprocess.Popen(
                #["hostname -i"],
                ["ifconfig"], 
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
                )
                ip_address1=(p3.communicate()[0])
                for i in ip_address1.split('\n'):
                              ip=re.search('inet addr:((10|192)\.+[0-9]+\.+[0-9]+\.+[0-9]+)',i)
                              if ip!=None:
                                     ip_address+=ip.group(1)+' '
        else:
                p2 = subprocess.Popen(
                ["hostname -I"],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
                )
                ip_address= (p2.communicate()[0])
        ip_address=ip_address.strip('\n')
        info['IP']=ip_address
        '''Ram Information'''
       	p1 = subprocess.Popen(
            ["cat /proc/meminfo | grep 'MemTotal:'"],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
            )
        raminfo = str(p1.communicate()[0]).strip("\n")
        ramsize = (raminfo.split("MemTotal:")[1]).lstrip(" ")
        ramval = round(int(ramsize.split(" ")[0])/1048576.00,2)
        info['Ram_Size'] = str(ramval)+"GB"
        info['Remarks']="N/A"
        return info
    
    def handle_incoming_socket(self,master_socket_conn,addr):
        print ("Created Log Handle")
        display = ['IP','No_of_PCI_Devices','NICs','Ram_Size','OS_Version','Processor_no_of_cores','Remarks']
        while True:
            print ("This is Master socket address %s"%master_socket_conn)
            data = master_socket_conn.recv(1024)
            strdata = str(data.decode())
            print ("Received data from the Master is %s"%strdata)
            if(re.search('prepare',strdata)):
                if (os.uname()[0] == "Linux"):
                    info = SlaveObj.linux_client()
                elif ("VM" in os.uname()[0]):
                    info = SlaveObj.vmware_client()
                else:
                    print ("Windows")
                    info = {'IP':'10.102.100.100','No_of_PCI_Devices':'2','NICs':'1','Ram_Size':'4 GB','OS_Version':'WINDOWS','Processor_no_of_cores':'4'}
                if (info['find_ubuntu'] == "ubuntu"):
                    print ("Received data from the Master is %s"%strdata)
                    out=strdata.split('_')
                    log_handle = open("/home/%s/IMT/Slave_Log.csv"%(out[1]),"w+")
                else:
                    log_handle = open("/opt/IMT/Slave_Log.csv","w+")
                reply = info['find_ubuntu'].encode()
                header = ""
                body = ""
                for i in display:
                    header = (header+","+i).lstrip(",")
                    body = (body+","+info[i]).lstrip(",")
                log_handle.write(header)
                log_handle.write("\n")
                log_handle.write(body)
                log_handle.write("\n")
                log_handle.close()
                no_of_bytes = master_socket_conn.send(reply)
            elif not data:
                reply = "done"
                no_of_bytes = master_socket_conn.send(reply)
                break
            else:
                continue
            print ("No of bytes sent to the Master is : %s"%no_of_bytes)
        master_socket_conn.close()

if  __name__ == "__main__":
    print ("-------------------Program Started------------------......................Welcome World.......................")
    SlaveObj = Slave()
    PORT_NUM = 40197
    p1 = subprocess.Popen(
                              ["lsof | grep -i 40197"],
                              shell=True,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE
                         )
    running_instance = p1.communicate()[0]
    running_instance = str(running_instance.decode())
    if(running_instance != ""):
        if(os.uname()[0] == "VMkernel"):
            pid = running_instance.split(" ")[0]
            print ("process id for VMware to kill is : "+str(pid))
        else:
            pid = (running_instance.split(" ",1)[1]).strip(" ")[0]
            print ("process id for Linux to kill is : "+str(pid))
        kill_process = "kill -9 " + pid
        os.system(kill_process)
    local_socket = SlaveObj.SocketObj.CreateSocket(PORT_NUM)
    if (local_socket == None):
        print("Unable to create the local socket with port no. : 40197")
        sys.exit()
    else:
        print("Successfully Created the Socket from Master File with port no. : 40197")
    while(1):
        print (".....................................................................................................................................")
        master_socket,addr = local_socket.accept()
        print ("Connected to Master")
        SlaveObj.handle_incoming_socket(master_socket,addr)
        print ("-----------------------Program Ended----------------------..........................Thank You...........................")
