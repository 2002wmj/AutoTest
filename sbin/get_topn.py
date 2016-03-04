import re
from bs4 import BeautifulSoup

def get_topn(app_date, topn_file):
    #获取TOPN每个应用的的详细数据，并保存为网页。
    soup = BeautifulSoup(app_date)
    app = soup.find_all(class_='appName  OUTPUT')
    app_list = return_list(app)
    flow = soup.find_all('label',class_='OUTPUT')
    flow_list = return_list(flow)
    percentage = soup.find_all(class_='PercentBar')
    percentage_list = return_list(percentage)
    html_list = save_topn(app_list,flow_list,percentage_list)
    save_html(topn_file,html_list)


def save_topn(app_list,flow_list,percentage_list):
    #保存抓取的topn数据为html文件
    zipped = list(zip(flow_list,percentage_list)) #将所有的流量和百分比打包成一个列表
    zipped_list = [zipped[x:x+3] for x in range(0,len(zipped),3)] #将打包好的列表每3个组成一组
    html_list = []
    count = 1
    for a in app_list:
    #将应用名，总流量,百分比转换成Html表格代码，并写入一个列表
        html_list.append('<tr>')
        html_list.append(set_td(count))
        html_list.append(set_td(a[0]))
        for x in zipped_list[count-1]:
            for y in x:
                html_list.append(set_td(y[0]))
        html_list.append('</tr>')
        count += 1
    return html_list

def set_td(data):
    #添加html列表标示符函数
    data_td = '<td>' + str(data) + '</td>'
    return data_td

def return_list(data):
    #传入已经匹配好的的数据，返回具体值得列表。
    regex = re.compile('>([^<]+?)<')
    list = []
    for x in data:
        list.append(re.findall(regex, str(x)))
    return list

def save_html(topn_file,html_list):
    #保存为html格式的文件，带有表格.
    file = open(topn_file,'w')
    file.write('''
<!Doctype html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta HTTP-EQUIV="pragma" CONTENT="no-cache">
<meta HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
<meta HTTP-EQUIV="expires" CONTENT="0">
<title>无标题文档</title>
  <style>
     td {text-align:center}
  </style>
</head>
<body>
<table width="700" height="150" border="1" align="center">
  <tr>
    <td>No</td>
    <td>应用</td>
    <td>总流量</td>
    <td>占百分比</td>
    <td>入境流量</td>
    <td>占百分比</td>
    <td>出境流量</td>
    <td>占百分比</td>
  </tr>
    ''')
    for a in html_list:
        file.write(a)
        file.write('\n')

    file.write('''
</table>
</body>
</html>
    ''')
    file.close()
    return topn_file

