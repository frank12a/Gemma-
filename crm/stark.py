from .import  models
from stark.service import  v1
class DepartmentConfig(v1.StarkConfig):
    list_display = ['title','code']
v1.site.register(models.Department,DepartmentConfig)
class UserinfoConfig(v1.StarkConfig):
    list_display = ['name','username','password','email','depart']

v1.site.register(models.UserInfo,UserinfoConfig)
v1.site.register(models.Course)
v1.site.register(models.School)
v1.site.register(models.ClassList)
v1.site.register(models.Customer)
