# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-27 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_customer_recv_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDistribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateField()),
                ('status', models.IntegerField(choices=[(1, '正在跟进'), (2, '已成单'), (3, '超过3天未跟进'), (4, '超过5天未成单')], verbose_name='状态')),
                ('customet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='咨询客户')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.UserInfo', verbose_name='课程顾问')),
            ],
        ),
    ]