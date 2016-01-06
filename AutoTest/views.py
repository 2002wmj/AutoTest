import logging
from django.http import HttpResponse
from django.shortcuts import render_to_response,HttpResponseRedirect
from sbin import test_one,check_env
from app.models import Pro_info

def save_result(pro_id,pro_ident,idf_path,flow_path,topn_path,start_date,finish_date,status=0):
    #保存测试结果数据，并保存
    if status != 0:
        Pro_info.objects.filter(id=pro_id).update(status=3)
    else:
        pro_list = Pro_info.objects.get(id=pro_id)
        pro_list.ident = pro_ident
        pro_list.log = idf_path
        pro_list.flow = flow_path
        pro_list.top_app = topn_path
        pro_list.start_date = start_date
        pro_list.finish_date = finish_date
        pro_list.status = status
        pro_list.save()


def start_test(request):
    pro_id = request.POST.get('pro_id',None)
    pcap_path = request.POST.get('pcap_path',None)
    pro_name = request.POST.get('pro_name',None)
    Pro_info.objects.filter(id=pro_id).update(status=1) #修改运行状态为正在运行
    check_result = check_env.check() #检查服务器icare和web是否启动
    if check_result:
    #检查服务器icare和web是否启动,没有启动责返回错误
        Pro_info.objects.filter(id=pro_id).update(status=3)
        logging.info('hello world')
        return HttpResponse(check_result)
    else:
        start_date,finish_date,pro_ident,idf_path,flow_path,topn_path = test_one.start_test(pcap_path, pro_name)#开始单协议测试，并返回结果
        save_result(pro_id,pro_ident,idf_path,flow_path,topn_path,start_date,finish_date)#将结果保存到数据库
        return render_to_response('result.html',{'name':pro_name,'ident':pro_ident})
