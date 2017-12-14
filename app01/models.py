from django.db import models

# Create your models here.
class UserInfo(models.Model):
    name=models.CharField(verbose_name='姓名',max_length=32)
    usertype=models.ForeignKey(verbose_name='用户的职位',to="UserType")

    def __str__(self):
        return  self.name
class UserType(models.Model):
    name=models.CharField(verbose_name='职位的名字',max_length=32)
    role=models.ManyToManyField(verbose_name='职位赋予的角色',to="Role")
    def __str__(self):
        return  self.name

class Role(models.Model):
    name=models.CharField(verbose_name='角色名字',max_length=32)

    def __str__(self):
        return self.name