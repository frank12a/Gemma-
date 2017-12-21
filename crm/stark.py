from . import models
from django.shortcuts import redirect, render, HttpResponse
from stark.service import v1


class DepartmentConfig(v1.StarkConfig):
    '''
    这是部门表实现了：显示字段、搜索、actions
    '''
    list_display = ['title', 'code']  # 页面显示的字段
    search_fields = ['title__contains', 'code__contains']  # 这是用来搜索的

    def multi_del(self, request):  # 这是自己定义的函数和actions相关
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
        return redirect("http://www.baidu.com")

    show_actions = True  #这是actions的
    multi_del.short_desc = '批量删除'  # 这是函数的名字
    actions = [multi_del]  # 这里存放actions的函数


v1.site.register(models.Department, DepartmentConfig)


class UserinfoConfig(v1.StarkConfig):
    '''

    这是用户：我们实现了：显示、搜索、组合搜索（有bug）


    '''
    search_fields = ['name__contains', 'username__contains','password__contains','email__contains']  # 这是用来搜索的,不要把外键放在里面
    list_display = ['name', 'username', 'password', 'email', 'depart']
    comb_filter = [
        v1.FilterOption('depart'),
    ]


v1.site.register(models.UserInfo, UserinfoConfig)


class CourseConfig(v1.StarkConfig):
    '''
    课程：用来字段的显示、搜索
    '''
    search_fields = ['name__contains']  # 这是用来搜索的,不要把外键放在里面
    list_display = ['name']
    def multi_del(self, request):  # 这是自己定义的函数和actions相关
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
        return redirect("http://www.baidu.com")

    show_actions = True  #这是actions的
    multi_del.short_desc = '批量删除'  # 这是函数的名字
    actions = [multi_del]  # 这里存放actions的函数

v1.site.register(models.Course, CourseConfig)


class SchoolConfig(v1.StarkConfig):
    '''
     校区：实现了：显示字段、搜索
    '''
    list_display = ['title']
    search_fields = ['title__contains']  # 这是用来搜索的,不要把外键放在里面


v1.site.register(models.School, SchoolConfig)


class ClassListConfig(v1.StarkConfig):
    list_display = ['school', 'course', 'semester', 'price', 'start_date', 'graduate_date', 'memo', 'teachers', 'tutor']
    search_fields = ['school__contains','course__contains','semester__contains','price__contains','start_date__contains','graduate_date__contains']  # 这是用来搜索的,不要把外键放在里面
    comb_filter = [

        v1.FilterOption('teachers',True),
        v1.FilterOption('tutor', ),

    ]


v1.site.register(models.ClassList, ClassListConfig)


class CustomerConfig(v1.StarkConfig):
    '''
    客户信息：显示字段、
    '''
    # search_fields = ['qq__contains','name__contains','title__contains','title__contains','title__contains','title__contains','title__contains']
    def get_gendr(self,obj=None,is_header=None):
        if is_header:
            return '性别'
        return obj.get_gender_display()
    def get_education(self,obj=None,is_header=None):
        if is_header:
            return  '学历'
        return obj.get_education_display()
    def get_experience(self,obj=None,is_header=None):
        if is_header:
            return '工作经验'
        return  obj.get_experience_display()
    def get_work_status(self,obj=None,is_header=None):
        if is_header:
            return '职业状态'
        return  obj.get_work_status.display()
    def get_source(self,obj=None,is_header=None):
        if is_header:
            return '客户来源'
        return  obj.get_source_display()
    ##course是多对多
    def get_course(self,obj=None,is_header=None):
        if is_header:
            return '咨询课程'
        html=[]
        course_list=obj.course.all()
        for role in course_list:
            ss=role.name
            html.append(ss)
        html=','.join(html)
        return  html

    def get_status(self,obj=None,is_header=None):
        if is_header:
            return '状态'
        return  obj.get_status_display()
    #显示少了get_status
    def get_status(self,obj=None,is_header=None):
        if is_header:
            return '职业状态'
        return  obj.get_work_status_display()

    list_display = ['qq', 'name',  get_gendr, get_education, 'graduation_school', 'major', get_experience,
                    get_status, 'company', 'salary',get_source,get_course, get_status,'consultant','date','last_consult_date',]

   #搜索
    search_fields = ['qq__contains', 'name__contains','graduation_school__contains','major__contains','company__contains','salary__contains','consultant__contains','date__contains','last_consult_date__contains',]  #

    comb_filter = [

        v1.FilterOption('gender',is_choice=True),
        v1.FilterOption('education', is_choice=True),
        # v1.FilterOption('graduation_school',),
        # v1.FilterOption('major', ),
        v1.FilterOption('experience', is_choice=True),
        v1.FilterOption('work_status', is_choice=True),
        # v1.FilterOption('company', ),
        # v1.FilterOption('salary', ),
        v1.FilterOption('source',  is_choice=True),
        # v1.FilterOption('salary', ),
        # v1.FilterOption('referral_from',),
        v1.FilterOption('course',True ),
        v1.FilterOption('status',is_choice=True ),
        v1.FilterOption('consultant', ),
        # v1.FilterOption('date', ),
        # v1.FilterOption('last_consult_date', ),
    ]

v1.site.register(models.Customer,CustomerConfig)
