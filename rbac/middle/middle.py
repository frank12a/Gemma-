import re
from django.conf import settings
from django.shortcuts import  redirect,HttpResponse
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
class LoginMixin(MiddlewareMixin):#登陆中间键
    def process_request(self, request):
        current_url = request.path_info
        if current_url=='/login/':
            return  None
        if request.session.get('user_info'):
            return  None
        return redirect('/login/')
class  middleMixin(MiddlewareMixin):
    #这里面做的是首先判断这个url是不是在权限里面如果不在就让他直接返回回去
    def process_request(self,request):
        current_url=request.path_info
        print("中间件",current_url)
        for url in settings.VLAID:
            if re.match(url,current_url):
                return  None
        permission_dict=request.session.get(settings.PRIMANRY_LIST)
        if not permission_dict:
            return  redirect("/login/")
        flag=False
        for group_id,code_url in permission_dict.items():
            for db_url in code_url["urls"]:
                regax = "^{0}$".format(db_url)
                if re.match(regax, current_url):
                    request.permission_codes_list=code_url["codes"]
                    flag=True
                    break
            if flag:
                break
        if not flag:
            return  HttpResponse("你没有权限")



