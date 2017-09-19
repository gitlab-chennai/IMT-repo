import fabric
from fabric.api import settings, hide, env, run
from fabric.exceptions import NetworkError
import os
import sys
import re
import subprocess
import pexpect

#ipmac_all = ["10.102.28.31"]
#ipmac_all = ["10.102.29.167","10.102.28.31","10.102.29.116","10.102.29.31","10.102.29.175","10.102.28.65","10.102.28.29","10.102.29.129","10.102.28.27","10.102.29.157","10.102.29.200","10.102.28.203","10.102.29.124","10.102.28.247","10.102.28.191","10.102.28.89","10.102.28.146","10.102.28.121","10.102.28.238","10.102.28.220","10.102.28.55","10.102.28.58","10.102.28.95","10.102.28.50","10.102.28.144"]
#ipmac_all=["10.102.28.58","10.102.28.95","10.102.28.241"]
#ipmac_all = ["10.102.28.214","10.102.28.246","10.102.29.135","10.102.29.162"]
ipmac_win = []
ipmac_vm = []
ipmac_li = []
ipmac_fail = []
HIDE_NONE = 0
HIDE_WARN = 1
HIDE_RUN = 2
HIDE_WARN_RUN = 3
HIDE_ALL = 4

exception_li=["10.102.29.120"]

#from_nwk,to_nwk,a,b=28,28,89,89
from_nwk,to_nwk,a,b=28,29,3,255


def nmap_fun():
    cmd = os.popen("nmap -F -O --osscan-guess 10.102.%d-%d.%d-%d"%(from_nwk,to_nwk,a,b))
    #cmd = os.popen("nmap -F -O --osscan-guess 10.102.29.162")
    out_data = cmd.read()
    out_type = out_data.split("Nmap scan report for")
    for line in out_type:
        line = line.split("TCP/IP fingerprint:")[0]
        ipadd = re.findall("10.102.[0-9]+.[0-9]+",line)
        if ( ipadd != [] ):
                os_type = re.findall("Linux|VMware|Ubuntu|Windows",line)
                if (os_type != []):
                    if ((os_type[0] == "Windows") or (os_type[0] == "windows")):
                        ipmac_win.append(ipadd[0])
                    elif ((os_type[0] == "Linux") or (os_type[0] == "linux") or (os_type[0] == "Ubuntu")):
                        ipmac_li.append(ipadd[0])
			print (ipmac_li)
                    elif (os_type[0] == "VMware"):
                        ipmac_vm.append(ipadd[0])
                    else:
                        ipmac_fail.append(ipadd[0])
                else:
                    ipmac_fail.append(ipadd[0])
def SlaveType():
    print ("Finding Slave type <Windows/Linux/VMware> IP's using nmap")
    os_list = ['Windows','windows','Linux','linux','VMware','Host seems down']
    for mac in ipmac_all:
        p = subprocess.Popen(['nmap', '-F','-O','--osscan-guess',mac],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out_data = str( p.communicate() )
        out_type = out_data.split("TCP/IP fingerprint:")[0]
        slave_type = "Not Working or Powered Off"
        for os_type in os_list:
            if(re.search(os_type, out_type)):
                slave_type = os_type
        print ("%s Slave OS is %s "%(mac,slave_type))
        if (slave_type != "Not Working or Powered Off"):
            if (slave_type != 'Host seems down'):
                if ((slave_type == "Windows") or (slave_type == "windows")):
                    ipmac_win.append(mac)
                elif ((slave_type == "Linux") or (slave_type == "linux")):
                   ipmac_li.append(mac)
                elif (slave_type == "VMware") :
                    ipmac_vm.append(mac)
                else:
                    ipmac_fail.append(mac)
            else:
                ipmac_fail.append(mac)
        else:
            ipmac_fail.append(mac)
def RunIp():
    print ("---------------Program Started--------------..................Welcome World...................")
    nmap_fun()
    print ("List before remove ip:",ipmac_li)
    for i in ipmac_li:
         if i in exception_li:
            ipmac_li.remove(i) 
    print ("List after remove ip:",ipmac_li)
    #SlaveType()
    #for mac in ipmac_win:
         #print ("**************************************************************************************************************")
         #logonuser = connect_host(mac)
    for mac in ipmac_li:
        #print ("Linux User IP's are : %s"%ipmac_li)
        print ("************************************************Hi Linux User**************************************************************")
        logonuser = connect_host(mac)
        if ( logonuser == "invalid" ):
            continue
        else:
            slave_path = "ps -eaf | grep \"Slave.py\" | grep -v grep"
            slave_process = execute(slave_path,path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
            print (slave_process)
       	    check_proc_status = re.search('Slave.py',slave_process)
       	    if (check_proc_status != None ):
       	        pid = (((str(slave_process).strip("\n")).split(" ",1)[1]).strip(" ")).split(" ")[0]
                kill_path = "kill -9 " + str(pid)
                print ("process to be kill is : "+str(kill_path))
                kill_process = execute(kill_path,path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                print ("Slave.py process killing completed in : " + str(mac))
            else:
                print ("Slave.py process doesn't exists to kill in : " + str(mac))
            if ( logonuser == "root" ):
                slave_folder_check = execute("ls /opt | grep \"^IMT$\"",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                check_fold_status = re.search('IMT',slave_folder_check)
                if (check_fold_status != None):
                    slave_folder_delete = execute("rm -rf /opt/IMT/",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                    print ("IMT folder deleted in : " + str(mac))
                else:
                    print ("IMT folder doesn't exists in : " + str(mac))
            elif ( (logonuser == "ubuntu") or (logonuser=='sesqa') ):
                slave_folder_check = execute("ls /home/ubuntu | grep \"^IMT$\"",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                check_fold_status = re.search('IMT',slave_folder_check)
                if (check_fold_status != None):
                    slave_folder_delete = execute("rm -rf /home/ubuntu/IMT/",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                    print ("IMT folder deleted in : " + str(mac))
                else:
                    print ("IMT folder doesn't exists in : " + str(mac))
    for mac in ipmac_vm:
        print ("**********************************************Hi vmware****************************************************************")
        logonuser = connect_host(mac)
        #print ("vm user ip's are:"ipmac_vm)
        if ( logonuser == "invalid" ):
            continue
        else:
            slave_path = "ps -c | grep \"Slave.py\" | grep -v grep"
            slave_process = execute(slave_path,path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
            print (slave_process)
            check_proc_status = re.search('Slave.py',slave_process)
            if (check_proc_status != None ):
                pid = (str(slave_process).strip("\n")).split(" ")[0]
                kill_path = "kill -9 " + str(pid)
                print ("process to be kill is : "+str(kill_path))
                kill_process = execute(kill_path,path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                print ("Slave.py process killing completed in : " + str(mac))
            else:
                print ("Slave.py process doesn't exists to kill in : " + str(mac))
            if ( logonuser == "root" ):
                slave_folder_check = execute("ls /opt | grep \"^IMT$\"",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                check_fold_status = re.search('IMT',slave_folder_check)
                if (check_fold_status != None):
                    slave_folder_delete = execute("rm -rf /opt/IMT/",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                    print ("IMT folder deleted in : " + str(mac))
                else:
                    print ("IMT folder doesn't exists in : " + str(mac))
            elif ( logonuser == "ubuntu" ):
                slave_folder_check = execute("ls /home/ubuntu | grep \"^IMT$\"",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                check_fold_status = re.search('IMT',slave_folder_check)
                if (check_fold_status != None):
                    slave_folder_delete = execute("rm -rf /home/ubuntu/IMT/",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
                    print ("IMT folder deleted in : " + str(mac))
                else:
                    print ("IMT folder doesn't exists in : " + str(mac))
    print ("---------------Program Ended--------------..................Thank You...................")
def connect_host(slave_ip,username="root",passwd="root123"):
    try:
        print ("connecting to %s"%slave_ip)
        fabric.api.env.host_string = slave_ip
        fabric.api.env.user = username
        fabric.api.env.password = passwd
        fabric.api.env.shell = "/bin/sh -c"
        env.abort_on_prompts = True
        log_con = fabric.api.run("ls")
        print ("Successsfully Connected with root user : %s"%slave_ip)
        return "root"
    except ( SystemExit, NetworkError ):
        try:
            print ("connecting "+str(slave_ip)+" : with ubuntu as user")
            fabric.api.env.host_string = slave_ip
            fabric.api.env.user = "ubuntu"
            fabric.api.env.password = passwd
            fabric.api.env.shell = "/bin/sh -c"
            #env.abort_on_prompts = False
            log_con = fabric.api.run("ls")
            print ("Successsfully Connected with ubuntu user : %s"%slave_ip)
            return "ubuntu"
    	except ( SystemExit, NetworkError ):
		print ("Failed to connect with root, ubuntu user's")
        	return "invalid"  
def firewal(ip):
    #child = pexpect.spawn ('ssh %s@%s'%(username,ip))
    child = pexpect.spawn ('ssh ubuntu@%s'%(ip))
    child.expect ('password: ')
    child.sendline('root123')
    child.sendline ('su root')
    child.expect('Password: ')
    child.sendline('root123')
    #child.sendline('whoami')
    child.sendline('systemctl stop firewalld.service')
    child.sendline('ufw disable')
    child.sendline('exit')
    child.sendline('exit')
    #print child.before
    child.interact()       # Give control of the child to the user.
    #firewal(username,passwd,slave_ip)
def StopFirewall(slave_ip):
    vm_check = execute("vmware -v",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
    vm_status = re.search('VMware',vm_check)
    if(vm_status == None): 
        fire_status = execute("cat /etc/issue",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
        if(re.search('SUSE',fire_status)):
            fire_status = execute("rcSuSEfirewall2 stop",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
            print ("Firewall Disabled for this SUSE Machine")
        elif(re.search('Ubuntu',fire_status)):
            fire_status = firewal(slave_ip)
            print ("Firewall Disabled for this Ubuntu Machine")
        else:
            fire_status = execute("systemctl stop firewalld",path='.',ignore_err=True,hide_opt=None,out_stream=None,err_stream=None,disconnect=False)
            print ("Firewall Disabled for this RHEL/CentOs Machine")
    else:
        execute("esxcli network firewall unload")
        print ("Firewall Disabled for this VMware Machine")
def execute(cmd, path='.', ignore_err=False, hide_opt=None,out_stream=None, err_stream=None, disconnect=True):
    if out_stream is None:
        o_stream = sys.stdout
    else:
        o_stream = out_stream
    if err_stream is None:
        e_stream = sys.stderr
    else:
        e_stream = err_stream
    with settings(warn_only=True):
        if hide_opt == HIDE_WARN:
            with hide('warnings'):
                with fabric.api.cd(path):
                    print "Fabric : Pty : False" 
                    status = fabric.api.run(cmd, stdout=o_stream, stderr=e_stream,pty=False,shell=True)
        elif hide_opt == HIDE_RUN:
            with hide('running'):
                with fabric.api.cd(path):
                    status = fabric.api.run(cmd, stdout=o_stream, stderr=e_stream,pty=False)
        elif hide_opt == HIDE_WARN_RUN:
            with hide('warnings', 'running'):
                with fabric.api.cd(path):
                    status = fabric.api.run(cmd, stdout=o_stream, stderr=e_stream,pty=False)
        elif hide_opt == HIDE_ALL:
            with hide('warnings', 'running', 'stdout'):
                with fabric.api.cd(path):
                    status = fabric.api.run(cmd, stdout=o_stream, stderr=e_stream,pty=False)
        else:
            with fabric.api.cd(path):
                print ("Fabric : pty : None")
                status = fabric.api.run(cmd, stdout=o_stream, stderr=e_stream)
        if disconnect:
            disconnect()
            return status
        if status.return_code == 0:
            return status
        else:
            if ignore_err:
                return status
            else:
                raise AutomationError(
                    "Command '{0}' Failed - Error={1}".format(cmd, status.return_code))
RunIp()
