# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2017-11-10 01:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='组的名字')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='菜单的名字')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='权限的名字')),
                ('url', models.CharField(max_length=32, verbose_name='权限url')),
                ('code', models.CharField(max_length=32, verbose_name='代码')),
                ('group_perimission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grop_permission', to='rbac.Group', verbose_name='用这个权限的组')),
                ('menu_id', models.ForeignKey(blank=True, null=None, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='自关联')),
            ],
            options={
                'verbose_name_plural': '权限表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='角色的名字')),
            ],
            options={
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户名字')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.AddField(
            model_name='role',
            name='role_userinfo',
            field=models.ManyToManyField(to='rbac.Userinfo', verbose_name='有角色的用户'),
        ),
        migrations.AddField(
            model_name='permission',
            name='role_perimission',
            field=models.ManyToManyField(related_name='role_usinfo', to='rbac.Role', verbose_name='拥有权限的角色'),
        ),
        migrations.AddField(
            model_name='group',
            name='group_menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='拥有这个组的菜单'),
        ),
    ]