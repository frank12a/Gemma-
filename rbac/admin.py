from django.contrib import admin

# Register your models here.
from . import  models

admin.site.register(models.Userinfo)
admin.site.register(models.Permission)
admin.site.register(models.Role)
