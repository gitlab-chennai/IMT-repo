import fabric

from fabric.api import settings, hide, env, run
from fabric.state import connections, output
from fabric.network import denormalize
from fabric.exceptions import NetworkError

import paramiko
import sys
import pexpect

HIDE_NONE = 0
HIDE_WARN = 1
HIDE_RUN = 2
HIDE_WARN_RUN = 3
HIDE_ALL = 4

class Fabric(object):
    def __init__(self):
        pass
    
    def connect_host(self,hostaddress,username="root",passwd="root123"):
        try:
            print ("Connecting to %s"%hostaddress)
            self._username = username
            self._remote_dns_name = hostaddress
            self._passwd = passwd
            fabric.api.env.host_string = self._remote_dns_name
            fabric.api.env.user = self._username
            fabric.api.env.password = self._passwd
            fabric.api.env.shell = "/bin/sh -c"
            env.abort_on_prompts = True
            print ("Successfully Connected to %s"%hostaddress)
            log_con = fabric.api.run("ls")
            return "root"
        except ( SystemExit, NetworkError ):
            try:
                print ("Connecting to "+str(hostaddress)+" : with ubuntu as user")
                self._username = "ubuntu"
                self._remote_dns_name = hostaddress
                self._passwd = passwd
                fabric.api.env.host_string = self._remote_dns_name
                fabric.api.env.user = self._username
                fabric.api.env.password = self._passwd
                fabric.api.env.shell = "/bin/sh -c"
                print ("Successfully Connected with ubuntu user : %s"%hostaddress)
                log_con = fabric.api.run("ls")
                return "ubuntu"
            except ( SystemExit, NetworkError ):
                print ("Failed to Connect with root, ubuntu user's")
                return "invalid"
    
    def firewal(self,ip):
        child = pexpect.spawn ('ssh ubuntu@%s'%(ip))
        child.expect ('password: ')
        child.sendline('root123')
        child.sendline ('su root')
        child.expect ('Password: ')
       	child.sendline('root123')
        child.sendline('systemctl stop firewalld.service')
        child.sendline('ufw disable')
        child.sendline('exit')
        child.sendline('exit')
       	child.interact()
    
    def execute(self, cmd, path='.', ignore_err=False, hide_opt=None, out_stream=None, err_stream=None, disconnect=True):
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
                        print ("Fabric : Pty : False")
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
                self.disconnect()
                return status
            if status.return_code == 0:
                return status
            else:
                if ignore_err:
                    return status
                else:
                    raise AutomationError("Command '{0}' Failed - Error={1}".format(cmd, status.return_code))
    
    def disconnect(self, log=False):
        for key in connections.keys():
            if output.status:
                connections[key].close()
                del connections[key]
                if output.status:
                    if log:
                        self._logger.info('Disconnected from {0}'.format(denormalize(key)))
                else:
                    self._logger.warning('Failed to disconnect from {0}'.format(denormalize(key)))

class FileTransfer(object):
    def __init__(self,hostname,username="root",password="root123"):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = 22
        self.log_filename = "paramiko" + "_" + hostname + ".log"
        paramiko.util.log_to_file(self.log_filename)
        self.transport = paramiko.Transport((self.hostname, self.port))
        self.transport.connect(username =self.username, password = self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
    
    def push_slave(self):
        all_files = ["/opt/IMT/IMT_Automation/Slave/Slave.py",
                 "/opt/IMT/IMT_Automation/Slave/__init__.py",
                 "/opt/IMT/IMT_Automation/constants.py",
                 "/opt/IMT/IMT_Automation/Util/Util.py",
                 "/opt/IMT/IMT_Automation/Util/__init__.py"]
        for each_file in all_files:
            filepath = localpath = each_file
            self.sftp.put(localpath,filepath)
        self.sftp.close()
    
    def get_log(self,mac):
        remotepath  = "/opt/IMT/Slave_Log.csv"
        localpath = "/opt/repo/"+mac+"Slave_Log.csv"
        self.sftp.get(remotepath,localpath)
        self.sftp.close()
        return 1
    
class FileTransferUb(object):
    def __init__(self,hostname,username="ubuntu",password="root123"):    
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = 22
        self.log_filename = "paramiko" + "_" + hostname + ".log"
        paramiko.util.log_to_file(self.log_filename)
        self.transport = paramiko.Transport((self.hostname, self.port))
        self.transport.connect(username =self.username, password = self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
    
    def push_slave(self):
        all_files = ["/opt/IMT/IMT_Automation/Slave/Slave.py",
                 "/opt/IMT/IMT_Automation/Slave/__init__.py",
                 "/opt/IMT/IMT_Automation/constants.py",
                 "/opt/IMT/IMT_Automation/Util/Util.py",
                 "/opt/IMT/IMT_Automation/Util/__init__.py"]
        all_files_ub = ["/home/ubuntu/IMT/IMT_Automation/Slave/Slave.py",
                 "/home/ubuntu/IMT/IMT_Automation/Slave/__init__.py",
                 "/home/ubuntu/IMT/IMT_Automation/constants.py",
                 "/home/ubuntu/IMT/IMT_Automation/Util/Util.py",
                 "/home/ubuntu/IMT/IMT_Automation/Util/__init__.py"]
        for i in range(0,5):
            self.sftp.put(all_files[i],all_files_ub[i])
        self.sftp.close()
    
    def get_log(self,mac):
        remotepath  = "/home/ubuntu/IMT/Slave_Log.csv"
        localpath = "/opt/repo/"+mac+"Slave_Log.csv"
        self.sftp.get(remotepath,localpath)
        self.sftp.close()
        return 1
