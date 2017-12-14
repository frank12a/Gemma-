from app01 import  models
from stark.service import v1
from  django.utils.safestring import mark_safe
print(123)




class UserInfoConfig(v1.StarkConfig):
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' value='%s'>"%(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return '编辑'

        return  mark_safe("<a href='%s/change'>编辑</a>"%(obj.id,))
    list_display=[checkbox,'id','name','usertype',edit]
v1.site.register(models.UserType)
v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Role)