from django.contrib import admin,messages
from django.shortcuts import render_to_response
from app import models
from app.models import Pro_info
# Register your models here.



def start_test(modeladmin,request,queryset):
    #配置后台的动作菜单
    start_pros = Pro_info.objects.filter(status=1)
    if start_pros:
        for start_pro in start_pros:
            start_name = start_pro.name #获取处于正在运行状态的协议名称
            messages.warning(request, u'协议"%s"正在进行测试，无法同时进行多个任务。'%(start_name))
    elif len(queryset) > 1:
        messages.warning(request, u"目前仅支持选择一个协议进行测试。请不要勾选多个。")
    else:
        return render_to_response('autest_admin.html',{'objs': queryset,'title': u'是否开始测试?'})
start_test.short_description = '启动任务' #中文别名



class Pro_info_admin(admin.ModelAdmin):
    fieldsets = (
        (None,{'fields':('name','group','desc','corporation','ident','status')}),
        (None,{'fields':('pcap','log','flow','top_app')})
    ) #配置增加里面菜单项

    search_fields = ('name','desc')
    list_display = ('name','group','desc','ident','status_chinese','start_date','pcap','log','flow','top_app')
    list_filter = ('group','start_date','ident','status')
    list_display_links = ('name','log','flow','pcap')
    actions = [start_test]

admin.site.register(models.Pro_info, Pro_info_admin)
admin.site.register(models.Groups)
