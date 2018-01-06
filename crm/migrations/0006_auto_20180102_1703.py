# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20180102_1703'),
        ('crm', '0005_salerank'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='auth',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Userinfo', verbose_name='用户权限'),
        ),
        migrations.AlterField(
            model_name='customerdistribution',
            name='status',
            field=models.IntegerField(choices=[(1, '正在跟进'), (2, '已成单'), (3, '超过3天未跟进'), (4, '超过15天未成单')], default=1, verbose_name='状态'),
        ),
    ]