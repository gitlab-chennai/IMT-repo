
import fabric

from fabric.api import settings, hide
from fabric.state import connections, output
from fabric.network import denormalize

import paramiko  # Using this module for doing file transfer 
                 # to VMWare machines.
import os
import sys

HIDE_NONE = 0
HIDE_WARN = 1
HIDE_RUN = 2
HIDE_WARN_RUN = 3
HIDE_ALL = 4

class LogStream(object):
    ''' LogStream class - Used for Fabric run's messages logging '''

    def __init__(self, logger_method):
        ''' Iniitializer '''
        self._logger_method = logger_method

    def write(self, text):
        ''' Fabric uses this method to write message '''

        # Instead of writing to stream IO, log message
        line = text.rstrip()

        # Ignore lines '[odie-11] out:'
        if line and not re.match(r'^\[\w+.*\]\s+out\:$', line, re.I):
            self._logger_method(line)

    def flush(self):
        ''' Fabric uses this method to flush stream data '''

        # Logger should do this flush
        pass

class Fabric(object):

    def __init__(self):
        '''
            dummy constructor.
        '''
        pass
        
    def connect_host(self,hostaddress,username="root",passwd="root123"):
        self._username = username
        self._remote_dns_name = hostaddress
        self._passwd = passwd

        fabric.api.env.host_string = self._remote_dns_name
        fabric.api.env.user = self._username
        fabric.api.env.password = self._passwd
        fabric.api.env.shell = "/bin/sh -c"

        return "Successsfully Connected ", hostaddress

    def quit_connection(self):
        self.execute("exit")

    def execute(self, cmd, path='.', ignore_err=False, hide_opt=None,
                out_stream=None, err_stream=None, disconnect=True):
        '''
        Run the command on remote machine using Fabric run API and return remote console
        output if succeeded or exception otherwise.
            cmd         - command to run on remote machine
            path        - path where command should be run from
            hide_opt    - fabric hide option
            ignore_err  - if set raise exception on error
            out_stream  - remote stdout will be sent to this stream
            err_stream  - remote stderr will be sent to this stream
        '''

        if out_stream is None:
            # Use system stdout
            o_stream = sys.stdout
        else:
            o_stream = out_stream

        if err_stream is None:
            # Use system stderr
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
                    print "Fabric : pty : None) "
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
                    raise AutomationError(
                        "Command '{0}' Failed - Error={1}".format(cmd, status.return_code))

    def disconnect(self, log=False):
        ''' Disconnect all ssh connections '''

        for key in connections.keys():
            if output.status:
                connections[key].close()
                del connections[key]
                if output.status:
                    if log:
                        self._logger.info('Disconnected from {0}'.format(denormalize(key)))
                else:
                    self._logger.warning('Failed to disconnect from {0}'.format(denormalize(key)))

    def put_files(self,remote_path, local_path,
                ostream=None, estream=None):
        '''
        Get files from remote host using Fabric get API
            remote_path: path on remote host
            local_path : local host path
            file_sepc  : remote files that match this wildcard will be downloaded
            ostream    : remote stdout will be sent to this stream
            estream    : remote stderr will be sent to this stream
        '''

        print "Placing files into the directory /opt/IMT into the remote host"

        with settings(warn_only=True), hide('running', 'stdout'):
            with fabric.api.cd("/opt/IMT"), fabric.api.lcd("/opt/IMT"):
                file_location = "/opt/IMT"
                status = fabric.api.put(file_location,file_location)
                print "Upload status ", status

        return True

    def get_file(self,mac,ostream=None, estream=None):
        '''
        Get files from remote host using Fabric get API
            remote_path: path on remote host
            local_path : local host path
            file_sepc  : remote files that match this wildcard will be downloaded
            ostream    : remote stdout will be sent to this stream
            estream    : remote stderr will be sent to this stream
        '''

        print "Placing files into the directory /opt/IMT into the remote host"

        with settings(warn_only=True), hide('running', 'stdout'):
            with fabric.api.cd("/opt/IMT"), fabric.api.lcd("/opt/IMT"):
                remote_file_location = "/opt/IMT/log.csv"
                local_path = "/opt/repo/"+mac
                print "Local Path ",local_path
                status = fabric.api.get(remote_file_location,local_path)
                if status.failed:
                    return False
        return True

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
         remotepath  = "/opt/IMT/log.csv"
         localpath = "/opt/repo/"+mac+"log.csv"
         self.sftp.get(remotepath,localpath)
         self.sftp.close()
         return 1 
