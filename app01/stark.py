from app01 import models
from stark.service import v1
from django.forms import ModelForm

print(123)


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
    list_display = ['id', 'name']
    model_form_class = UserInfoModelForm

class UserTypeConfig(v1.StarkConfig):
    list_display = ['id', 'name',]

v1.site.register(models.UserType,UserTypeConfig)

v1.site.register(models.UserInfo, UserInfoConfig)


class RoleConfig(v1.StarkConfig):
    list_display = ['id', 'name']


v1.site.register(models.Role, RoleConfig)
class HostConfig(v1.StarkConfig):
    list_display = ['id', 'hostname','ip','port']

v1.site.register(models.Host, HostConfig)

