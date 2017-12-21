from app04 import models
from stark.service import v1


class RoleConfig(v1.StarkConfig):
    list_display = ['id', 'title']


v1.site.register(models.Role, RoleConfig)


class DepartmentConfig(v1.StarkConfig):
    list_display = ['id', 'caption']


v1.site.register(models.Department, DepartmentConfig)


class UserInfoConfig(v1.StarkConfig):
    def get_gender(self, obj=None, is_header=None):
        if is_header:
            return "性别"
        return obj.get_gender_display()
    def get_depart(self,obj=None,is_header=None):
        if is_header:
            return '所属部门'
        return obj.depart.caption
    def get_roles(self,obj=None,is_header=None):
        if is_header:
            return '角色'
        html=[]
        role_list=obj.roles.all()
        for role in role_list:
            ss=role.title
            html.append(ss)
        html=','.join(html)
        return  html
    list_display = ['id', 'name', 'email', get_gender,get_depart,get_roles ]#这个显示页面有多对多和FK以及choices
    comb_filter = [
        v1.FilterOption('gender',is_choice=True),
        v1.FilterOption('depart',),
        v1.FilterOption('roles',True)
    ]

v1.site.register(models.UserInfo, UserInfoConfig)
