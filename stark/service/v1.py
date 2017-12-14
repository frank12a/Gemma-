from django.conf.urls import url
from  django.shortcuts import  HttpResponse,render,redirect
class StarkConfig(object):
    list_display = []
    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site= site
    def get_urls(self):
        app_model_name=(self.model_class._meta.app_label,self.model_class._meta.model_name,)
        print(app_model_name,"app_model_name")
        urlpatterns = [
            url(r'^$',self.changelist,name='%s/%s/changelist'%app_model_name),
            url(r'add/^$',self.add_views,name='%s/%s/addviews'%app_model_name),
            url(r'(\d+)/change/^$',self.change_views,name='%s/%s/changelist'%app_model_name),
            url(r'(\d+)/delete/^$',self.delete_views,name='%s/%s/changelist'%app_model_name)
        ]
        print(urlpatterns)
        return  urlpatterns
    def changelist(self,request,*args,**kwargs):
        # if not self.list_display:
        #
        # else:
        #处理表头数据
        head_list=[]
        for field_name in self.list_display:
            if isinstance(field_name,str):
                verbose_name=self.model_class._meta.get_field(field_name).verbose_name
            else:
                verbose_name=field_name(self,is_header=True)
            head_list.append(verbose_name)

        #处理数据
        data_list=self.model_class.objects.all()
        new_data_list=[]
        for row in data_list:
            temp=[]
            for  field_name in self.list_display:
                if isinstance(field_name,str):
                    val=getattr(row,field_name)
                else:
                    val=field_name(self,row)
                temp.append(val)
            new_data_list.append(temp)
        return  render(request,"stark/changelist.html",{"data_list": new_data_list,"head_list":head_list})

        # return  render(request,)
        #
        # return  HttpResponse("查看列表")
    def add_views(self,request,*args,**kwargs):
        return HttpResponse("增加页面")
    def change_views(self,request,*args,**kwargs):
        return  HttpResponse("编辑页面")
    def delete_views(self,request,*args,**kwargs):
        return  HttpResponse("删除页面")
    @property
    def urls(self):
        return  self.get_urls()
class StarkSite(object):
    def __init__(self):
        self._registy ={}
    def register(self,model_class,stark_config_class=None):
        if not stark_config_class:
            stark_config_class=StarkConfig
        self._registy[model_class]=stark_config_class(model_class,self)
    def get_urls(self):
        urlpatterns = []
        for model_class,stark_config_obj in self._registy.items():
            app_name=model_class._meta.app_label
            model_name=model_class._meta.model_name
            cur_url= url(r'^%s/%s/'%(app_name,model_name),(stark_config_obj.urls,None,None))#不要加逗号
            urlpatterns.append(cur_url)
        return  urlpatterns
    @property
    def urls(self):
        return  (self.get_urls(),None,None)
site=StarkSite()