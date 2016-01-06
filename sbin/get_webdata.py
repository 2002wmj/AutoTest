#!/usr/bin/env python
#Author: Minjie Wang
import urllib.request, http.cookiejar, sys , re, datetime, time
from conf import at_config
from sbin import get_topn

def input_cookie():
    #导入登录的Cookie值
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
    urllib.request.install_opener(opener)
    cookie_url = 'http://%s:8080/web/login/DoSysLogin.action?username=admin&password=tistone&code=-86791' %(at_config.web_ip)
    req = urllib.request.Request(cookie_url)
    u = urllib.request.urlopen(req)

def get_ident(start_time, end_time, pro_name,topn_file):
    #获取协议的识别率和TOPN数据
    s_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    e_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    url_time = urllib.parse.urlencode({'startTime':s_time,'endTime':e_time}) #对时间参数进行UrlEncode编码
    url = 'http://%s:8080/web/trafficView/topnApp/getTopNData.action?field4Sort=all&topN=10&mDataProp_0=0&mDataProp_1=1&%smDataProp_2=2&netPro=ip&mDataProp_3=3&mDataProp_4=4&mDataProp_6=6&mDataProp_5=5&mDataProp_8=8&mDataProp_7=7&mDataProp_9=9&sColumns=&iColumns=12&showModel=app&mDataProp_10=10&paramValue=&mDataProp_11=11&paramValues=&paramNames=&unit=Bits&showModels=app&iDisplayStart=0&_TimeCond=cust&iDisplayLength=-1&paramName=&sEcho=1' %(at_config.web_ip, url_time)
    print(url)
    app_date = urllib.request.urlopen(url).read().decode('utf-8')
    a = "title='添加策略' class='appName  OUTPUT' >%s</a></div>" %(pro_name)
    b = '"[^w]+width:([^%]+?)%;'
    c = a + b   #拼接正则表达式
    regex = re.compile(c)
    result = re.findall(regex, app_date)
    if result:
        pro_ident = float(result[0])
    else:
        pro_ident = 0
    get_topn.get_topn(app_date, topn_file) #分析topn应用数据，并保存为html格式

    return pro_ident


def get_flow(start_time, end_time, flow_file ):
    #获取流记录数据并保存
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d%%20%H:%M:%S')
    end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d%%20%H:%M:%S')
    url = 'http://%s:8080/web/trafficView/userPkg/getFlowViewExcel.action?startTime=%s&endTime=%s&_TimeCond=cust&netPro=ipv4&transPro=ALL&field4Sort=all&userGroupIDs=&userIDs=&appGroupIDs=-1&appIDs=-1&destIP=&srcPort=-1&destPort=-1&realtime=true&exportScope=conditional&exportFields=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30&exportType=excel&flowType=2&iSortCol_0=10&sSortDir_0=desc&iDisplayLength=30&iDisplayStart=0' %(at_config.web_ip, start_time, end_time)
    print(url)
    urllib.request.urlretrieve(url,flow_file)


def get_data(start_time, end_time, pro_name, flow_file, topn_file):
    input_cookie()
    pro_ident = get_ident(start_time, end_time, pro_name, topn_file)
    get_flow(start_time, end_time, flow_file )

    return pro_ident


