
from . import models
from django.conf.urls import url
from stark.service import v1
import json

from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse,redirect,render
from django.utils.safestring import mark_safe
from django.urls import reverse


class DepartmentConfig(v1.StarkConfig):
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


class UserinfoConfig(v1.StarkConfig):
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


class SchoolConfig(v1.StarkConfig):
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
    def get_record(self,obj=None,is_header=False):
        if is_header:
            return '上课记录'
        return  obj.get_record_display()
    list_display = ['course_record', 'student', get_record]
    show_search_form = False
    comb_filter = [
        v1.FilterOption('course_record', ),
                     ]
    show_combe_fileter=False
    def get_checked(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='checked')

    get_checked.short_desc='已签到'
    def get_vacate(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='vacate')
    get_vacate.short_desc='请假'

    def get_late(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='late')

    get_late.short_desc = '迟到'

    def get_noshow(self,request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='noshow')

    get_noshow.short_desc = '缺勤'

    def get_leave_early(self,request):
        pk_list=request.POST.getlist('pk')
        print('pk',pk_list)
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='leave_early')
    get_leave_early.short_desc = '早退'
    actions = [get_checked,get_vacate,get_late,get_noshow,get_leave_early]
    show_add_btn = False





v1.site.register(models.StudyRecord, StudyRecordconfig)


class CourseRecordconfig(v1.StarkConfig):
    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        urls = [

            url(r'^score_list/(\d+)$', self.wrap(self.score_list), name='%s/%s/score_list' % app_model_name),
    ]

        return urls

    def score_list(self,request,nid):
        if request.method=='GET':
            study_list=models.StudyRecord.objects.filter(course_record_id=nid)
            choices=models.StudyRecord.score_choices
            return render(request, 'scorelist.html', {"study_list": study_list, 'choices': choices})
        elif request.method=='POST':
            # data={
            #     '3':{'select_name':80,"homework":'你好'},
            #     '2':{'select_name':70,"homework":'你好呀'},
            #     ''' 'select_name_2': ['80'], 'homework_note_2': ['和那后'], 'select_name_3': ['80'], 'homework_note_3': ['韩浩']}>
            #     '''
            # }
            print('******',request.POST)
            data_dict={}
            for k, val in request.POST.items():
                print(k)
                if k =='csrfmiddlewaretoken':
                      continue
                name, id = k.rsplit('_', 1)
                if id not in data_dict:
                    print(id)
                    data_dict[id] = {name: val}
                else:
                    data_dict[id][name] = val
            print(data_dict)
            for k,val in data_dict.items():
               models.StudyRecord.objects.filter(id=k).update(**val)
            return  redirect(request.path_info)






    def get_kaoqin(self, obj=None, is_header=False):
        if is_header:
            return '考勤记录'
        return mark_safe('<a href="/frank/crm/studyrecord/?course_record=%s">考勤记录</a>'%(obj.pk))

    def get_scorelist(self, obj=None, is_header=False):
        if is_header:
            return '分数统计'
        rurl=reverse('%s/%s/score_list'%(self.model_class._meta.app_label, self.model_class._meta.model_name,),args=(obj.pk,))
        # return mark_safe('<a href="/frank/crm/courserecord/score_list/%s">分数录入</a>' % (obj.pk))
        return mark_safe('<a href="%s">分数录入</a>' % rurl)

    list_display = ['class_obj', 'day_num', get_kaoqin,get_scorelist]
    show_search_form = False


    def multi_init(self,request):#这个是初始化上课记录
        courserecord_list = request.POST.getlist('pk')# 获取所有的需要初始化的班级的id
        crecord_list = models.CourseRecord.objects.filter(id__in=courserecord_list) # 获取所有需要初始化的班级对象
        for record in crecord_list: # 循环每个需要初始化的对象
            is_exists=models.StudyRecord.objects.filter(course_record=record).exists() # 判断在学生记录上是否有这个版的记录
            if is_exists:        #如果存在就跳过
                continue
            student_list=models.Student.objects.filter(class_list=record.class_obj)# 找到班级所有的学生
            bulk_list=[]
            for student in student_list:
                bulk_list.append(models.StudyRecord(student=student,course_record=record))
            models.StudyRecord.objects.bulk_create(bulk_list)
        for record in  crecord_list:
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
        return  urls
    def score_show(self,request):
        ret={'status':False,'data':None,'msg':None}
        try:
            cid=request.GET.get('cid')#是班级的id
            print(cid)
            sid=request.GET.get('sid')#是任呀
            print(sid)
            record_list=models.StudyRecord.objects.filter(student_id=sid,course_record__class_obj_id=cid)
            print('fuck',record_list)
            data=[]
            for item in record_list:
                day='day%s'%item.course_record.day_num
                data.append(['day',item.score])
            ret['status']=True
            ret['data']=data
        except Exception as e :
            ret['msg']=str(e)
        return  HttpResponse(json.dumps(ret))



    def get_score_view(self,request,nid):
        obj=models.Student.objects.filter(id=nid).first()
        if not obj:
            return HttpResponse('查无此人')
        class_list=obj.class_list.all()

        return  render(request,'score_view.html',{"class_list":class_list,'sid':nid})
    def get_score(self,obj=None,is_header=False):
        if is_header:
            return '查看分数'
        urls=reverse('%s/%s/get_score'%(self.model_class._meta.app_label, self.model_class._meta.model_name,),args=(obj.pk,))
        return  mark_safe("<a href='%s'>查看分数</a>"%urls)
    list_display = ['username',get_score ]



v1.site.register(models.Student, Studentconfig)
