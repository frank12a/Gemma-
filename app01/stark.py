from app01 import  models
from stark.service import v1





v1.site.register(models.UserType)
v1.site.register(models.UserInfo)
v1.site.register(models.Role)