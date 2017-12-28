from stark.service import v1
from django.shortcuts import HttpResponse, redirect, render
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf.urls import url
import json
from  crm  import models
import datetime
from django.db.models import Q

class CustomerConfig(v1.StarkConfig):
    '''
    客户信息：显示字段、
    '''

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        urls = [

            url(r'^public/$', self.wrap(self.public), name='%s/%s/public' % app_model_name),
        ]

    def public(self):
        date_now=datetime.datetime.now().date()#当前时间
        date_time_15=datetime.timedelta(day=15)
        date_time_3=datetime.timedelta(day=3)
        deadline1=date_now-date_time_15
        deadline2=date_now-date_time_3
        # con = Q()
        # q3=Q()
        # q1 = Q()
        # q1.children.append(('last_consult_date__lt', deadline2))
        # q2 = Q()
        # q2.children.append(('recv_date__lt',deadline1))
        # con.add(q1, 'OR')
        # con.add(q2, 'OR')
        # con.add(q3,'and')
        models_list=models.Customer.objects.filter(Q(recv_date__lt=deadline1)|Q(last_consult_date__lt=deadline2),status=2)
        print(models_list)

        pass
    # search_fields = ['qq__contains','name__contains','title__contains','title__contains','title__contains','title__contains','title__contains']
    def get_gendr(self, obj=None, is_header=None):
        if is_header:
            return '性别'
        return obj.get_gender_display()

    def get_education(self, obj=None, is_header=None):
        if is_header:
            return '学历'
        return obj.get_education_display()

    def get_experience(self, obj=None, is_header=None):
        if is_header:
            return '工作经验'
        return obj.get_experience_display()

    def get_work_status(self, obj=None, is_header=None):
        if is_header:
            return '职业状态'
        return obj.get_work_status.display()

    def get_source(self, obj=None, is_header=None):
        if is_header:
            return '客户来源'
        return obj.get_source_display()

    ##course是多对多
    def get_course(self, obj=None, is_header=None):
        if is_header:
            return '咨询课程'
        html = []
        course_list = obj.course.all()
        for role in course_list:
            ss = role.name
            html.append(ss)
        html = ','.join(html)
        return html

    def get_status(self, obj=None, is_header=None):
        if is_header:
            return '状态'
        return obj.get_status_display()

    # 显示少了get_status
    def get_status(self, obj=None, is_header=None):
        if is_header:
            return '职业状态'
        return obj.get_work_status_display()

    def recode(self, obj=None, is_header=None):
        if is_header:
            return '跟进记录'
        return mark_safe("<a href='/stark/crm/consultrecord/?customer=%s'>查看跟进记录</a>" % (obj.pk,))

    list_display = ['qq', 'name', get_gendr, get_education, 'graduation_school', 'major', get_experience,
                    get_status, 'company', 'salary', get_source, get_course, get_status, recode]

    # 搜索
    search_fields = ['qq__contains', 'name__contains', 'graduation_school__contains', 'major__contains',
                     'company__contains', 'salary__contains', 'consultant__contains', 'date__contains',
                     'last_consult_date__contains', ]  #

    comb_filter = [
        v1.FilterOption('gender', is_choice=True),
        v1.FilterOption('education', is_choice=True),
        v1.FilterOption('experience', is_choice=True),
        v1.FilterOption('work_status', is_choice=True),
        v1.FilterOption('source', is_choice=True),
        v1.FilterOption('course', True),
        v1.FilterOption('status', is_choice=True),
        v1.FilterOption('consultant', ),
    ]