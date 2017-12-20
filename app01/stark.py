from app01 import models
from stark.service import v1
from django.forms import ModelForm
from django.shortcuts import render,redirect


class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        error_messages = {
            'name': {
                'required': '用户名不能为空',
            }
        }


class UserInfoConfig(v1.StarkConfig):
    list_display = ['id', 'name','usertype']#页面显示的字段
    # list_filter = ['name', 'usertype']
    model_form_class = UserInfoModelForm#把自定义的ModelForm作为传过去
    search_fields = ['name__contains', 'id__contains','usertype__contains']#这个是查询的字段是模糊查询

    show_actions = True#这是是否显示actions
    def multi_del(self,request):#这是自己定义的函数和actions相关
        pk_list=request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
        return  redirect("http://www.baidu.com")
    multi_del.short_desc='批量删除'#这是函数的名字
    actions=[multi_del]#这里存放actions的函数





class UserTypeConfig(v1.StarkConfig):
    list_display = ['id', 'name']


v1.site.register(models.UserType,UserTypeConfig)

v1.site.register(models.UserInfo, UserInfoConfig)


class RoleConfig(v1.StarkConfig):
    list_display = ['id', 'name']


v1.site.register(models.Role, RoleConfig)
class HostModelForm(ModelForm):
    class Meta:
        model=models.Host
        fields=['id','hostname','ip','port']
        error_messages={
            "hostname":{
                'required':'主机名不能为空',
            },
            'ip':{
                'required':'ip地址不能为空',
                'invalid':'格式错误',
            }
        }
class HostConfig(v1.StarkConfig):
    def ip_port(self,obj=None,is_header=False):
        if is_header:
            return  '自定义列'
        return '%s:%s'%(obj.ip,obj.port,)


    list_display = ['id', 'hostname','ip','port',ip_port]
    model_form_class = HostModelForm
    def delete_views(self, request, nid, *args, **kwargs):
        if request.method=="GET":
            return  render(request,'stark/my_delete.html')
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())


v1.site.register(models.Host, HostConfig)

