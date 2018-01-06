from . import models
from django.conf.urls import url
from stark.service import v1
import json
from django.db.models import Q
from  utils import message
from xxxxxx import XXX
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, redirect, render
from django.utils.safestring import mark_safe
from django.urls import reverse

import datetime

from django.forms import ModelForm

class BasePermission(object):
    def get_show_add_btn(self):
        code_list=self.request.permission_codes_list
        if 'add' in code_list:
            return  True
    def get_edit_display(self):
        code_list = self.request.permission_codes_list
        if 'edit' in code_list:
            return  super(SchoolConfig,self).get_edit_display()
        else:
           return []
    def get_list_display(self):
        code_list=self.request.permission_codes_list
        data = []
        if self.list_display:
            data.extend(self.list_display)
            # data.append(v1.StarkConfig.edit)
            if 'del' in code_list:
              data.append(v1.StarkConfig.delete)
            data.insert(0, v1.StarkConfig.checkbox)
        return data
class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['last_consult_date', 'recv_date', 'status', 'consultant',]
class DepartmentConfig(BasePermission,v1.StarkConfig):
    '''
    这是部门表实现了：显示字段、搜索、actions
    '''
    list_display = ['title', 'code']  # 页面显示的字段
    show_actions = False  # 这是actions的显示是否出现
    show_search_form = False  # 不用显示搜索的框
    edit_display = ['title']

    def get_list_display(self):
        result = []
        result.extend(self.list_display)
        result.append(v1.StarkConfig.delete)
        result.insert(0, v1.StarkConfig.checkbox)
        return result


v1.site.register(models.Department, DepartmentConfig)


class UserinfoConfig(BasePermission,v1.StarkConfig):
    '''

    这是用户：我们实现了：显示、搜索、组合搜索（有bug）


    '''
    # search_fields = ['name__contains', 'username__contains','email__contains']  # 这是用来搜索的,不要把外键放在里面
    list_display = ['name', 'username', 'email', 'depart']
    comb_filter = [
        v1.FilterOption('depart', text_func_name=lambda x: str(x), val_func_name=lambda x: x.code),
    ]
    show_actions = False
    show_search_form = False


v1.site.register(models.UserInfo, UserinfoConfig)


class CourseConfig(v1.StarkConfig):
    '''
    课程：用来字段的显示、搜索
    '''
    search_fields = ['name__contains']  # 这是用来搜索的,不要把外键放在里面
    list_display = ['name']
    edit_display = ['name']

    def get_list_display(self):
        result = []
        result.extend(self.list_display)
        # result.append(v1.StarkConfig.edit)
        result.append(v1.StarkConfig.delete)
        result.insert(0, v1.StarkConfig.checkbox)
        return result

    show_actions = False  # 这是actions的


v1.site.register(models.Course, CourseConfig)


class SchoolConfig(BasePermission,v1.StarkConfig):
    '''
     校区：实现了：显示字段、搜索
    '''
    list_display = ['title']
    search_fields = ['title__contains']  # 这是用来搜索的,不要把外键放在里面
    edit_display = ['title']

    def get_list_display(self):
        result = []
        result.extend(self.list_display)
        # result.append(v1.StarkConfig.edit)
        result.append(v1.StarkConfig.delete)
        result.insert(0, v1.StarkConfig.checkbox)
        return result
# comb_filter = [
#         v1.FilterOption('depart', text_func_name=lambda x: str(x), val_func_name=lambda x: x.code),
#     ]

v1.site.register(models.School, SchoolConfig)


class ClassListConfig(v1.StarkConfig):
    def course_semester(self, obj=None, is_header=False):
        if is_header:
            return '班级与期数'
        return ('%s(%s期)') % (obj.course, obj.semester)

    def num(self, obj=None, is_header=False):
        if is_header:
            return '人数'
        return obj.student_set.all().count()

    def get_teacher(self, obj=None, is_header=None):
        if is_header:
            return '咨询课程'
        html = []
        course_list = obj.teachers.all()
        for role in course_list:
            ss = role.name
            html.append(ss)
        html = ','.join(html)
        return html

    list_display = ['school', course_semester, num, 'price', 'start_date', 'graduate_date', 'memo', get_teacher,
                    'tutor']
    search_fields = ['school__contains', 'course__contains', 'semester__contains', 'price__contains',
                     'start_date__contains', 'graduate_date__contains']  # 这是用来搜索的,不要把外键放在里面
    comb_filter = [
        v1.FilterOption('school', ),
        v1.FilterOption('course', ),

    ]


v1.site.register(models.ClassList, ClassListConfig)


class CustomerConfig(v1.StarkConfig):
    '''
    客户信息：显示字段、
    '''

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        urls = [

            url(r'^public/$', self.wrap(self.public), name='%s/%s/public' % app_model_name),
            url(r'^(\d+)/competion/$', self.wrap(self.competion), name='%s/%s/competion' % app_model_name),
            url(r'^sale_views/$', self.wrap(self.sale_views), name='%s/%s/sale_views' % app_model_name),
            url(r'^single/$', self.wrap(self.single), name='%s/%s/single' % app_model_name),
            url(r'^multi/$', self.wrap(self.multi), name='%s/%s/multi' % app_model_name),
        ]
        return urls
    def public(self,request):
        date_now=datetime.datetime.now().date()#当前时间
        date_time_15=datetime.timedelta(days=15)
        date_time_3=datetime.timedelta(days=3)
        deadline1=date_now-date_time_15
        deadline2=date_now-date_time_3
        #方法一：
        con = Q()
        q3=Q(('status',2))
        q1 = Q()
        q1.children.append(('last_consult_date__lt', deadline2))
        q2 = Q()
        q2.children.append(('recv_date__lt',deadline1))
        con.add(q1, 'OR')
        con.add(q2, 'OR')
        con.add(q3,'AND')
        #方法二：
        # models_list=models.Customer.objects.filter(Q(recv_date__lt=deadline1)|Q(last_consult_date__lt=deadline2),status=2)
        models_list=models.Customer.objects.filter(con)
        print(models_list)
        return  render(request,'custmoer_public.html',{'models_list':models_list})
        # return  HttpResponse('ok')
    def competion(self,request,cid):#抢单
        """
        抢单的代码
        """
        current_user_id=5
        #首选判断这个用户是不是在公共的里面和客户顾问不是他本人
        date_now = datetime.datetime.now().date()  # 当前时间
        date_time_15 = datetime.timedelta(days=15)
        date_time_3 = datetime.timedelta(days=3)
        deadline1 = date_now - date_time_15
        deadline2 = date_now - date_time_3
        is_exist=models.Customer.objects.filter(Q(recv_date__lt=deadline1)|Q(last_consult_date__lt=deadline2),status=2).exclude(consultant_id=current_user_id).update(last_consult_date=date_now,recv_date=date_now,consultant_id=current_user_id)
        if not is_exist:
            return HttpResponse("手速慢")
        models.CustomerDistribution.objects.filter(user_id=current_user_id,customer_id=cid,ctime=date_now)
        # return  redirect(request.path_info)
        return HttpResponse("抢单成功")
    def sale_views(self,request):#分配表里查看
        current_user_id = 5
        # customer_list=models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')
        customer_list=models.Customer.objects.filter(consultant_id=current_user_id)
        return render(request,'sale_views.html',{"customer_list":customer_list})
    def single(self,request):
       if request.method=="GET":
           form=SingleModelForm()
           return render(request,'single_form.html',{'form':form})
       else:

         form=SingleModelForm(request.POST)
         if form.is_valid():
             sale_id = XXX.get_sale_id()
             if  not sale_id:
                 return  HttpResponse("没有客户顾问无法分配")
             ctime=datetime.datetime.now().date()
             from django.db import transaction
             try:
                with transaction.atomic():
                     #方法一
                     # form.instance.consultant_id = sale_id
                     # form.instance.recv_date = ctime
                     # form.instance.last_consult_date = ctime
                     # obj = form.save()
                     #方法二
                     form.cleaned_data['consultant_id'] = sale_id
                     form.cleaned_data['recv_date']= ctime
                     form.cleaned_data['last_consult_date']= ctime
                     course_list=form.cleaned_data.pop('course')
                     print('course_list',course_list)
                     obj=models.Customer.objects.create(**form.cleaned_data)
                     obj.course.add(*course_list)
                     models.CustomerDistribution.objects.create(user_id=sale_id,customer=obj,ctime=ctime)
                     #发短信
             except Exception as e:
                 XXX.rollback(sale_id)
             message.send_message('自动发送','很，兴奋代码自动发送邮件，','2981405421@qq.com','大毛')
             return HttpResponse('保存成功')
         else:
             return render(request, 'single_form.html', {'form': form})
    def multi(self,request):
        if request.method=='GET':
            return  render(request,'multi_view.html')
        else:
            ctime = datetime.datetime.now().date()
            from django.db import transaction
            from  io import  BytesIO
            file_obj=request.FILES.get('exfile')
            f=BytesIO()
            for chunk in file_obj:
                f.write(chunk)
            import xlrd
            work_hold = xlrd.open_workbook(file_contents=f.getvalue())
            sheet=work_hold.sheet_by_index(0)
            maps = {
                0: 'qq',
                1: 'name',
                2: 'gender',
                3: 'education',
                4: 'graduation_school',
                5: 'major',
                6: 'experience',
                7: 'work_status',
                8: 'course',
            }
            print('sheet.nrows',sheet.nrows)
            for index in range(1,sheet.nrows):# 这个是获取的行数
                sale_id = XXX.get_sale_id()
                if not sale_id:
                    return HttpResponse("没有客户顾问无法分配")
                row=sheet.row(index)  # 这是通过行数获取行的内容
                dict_obj={} # 字典
                for i in range(len(maps)):     # 这是获取列的数量
                    key=maps[i]        # 这是键
                    cell=row[i]   # 这是获取空格的对象
                    dict_obj[key]=cell.value
                try:
                    with transaction.atomic():
                        dict_obj['consultant_id']=int(sale_id.decode('utf-8'))
                        course_list=[]
                        course_list.extend(dict_obj.pop('course').split(','))
                        obj=models.Customer.objects.create(**dict_obj)
                        obj.course=course_list
                        models.CustomerDistribution.objects.create(user_id=sale_id, customer=obj, ctime=ctime)
                except Exception as e:
                    print(e)
                    XXX.rollback(sale_id)
                message.send_message('自动发送', '很，兴奋代码自动发送邮件，', '2981405421@qq.com', '大毛')
            return HttpResponse('保存成功')




            # file_obj=request.FILES.get('exfile')
            # with open('xxxx.xlsx','wb') as f:
            #     for chunk in file_obj:
            #         f.write(chunk)
            # import  xlrd
            # work_hold=xlrd.open_workbook('xxxx.xlsx')
            # sheet=work_hold.sheet_by_index(0)
            # maps={
            #     0:'学校',
            #     1:'日期',
            # }
            # for index  in range(1,sheet.nrows):# 这个是获取的行数
            #     row=sheet.row(index)  # 这是通过行数获取行的内容
            #     dict_obj={} # 字典
            #     for i in range(len(maps)):     # 这是获取列的数量
            #         key=maps[i]        # 这是键
            #         cell=row[i]   # 这是获取空格的对象
            #         dict_obj[key]=cell.value
            #     print(dict_obj)      # 这是获取对象
            # print(work_hold,type(work_hold))
            # print(file_obj.field_name)#这是对象名字
            # print(file_obj.size)#这是对象名字
            # print(file_obj.name)#这是对象名字
            # print('上传对象',file_obj,type(file_obj))
            # return  HttpResponse('上传成功')






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

    def get_status1(self, obj=None, is_header=None):
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
                    get_status, 'company', 'salary', 'date',get_source, get_course, get_status1, recode]

    # 搜索
    search_fields = ['qq__contains', 'name__contains', 'graduation_school__contains', 'major__contains',
                     'company__contains', 'salary__contains', 'consultant__contains', 'date__contains',
                     'last_consult_date__contains', ]  #

    comb_filter = [ #组合搜索 一个是choice一是多选，和多对一
        v1.FilterOption('gender', is_choice=True),
        v1.FilterOption('education', multi=True,is_choice=True),
        # v1.FilterOption('experience', is_choice=True),
        # v1.FilterOption('work_status', is_choice=True),
        # # v1.FilterOption('source', is_choice=True),
        # # v1.FilterOption('course', True),
        # v1.FilterOption('status', is_choice=True),
        v1.FilterOption('consultant', ),
    ]
    order_by = ['-status']


v1.site.register(models.Customer, CustomerConfig)


class ConsultRecordConfig(v1.StarkConfig):
    list_display = ['customer', 'consultant', 'date']

    comb_filter = [
        v1.FilterOption('customer')
    ]

    def changelist_view(self, request, *args, **kwargs):
        customer = request.GET.get('customer')
        # session中获取当前用户ID
        current_login_user_id = 6
        ct = models.Customer.objects.filter(consultant=current_login_user_id, id=customer).count()
        if not ct:
            return HttpResponse('别抢客户呀...')

        return super(ConsultRecordConfig, self).changelist_view(request, *args, **kwargs)


v1.site.register(models.ConsultRecord, ConsultRecordConfig)


class StudyRecordconfig(v1.StarkConfig):
    def get_record(self, obj=None, is_header=False):
        if is_header:
            return '上课记录'
        return obj.get_record_display()

    list_display = ['course_record', 'student', get_record]
    show_search_form = False
    comb_filter = [
        v1.FilterOption('course_record', ),
    ]
    show_combe_fileter = False

    def get_checked(self, request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='checked')

    get_checked.short_desc = '已签到'

    def get_vacate(self, request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='vacate')

    get_vacate.short_desc = '请假'

    def get_late(self, request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='late')

    get_late.short_desc = '迟到'

    def get_noshow(self, request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='noshow')

    get_noshow.short_desc = '缺勤'

    def get_leave_early(self, request):
        pk_list = request.POST.getlist('pk')
        print('pk', pk_list)
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='leave_early')

    get_leave_early.short_desc = '早退'
    actions = [get_checked, get_vacate, get_late, get_noshow, get_leave_early]
    show_add_btn = False


v1.site.register(models.StudyRecord, StudyRecordconfig)


class CourseRecordconfig(v1.StarkConfig):
    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        urls = [

            url(r'^score_list/(\d+)$', self.wrap(self.score_list), name='%s/%s/score_list' % app_model_name),
        ]

        return urls

    def score_list(self, request, nid):
        if request.method == 'GET':
            study_list = models.StudyRecord.objects.filter(course_record_id=nid)
            choices = models.StudyRecord.score_choices#这个是静态字段的查询
            return render(request, 'scorelist.html', {"study_list": study_list, 'choices': choices})
        elif request.method == 'POST':
            # data={
            #     '3':{'select_name':80,"homework":'你好'},
            #     '2':{'select_name':70,"homework":'你好呀'},
            #     ''' 'select_name_2': ['80'], 'homework_note_2': ['和那后'], 'select_name_3': ['80'], 'homework_note_3': ['韩浩']}>
            #     '''
            # }
            print('******', request.POST)
            data_dict = {}
            for k, val in request.POST.items():
                print(k)
                if k == 'csrfmiddlewaretoken':
                    continue
                name, id = k.rsplit('_', 1)
                if id not in data_dict:
                    print(id)
                    data_dict[id] = {name: val}
                else:
                    data_dict[id][name] = val
            print(data_dict)
            for k, val in data_dict.items():
                models.StudyRecord.objects.filter(id=k).update(**val)
            return  redirect(request.path_info)#返回当前页面
            # return render(request, 'scorelist.html')

    def get_kaoqin(self, obj=None, is_header=False):
        if is_header:
            return '考勤记录'
        return mark_safe('<a href="/frank/crm/studyrecord/?course_record=%s">考勤记录</a>' % (obj.pk))

    def get_scorelist(self, obj=None, is_header=False):
        if is_header:
            return '分数统计'
        rurl = reverse('%s/%s/score_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,),
                       args=(obj.pk,))
        # return mark_safe('<a href="/frank/crm/courserecord/score_list/%s">分数录入</a>' % (obj.pk))
        return mark_safe('<a href="%s">分数录入</a>' % rurl)

    list_display = ['class_obj', 'day_num', get_kaoqin, get_scorelist]
    show_search_form = False

    def multi_init(self, request):  # 这个是初始化上课记录
        courserecord_list = request.POST.getlist('pk')  # 获取所有的需要初始化的班级的id
        crecord_list = models.CourseRecord.objects.filter(id__in=courserecord_list)  # 获取所有需要初始化的班级对象
        for record in crecord_list:  # 循环每个需要初始化的对象
            is_exists = models.StudyRecord.objects.filter(course_record=record).exists()  # 判断在学生记录上是否有这个版的记录
            if is_exists:  # 如果存在就跳过
                continue
            student_list = models.Student.objects.filter(class_list=record.class_obj)  # 找到班级所有的学生
            bulk_list = []
            for student in student_list:
                bulk_list.append(models.StudyRecord(student=student, course_record=record))
            models.StudyRecord.objects.bulk_create(bulk_list)#这个不需要用**
        for record in crecord_list:
            models.StudyRecord.objects.filter()
            models.Student.objects.filter()

        return HttpResponse('.......')

    multi_init.short_desc = '考勤初始化'
    actions = [multi_init]


v1.site.register(models.CourseRecord, CourseRecordconfig)


class Studentconfig(v1.StarkConfig):
    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        urls = [
            url(r'^get_score_view/(\d+)$', self.wrap(self.get_score_view), name='%s/%s/get_score' % app_model_name),
            url(r'^score_show/$', self.wrap(self.score_show), name='%s/%s/score_show' % app_model_name),
        ]
        return urls

    def score_show(self, request):
        ret = {'status': False, 'data': None, 'msg': None}
        try:
            cid = request.GET.get('cid')  # 是班级的id
            print(cid)
            sid = request.GET.get('sid')  # 是任呀
            print(sid)
            record_list = models.StudyRecord.objects.filter(student_id=sid, course_record__class_obj_id=cid)
            print('fuck', record_list)
            data = []
            for item in record_list:
                day = 'day%s' % item.course_record.day_num
                data.append([day, item.score])
            ret['status'] = True
            ret['data'] = data
        except Exception as e:
            ret['msg'] = str(e)
        return HttpResponse(json.dumps(ret))

    def get_score_view(self, request, nid):
        obj = models.Student.objects.filter(id=nid).first()
        if not obj:
            return HttpResponse('查无此人')
        class_list = obj.class_list.all()

        return render(request, 'score_view.html', {"class_list": class_list, 'sid': nid})

    def get_score(self, obj=None, is_header=False):
        if is_header:
            return '查看分数'
        urls = reverse('%s/%s/get_score' % (self.model_class._meta.app_label, self.model_class._meta.model_name,),
                       args=(obj.pk,))
        return mark_safe("<a href='%s'>查看分数</a>" % urls)#反向解析

    list_display = ['username', get_score]


v1.site.register(models.Student, Studentconfig)
class CustomerDistributionConfig(v1.StarkConfig):

    def get_status(self,obj=None,is_header=None):
        if is_header:
            return  '状态'
        return  obj.get_status_display()

    list_display = ['user', 'customer', 'ctime', get_status]
v1.site.register(models.CustomerDistribution,CustomerDistributionConfig)

