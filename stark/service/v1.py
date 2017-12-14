from django.conf.urls import url
from  django.shortcuts import  HttpResponse,render
class StarkConfig(object):
    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site=site
    def get_urls(self):
        app_model_name=(self.model_class._meta.app_label,self.model_class._meta.model_name)
        urlpatterns = [
            url(r'^$', self.changelist,name='%s/%s/changelist'%app_model_name),
            url(r'add^$', self.add_views,name='%s/%s/addviews'%app_model_name),
            url(r'(\d+)/change^$', self.change_views,namde='%s/%s/changelist'%app_model_name),
            url(r'(\d+)/delete^$', self.delete_views,namde='%s/%s/changelist'%app_model_name),
        ]
        return  urlpatterns
    def changelist(self):
        return  HttpResponse("查看列表")
    def add_views(self):
        return HttpResponse("增加页面")
    def change_views(self):
        return  HttpResponse("编辑页面")
    def delete_views(self):
        return  HttpResponse("删除页面")
    @property
    def urls(self):
        return  self.get_urls()
class StartSite(object):
    def __init__(self):
        self._registy={}
    def register(self,model_class,start_config_class=None):
        if not start_config_class:
            start_config_class=StarkConfig;
        self._registy[model_class]=start_config_class(model_class,self)
    def get_urls(self):
        urlpatterns = []
        for model_class,stark_config_obj in self._registy.items():
            app_name=model_class._meta.app_label
            model_name=model_class._meta.model_name
            cur_url= url(r'^%s/%s/'%(app_name,model_name), (stark_config_obj.uls,None,"stark"))#不要加逗号
            urlpatterns.append(cur_url)
        return  urlpatterns
    @property
    def urls(self):
        return  self.get_urls(),None,None
site=StartSite()