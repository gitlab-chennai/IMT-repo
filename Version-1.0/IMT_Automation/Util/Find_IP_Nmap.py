import os,re
import threading 
dict = {}
working_ip = []
wip_os = []
ipmac_work_win = []
ipmac_work_livm = []
ipmac_fail = []

#from_nwk,to_nwk,a,b=29,29,3,3
from_nwk,to_nwk,a,b=28,29,3,255

def nmap_fun():
    cmd = os.popen("nmap -F -O --osscan-guess 10.102.%d-%d.%d-%d"%(from_nwk,to_nwk,a,b))
    out_data = cmd.read()
    #host_up_ipcount = re.search("([0-9]*) host[s]* up",out_data)
    out_type = out_data.split("Nmap scan report for")
    for line in out_type:
        line = line.split("TCP/IP fingerprint:")[0]
        ipadd = re.findall("10.102.[0-9]+.[0-9]+",line)
        if ( ipadd != [] ):
                os_type = re.findall("Linux|VMware|Ubuntu|Windows",line,re.I)
                if (os_type != []):
                    if ((os_type[0]=="Windows") or (os_type[0]=="windows")):
                        ipmac_work_win.append(ipadd[0])	
                    else:
                        ipmac_work_livm.append(ipadd[0])
                        working_ip.append(ipadd[0])
                        wip_os.append(os_type[0])
                        dict[working_ip[len(working_ip)-1]]=("ON",os_type[0])
    for i in range(from_nwk,to_nwk+1):
        for j in range(a,b+1):
                ip_add = "10.102.%d.%d" % (i,j)
                if ip_add not in dict.keys(): 
                    ipmac_fail.append(ip_add)
                    dict[ip_add]=("OFF","N/A")
    print ("Total number of Working IP's are : %d"%(len(ipmac_work_win)+len(ipmac_work_livm)))
    print ("Working Windows IP's are : %s"%(ipmac_work_win))
    print ("Working Linux IP's are : %s"%(ipmac_work_livm))
    print ("Not Working IP's are : %s"%(ipmac_fail))
    #print (dict)
nmap_fun()

print (ipmac_work_win)
print (ipmac_work_livm)
print ("failed ip's are:",ipmac_fail)
