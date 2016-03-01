#!/usr/bin/env python
#Author: Minjie Wang
import paramiko
from conf import at_config


def icare_system(system):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(at_config.icare_ip,22,at_config.icare_username, at_config.icare_password)
    stdin, stdout, stderr = ssh.exec_command(system)
    cmd_result = stdout.read(),stderr.read()
    ssh.close()
    return cmd_result[0]

def icare_sftp(remotepath,localpath):
    t = paramiko.Transport((at_config.icare_ip,22))
    t.connect(username = at_config.icare_username, password = at_config.icare_password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remotepath, localpath)
    t.close()
    return 0
