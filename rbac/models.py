from django.db import models


# Create your models here.#5个表7个类
class Menu(models.Model):
    title = models.CharField(max_length=32, verbose_name="菜单的名字")

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=32, verbose_name="组的名字")
    group_menu = models.ForeignKey("Menu", verbose_name="拥有这个组的菜单")

    def __str__(self):
        return self.name


class Userinfo(models.Model):
    """"用户表"""
    name = models.CharField(max_length=32, verbose_name="用户名字")
    password = models.CharField(max_length=32, verbose_name="密码")
    role_userinfo = models.ManyToManyField("Role", verbose_name="用户的角色",blank=True)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.name


class Role(models.Model):  # 角色和用户多对多
    """角色表"""
    name = models.CharField(max_length=32, verbose_name="角色的名字")
    role_perimission = models.ManyToManyField("Permission", verbose_name="拥有权限的角色", related_name="role_usinfo")

    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.name


class Permission(models.Model):
    """权限表"""
    title = models.CharField(max_length=32, verbose_name="权限的名字")
    url = models.CharField(max_length=32, verbose_name="权限url")
    code = models.CharField(max_length=32, verbose_name="代码")
    menu_id = models.ForeignKey("Permission", verbose_name="自关联", blank=True, null=True)

    group_perimission = models.ForeignKey("Group", verbose_name="用这个权限的组", related_name="grop_permission")

    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.title
