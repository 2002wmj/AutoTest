#!/usr/bin/env python
#Author: Minjie Wang
import os,time,sys,datetime,logging
from conf import at_config
from sbin import get_webdata


def Tcpprep(pacp_file, cache_file):
    #使用tcpprep工具处理Pacp包
    tcpprep_cmd = 'tcpprep -a client --cachefile=%s --pcap=%s'%(cache_file, pacp_file)
    result = os.system(tcpprep_cmd)
    if result != 0:
        pass
    return tcpprep_cmd

def Tcpreplay(pacp_file, cache_file):
    #回放协议包操作
    tcpreplay_cmd = 'tcpreplay --intf1=eth1 --intf2=eth1 -M 1 --cachefile=%s %s'%(cache_file, pacp_file)
    result = os.system(tcpreplay_cmd)
    if result != 0:
        pass
    return tcpreplay_cmd

def idf_clear():
    #清空icare服务器的idf日志
    cut_line = '################### Auto_Test #########################\n'
    clear_cmd = 'echo -ne "%s" >%s' %(cut_line, at_config.idf_log)
    idf_clear_cmd = "ssh root@%s '%s' "%(at_config.icare_ip, clear_cmd)
    result = os.system(idf_clear_cmd)
    if result != 0:
        pass

def idf_copy(idf_file):
    #将icare服务器的idf日志拷贝到本地
    cp_cmd = "ssh root@%s 'cp %s /tmp/idf.log'"%(at_config.icare_ip, at_config.idf_log)
    scp_cmd = "scp root@%s:/tmp/idf.log %s"%(at_config.icare_ip, idf_file)
    cp_result = os.system(cp_cmd)
    scp_result = os.system(scp_cmd)


def start_test(pacp_path, pro_name):
    pacp_file = os.path.join(os.getcwd(), pacp_path) #生成pacp文件的本地完整路径
    cache_path = os.path.splitext(pacp_path)[0] + '.cache'
    cache_file = os.path.join(os.getcwd(), cache_path) #生成cache文件的本地完整路径
    idf_path = 'files/log/' + pro_name + '_idf.log'
    idf_file = os.path.join(os.getcwd(), idf_path) #生成idf.log的本地完整路径
    flow_path = 'files/flow/' + pro_name + '.xls'
    flow_file = os.path.join(os.getcwd(), flow_path) #生成流记录的本地完整路径
    topn_path = 'files/topapp/' + pro_name + '.html'
    topn_file = os.path.join(os.getcwd(), topn_path) #生成流记录的本地完整路径

    Tcpprep(pacp_file,cache_file)
    idf_clear()
    start_time = datetime.datetime.now() #记录回放开始时间
    Tcpreplay(pacp_file,cache_file)
    time.sleep(30)                       #获取结果间隔时间
    end_time = datetime.datetime.now() #记录回放结束时间
    #start_time = start_time + datetime.timedelta(minutes=-5)
    idf_copy(idf_file) #获取icare的日志文件
    pro_ident = get_webdata.get_data(start_time, end_time, pro_name, flow_file, topn_file) #开始抓取网页数据,返回识别率


    return start_time,end_time,pro_ident,idf_path,flow_path,topn_path
