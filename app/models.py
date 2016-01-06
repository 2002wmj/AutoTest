from django.db import models

# Create your models here.

class Pro_info(models.Model):
    name = models.CharField(max_length=200, unique=True ,verbose_name="协议名称")
    group = models.ForeignKey('Groups',verbose_name="协议类别")
    desc = models.CharField(max_length=200,blank=True,null=True,verbose_name="描述")
    corporation = models.CharField(max_length=200,blank=True,null=True,verbose_name="公司")
    ident = models.IntegerField(default='0', verbose_name="识别率")
    status =models.IntegerField(default='0',verbose_name="运行状态") #运行状态（0：运行完成，1：正在运行，2：等待运行，3：运行失败）
    pcap = models.FileField(upload_to='./files/pcap/',blank=True,null=True, verbose_name="协议包")
    log = models.FileField(upload_to='./files/log/',blank=True,null=True, verbose_name="icare日志")
    flow = models.FileField(upload_to='./files/flow/',blank=True,null=True, verbose_name="流记录")
    top_app = models.FileField(upload_to='./files/topapp/',blank=True,null=True, verbose_name="TOPN应用")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="运行时间")
    finish_date = models.DateTimeField(blank=True,null=True, verbose_name="结束时间")
    class Meta:
        verbose_name = '协议测试'
        verbose_name_plural = '协议测试'

    def status_chinese(self):
        if self.status == 1:return u'<span style="color:Blue;font-weight:bold">正在运行</span>'
        elif self.status == 2:return u'<span style="color:orange;font-weight:bold">等待运行</span>'
        elif self.status == 3:return u'<span style="color:red;font-weight:bold">运行失败</span>'
        else:return u'<span style="color:green;font-weight:bold">运行完成</span>'
    status_chinese.allow_tags = True
    status_chinese.short_description = '运行状态'

    def __str__(self):
        return self.name


class Groups(models.Model):
    group_name = models.CharField(max_length=200,unique=True,verbose_name="分组名称")

    class Meta:
        verbose_name = '协议分类'
        verbose_name_plural = '协议分类'

    def __str__(self):
        return self.group_name
