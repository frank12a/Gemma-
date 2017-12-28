from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from . import models
from django.forms import ModelForm
from django.forms import widgets as wb

class LoginModelForm(ModelForm):
    class Meta:
        model=models.UserInfo
        fields=['username','password']
        widgets={
            'username':wb.TextInput(),
            'password':wb.PasswordInput()
        }
def login(request):
    if request.method=='GET':
       form=LoginModelForm()
       return render(request,'login.html',{"form":form})
    else:
        form=LoginModelForm(request.POST)
        if form.is_valid():
            obj=models.UserInfo.objects.filter(**form.cleaned_data).first()
            if obj:
                print(obj.name)
                request.session['username']=obj.name
                print('运行')
                return  redirect('/frank/crm/customer/')
            return render(request, 'login.html', {"form": form})

        return render(request, 'login.html', {"form": form})
                # return  HttpResponse("出错啦")




