#!/usr/bin/env python
#Author: Minjie Wang
import os,urllib.request
from conf import at_config

def check_icare():
    #判断目标服务器的icare是否正常启动
    result_icare = 0
    icare_id_cmd = 'ssh root@%s "pidof icare"'%(at_config.icare_ip )
    icare_id = os.popen(icare_id_cmd).read()
    if not icare_id :
        result_icare = '服务器(%s)的Icare没有正常启动!'%(at_config.icare_ip)
    return result_icare

def check_web():
    #判断目标服务器的WEB是否正常启动
    result_web = 0
    url = 'http://%s:8080/web/login/DoSysLogin.action?username=admin&password=tistone&code=-86791' %(at_config.web_ip)
    try:
        req = urllib.request.urlopen(url)
    except:
        result_web = '服务器(%s)的WEB服务没有正常启动!'%(at_config.web_ip)

    return result_web

def check():
    result = check_icare()
    if result == 0:
        result = check_web()
    return result
