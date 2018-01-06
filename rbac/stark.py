from  stark.service import v1
from  . import  models
class Userinfoconfig(v1.StarkConfig):
    list_display = ['id','name',]


v1.site.register(models.Userinfo,Userinfoconfig)
class Roleconfig(v1.StarkConfig):
    list_display = ['id','name','role_perimission']
v1.site.register(models.Role,Roleconfig)
class Groupconfig(v1.StarkConfig):
    list_display = ['id','name','group_menu']
v1.site.register(models.Group,Groupconfig)
class Menuconfig(v1.StarkConfig):
    list_display = ['id','title']
v1.site.register(models.Menu,Menuconfig)
class Permissionconfig(v1.StarkConfig):
    list_display = ['id','title','url','code','group_perimission']
v1.site.register(models.Permission,Permissionconfig)
