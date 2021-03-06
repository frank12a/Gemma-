# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='role_perimission',
        ),
        migrations.RemoveField(
            model_name='role',
            name='role_userinfo',
        ),
        migrations.AddField(
            model_name='role',
            name='role_perimission',
            field=models.ManyToManyField(related_name='role_usinfo', to='rbac.Permission', verbose_name='拥有权限的角色'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='role_userinfo',
            field=models.ManyToManyField(to='rbac.Role', verbose_name='用户的角色'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='menu_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='自关联'),
        ),
    ]
