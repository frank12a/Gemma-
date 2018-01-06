import urllib

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from rbac import models
from django.forms import ModelForm
from django.forms import widgets as wb
from django.http import StreamingHttpResponse

# class LoginModelForm(ModelForm):
#     class Meta:
#         model = models.Userinfo
#         fields = ['name', 'password']
#         widgets = {
#             'name': wb.TextInput(),
#             'password': wb.PasswordInput()
#         }

from rbac.service.init_permission import inin_permission


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        print(username, pwd)
        obj = models.Userinfo.objects.filter(name=username, password=pwd).first()
        print(obj)
        if obj:
            request.session['user__info'] = {'user_id': obj.id, 'name': obj.userinfo.name, 'uid': obj.userinfo.id}
            inin_permission(request,obj)
            return redirect('/index/')
        return render(request, 'login.html')

from urllib.request import quote

def xiazai(request):
    the_file_name = 'static/模板.xlsx'
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as  f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(quote(the_file_name.rsplit('/', 1)[1]))#用到了字符串的拼接
    print(response['Content-Disposition'])
    return response
def index(request):
    return render(request,'index.html')
