import copy  # 这是为了保存后面的数据
import json  # 这是为了数据格式

from django.shortcuts import HttpResponse, render, redirect
from django.conf.urls import url
from django.utils.safestring import mark_safe  # 这是为了保护传到页面上的文本变成html标签
from django.urls import reverse  # 这是为了反向生成url
from django.http import QueryDict  # 这是request.GET 的数据结构
from django.db.models import Q  # 这是查询的数据结构


class FilterOption(object):
    """
    这是为了数据结构是从字典变成类，更好的保存数据与使用
    """

    def __init__(self, field_name, multi=False, condition=None, is_choice=False, text_func_name=None,
                 val_func_name=None):
        self.field_name = field_name  # 组合筛选的字段
        self.multi = multi  # 是否可以多选
        self.condition = condition  # 筛选的条件
        self.is_choice = is_choice  # 这个是不是choice
        self.text_func_name = text_func_name  # 这是
        self.val_func_name = val_func_name

    def get_queryset(self, _field):  # 这个是前面配置的筛选条件
        if self.condition:
            return _field.rel.to.objects.filter(**self.condition)
        return _field.rel.to.objects.all()

    def get_choices(self, _field):  # 这个是说明筛选条件是choices
        return _field.choices


class FilterRow(object):
    """
    这是为了更好的把数据在前端显示，用了__iter__方法
    """

    def __init__(self, option, data, request):
        self.data = data  # 这个是筛选条件的数据
        self.option = option  # 这个option是FilterOption的对象
        self.request = request  # 这个就是请求数据

    def __iter__(self):
        '''
             用到了迭代器
        :return:
        '''
        params = copy.deepcopy(self.request.GET)  # 首先把request.GET的数据复制一份
        params._mutable = True  # 用这个设置是说这个数据可以被修改了
        current_id = params.get(self.option.field_name)  # 这个是单列表
        current_id_list = params.getlist(self.option.field_name)  # 这个是获取多个的用getlist
        if self.option.field_name in params:  # 如果gender在里面那么全部就不会亮
            origin_list = params.pop(self.option.field_name)
            print('origin_list', origin_list)
            url = '{0}?{1}'.format(self.request.path_info, params.urlencode())  # 这个使用format格式
            yield mark_safe('<a href="{}">全部</a>'.format(url))  # 用迭代器返回
            params.setlist(self.option.field_name, origin_list)  # 两个结合在一起的
        else:
            url = '{0}?{1}'.format(self.request.path_info, params.urlencode())  # 前面跟的是地址，后面跟的是条件
            yield mark_safe('<a class="active" href="{}">全部</a>'.format(url))  # 如果没有这行的数据，那么全部就变亮
        for val in self.data:
            if self.option.is_choice:  # 如果是多选就执行下面的,步骤。
                pk, text = str(val[0]), val[1]
            else:
                text = self.option.text_func_name(val) if self.option.text_func_name else str(val)  # 这个是三元表达式
                pk = self.option.val_func_name(val) if self.option.val_func_name   else  str(val.pk)
                # pk, text = str(val.pk), str(val)
            # 当前Url  self.request.path_info
            # 问号后面的数据self.request.GET
            if not self.option.multi:
                # 单选
                params[self.option.field_name] = pk  # gender=1
                url = '{0}?{1}'.format(self.request.path_info, params.urlencode())
                if current_id == pk:
                    yield mark_safe('<a href="{0}" class="active">{1}</a>'.format(url, text))
                else:
                    yield mark_safe('<a href="{0}" >{1}</a>'.format(url, text))
            else:
                # 多选
                _parmas = copy.deepcopy(params)
                print('_parmas', _parmas)
                id_list = _parmas.getlist(self.option.field_name)
                print('id_list', id_list)
                print('current_id_list', current_id_list)
                if pk in current_id_list:
                    id_list.remove(pk)
                    _parmas.setlist(self.option.field_name, id_list)
                    url = '{0}?{1}'.format(self.request.path_info, _parmas.urlencode())
                    yield mark_safe('<a href="{0}" class="active">{1}</a>'.format(url, text))

                else:
                    id_list.append(pk)
                    _parmas.setlist(self.option.field_name, id_list)
                    url = '{0}?{1}'.format(self.request.path_info, _parmas.urlencode())
                    yield mark_safe('<a href="{0}" >{1}</a>'.format(url, text))


class ChangeList(object):
    def __init__(self, config, queryset):
        self.config = config  # 这是StarkConfig传过来的self
        self.list_display = config.get_list_display()  # 这是显示的字段
        self.model_class = config.model_class  # 这是我们要处理的类
        self.request = config.request  # 这是传过来self的request
        self.comb_filter = config.get_comb_filter()  # 这是组合搜索的
        self.edit_display = config.get_edit_display()  # 这是编辑的

        self._query_param_key = '_listfilter'  # 这是为了返回页面时定义的一个名字
        self.actions = config.get_actions()  # 这是actions的函数
        self.show_actions = config.get_show_actions()  # 这是是否显示actions
        self.show_add_btn = config.get_show_add_btn()  # 这是是否要显示增加按钮
        self.show_combe_fileter = config.get_show_combe_fileter()  # 这是是否要显示增加按钮

        # 搜索用
        self.show_search_form = config.get_show_search_form()  # 这是是否要显示搜索按钮
        self.search_form_val = config.request.GET.get(config.search_key, '')  # 这是查询时显示查询的内容

        from utils.pager import Pagination  # 这是导入分页的插件
        current_page = self.request.GET.get('page', 1)  # 查询现在的页面
        total_count = queryset.count()  # 查询所有的记录数
        page_obj = Pagination(current_page, total_count, self.request.path_info, self.request.GET, )  # 这是关于页面处理的插件
        self.page_obj = page_obj  # 这是关于页面的所有函数

        self.data_list = queryset[page_obj.start:page_obj.end]  # 关于页面的起止页

        # #这是不一样的代码
        self.show_add_btn = config.get_show_add_btn()  # 这是是否要显示增加按钮
        self.add_url = config.get_add_url()  # 这是增加按钮的url

    def gen_comb_filter(self):
        from django.db.models import ForeignKey, ManyToManyField
        for option in self.comb_filter:  # option是个FilterOption对象
            _field_name = self.model_class._meta.get_field(option.field_name)  # 找到的是的表的字段
            print('_field_name', _field_name)
            if isinstance(_field_name, ForeignKey):
                temp = FilterRow(option, option.get_queryset(_field_name), self.request)
            elif isinstance(_field_name, ManyToManyField):
                temp = FilterRow(option, option.get_queryset(_field_name), self.request)
            else:
                temp = FilterRow(option, option.get_choices(_field_name), self.request)
            yield temp

    def modify_actions(self):  # 这是action里面处理的函数
        result = []
        for func in self.actions:
            temp = {'name': func.__name__, 'text': func.short_desc}
            result.append(temp)
        return result

    def get_change_url(self, nid):  # 这是编辑页面的反向解析
        name = '%s/%s/change_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        change_url = reverse(name, args=(nid,))
        return change_url

    def add_url(self):  # 这是增加url
        return self.config.get_add_url

    def head_list(self):  # 这是处理头部数据的
        result = []
        for field_name in self.list_display:
            if isinstance(field_name, str):  # 是不是字符串
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name  # 获取它的verbose_name
            else:
                verbose_name = field_name(self.config, is_header=True)
            result.append(verbose_name)
        return result

    def body_list(self):
        data_list = self.data_list
        new_data_list = []
        for row in data_list:
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name, str):
                    # print('row',row,type(row))
                    # print('field_name',field_name,type(row))
                    val = getattr(row, field_name)
                    if field_name in self.edit_display:
                        val = self.get_edit_tag(row.pk, val)
                else:
                    val = field_name(self, row)
                temp.append(val)
            new_data_list.append(temp)
        return new_data_list

    def get_edit_tag(self, pk, text):
        query_str = self.request.GET.urlencode()
        params = QueryDict(mutable=True)
        params[self.config._query_param_key] = query_str
        return mark_safe("<a href='%s?%s'>%s</a>" % (self.config.get_change_url(pk), params.urlencode(), text))

    # 这是要删除的url
    def get_delete_url(self, nid):  # 这是删除页面的反向解析
        name = '%s/%s/delete_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        delete_url = reverse(name, args=(nid,))
        return delete_url


class StarkConfig(object):
    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self._query_param_key = '_listfilter'  # 这是固定的值
        self.search_key = 'q'

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' value='%s'>" % (obj.id,))

    def edit(self, obj=None, is_header=False):
        if is_header:
            return '编辑'
        query_str = self.request.GET.urlencode()  # 如果有后面有条件就走下面的方法
        if query_str:
            params = QueryDict(mutable=True)
            params[self._query_param_key] = query_str
            return mark_safe("<a href='%s?%s'>编辑</a>" % (self.get_change_url(obj.id), params.urlencode(),))
        return mark_safe("<a href='%s'>编辑</a>" % (self.get_change_url(obj.id)))

    def delete(self, obj=None, is_header=False):
        if is_header:
            return '删除'
        query_str = self.request.GET.urlencode()
        if query_str:
            params = QueryDict(mutable=True)  # 这是修改这种数据格式
            params[self._query_param_key] = query_str
            return mark_safe("<a href='%s?%s'>删除</a>" % (self.get_delete_url(obj.id), params.urlencode(),))
        return mark_safe("<a href='%s'>删除</a>" % (self.get_delete_url(obj.id)))

    # 这是显示的字段
    list_display = []

    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0, StarkConfig.checkbox)
        return data
        # 这是编辑的字段

    edit_display = []

    def get_edit_display(self):
        result = []
        if self.edit_display:
            result.extend(self.edit_display)
        return result

    # 添加按钮
    show_add_btn = True

    # 显示按钮
    def get_show_add_btn(self):
        return self.show_add_btn

    model_form_class = None

    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class
        from django.forms import ModelForm
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_class
        #         fields = '__all__'
        meta = type('meta', (object,), {'model': self.model_class, 'fields': '__all__'})
        TestModelForm = type("TestModelForm", (ModelForm,), {"Meta": meta})
        return TestModelForm

    # actions定制
    # 是否显示在前端显示
    search_fields = []

    def get_search_fields(self):
        result = []
        if self.search_fields:
            result.extend(self.search_fields)
        return result

    show_actions = True

    def get_show_actions(self):
        return self.show_actions

    actions = []  # 默认actions是空的

    def get_actions(self):  # 这里面放的是actions的函数
        result = []
        if self.actions:
            result.extend(self.actions)
        print('result', result)
        return result

    # 是否要显示搜索按钮
    show_search_form = True

    def get_show_search_form(self):
        return self.show_search_form

    # 这是删除url的反向解析
    def get_delete_url(self, nid):
        name = '%s/%s/delete_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        delete_url = reverse(name, args=(nid,))
        return delete_url

    def get_add_url(self):
        name = '%s/%s/add_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        add_url = reverse(name)
        return add_url

    def get_search_form_condition(self):
            key_word = self.request.GET.get(self.search_key)
            search_fields = self.get_search_fields()
            condition = Q()
            condition.connector = 'or'
            if key_word and self.get_show_search_form:
                for field_name in search_fields:
                    condition.children.append((field_name, key_word))
            return condition

    # 编辑页面的路由系统的反射
    def get_change_url(self, nid):
        name = '%s/%s/change_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        change_url = reverse(name, args=(nid,))
        return change_url

    # 增加页面的路由系统的反射
    def get_add_url(self):
        name = '%s/%s/add_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        add_url = reverse(name)
        return add_url

    # 删除页面
    def get_delete_url(self, nid):
        name = '%s/%s/delete_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        delete_url = reverse(name, args=(nid,))
        return delete_url

    # 展示页面的路由系统的反射
    def get_list_url(self):
        name = '%s/%s/show_lists' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        list_url = reverse(name)
        return list_url
        # 需要页面显示的字段

    show_combe_fileter = True

    def get_show_combe_fileter(self):
        if self.show_combe_fileter:
            return self.show_combe_fileter

    ##组合搜索
    comb_filter = []

    def get_comb_filter(self):
        result = []
        if self.comb_filter:
            result.extend(self.comb_filter)
        return result
    order_by=[]
    def get_order_by(self):
        result=[]
        result.extend(self.order_by)
        return result

    def wrap(self, view_func):
        def inner(request, *args, **kwargs):
            self.request = request
            return view_func(request, *args, **kwargs)

        return inner

    # 生成URL
    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        urlpatterns = [
            url(r'^$', self.wrap(self.changelist), name='%s/%s/show_lists' % app_model_name),
            url(r'^add/$', self.wrap(self.add_views), name='%s/%s/add_list' % app_model_name),
            url(r'^(\d+)/change/$', self.wrap(self.change_views), name='%s/%s/change_list' % app_model_name),
            url(r'^(\d+)/delete/$', self.wrap(self.delete_views), name='%s/%s/delete_list' % app_model_name),
        ]
        urlpatterns.extend(self.extra_url())  # 对URL的扩展
        return urlpatterns

    def extra_url(self):
        return []

    # 展示页面
    def changelist(self, request, *args, **kwargs):
        if request.method == "POST" and self.get_show_actions():
            func_name_str = request.POST.get("list_actions")
            print('PK', request.POST.get('pk'))
            actions_func = getattr(self, func_name_str)
            ret = actions_func(request)
            if ret:
                return ret
        comb_condition = {}
        print('组合搜索条件', request.GET)
        option_list = self.get_comb_filter()
        print(option_list)
        print(request.GET.keys())
        for key in request.GET.keys():
            value_list = request.GET.getlist(key)
            flag = False
            for option in option_list:
                if option.field_name == key:
                    flag = True
                    break
            if flag:
                comb_condition['%s__in' % key] = value_list
        print("************************")
        queryset = self.model_class.objects.filter(self.get_search_form_condition()).filter(**comb_condition).distinct().order_by(*self.get_order_by())
        print('queryset', queryset)
        cl = ChangeList(self, queryset)
        print(cl.body_list)
        return render(request, "stark/changelist.html", {'cl': cl})

    # 增加页面
    def add_views(self, request, *args, **kwargs):
        model_form_class = self.get_model_form_class()
        _popbackid = request.GET.get('_popbackid')
        if request.method == "GET":
            form = model_form_class()
            return render(request, 'stark/add_view.html', {'form': form, 'config': self})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                new_obj = form.save()
                if _popbackid:  # 如果存在就是pop增加的
                    print('走这里啦')
                    from django.db.models.fields.reverse_related import ManyToOneRel
                    result = {'status': False, 'id': None, 'text': None, 'popbackid': _popbackid}  # 构建函数进行传值
                    model_name = request.GET.get("model_name")
                    print('model_name', model_name)
                    related_name = request.GET.get("related_name")
                    print('related_name', related_name)
                    for related_object in new_obj._meta.related_objects:
                        _model_name = related_object.field.model._meta.model_name
                        _related_name = related_object.related_name
                        if (type(related_object) == ManyToOneRel):
                            _field_name = related_object.field_name
                            print('_field_name', _field_name)
                        else:
                            _field_name = 'pk'
                        limit_choices_to = related_object.limit_choices_to  # 获取它的limit_choices_to
                        if (_model_name == model_name) and (str(_related_name) == related_name):  # 判断是否相等
                            is_exists = self.model_class.objects.filter(**limit_choices_to, pk=new_obj.pk).exists()
                            if is_exists:
                                print('存在')
                                result['status'] = True
                                result['id'] = getattr(new_obj, _field_name)  # 获取id
                                result['text'] = str(new_obj)  # 文本内容
                    return render(request, 'stark/pop_response.html',
                                  {'json_result': (json.dumps(result, ensure_ascii=False))})
                else:
                    print('走这里1')
                    return redirect(self.get_list_url())
            return render(request, 'stark/add_view.html', {'form': form, 'config': self})

    def change_views(self, request, nid, *args, **kwargs):  # 这个get添加了找回页面
        obj = self.model_class.objects.filter(pk=nid).first()
        _popbackid = request.GET.get('_popbackid')
        if not obj:
            return redirect(self.get_list_url())
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)
            # new_form = []
            # for bfield in form:
            #     temp = {'is_popurl': False, 'item': bfield}
            #     from django.forms.boundfield import BoundField
            #     from django.db.models.query import QuerySet
            #     from django.forms.models import ModelChoiceField
            #     if isinstance(bfield.field, ModelChoiceField):
            #         related_class_name = bfield.field.queryset.model  # <class 'app04.models.Department'>
            #         if related_class_name in site._registy:  # 这是判断是否注册过
            #             app_model_name = related_class_name._meta.app_label, related_class_name._meta.model_name  # 这是找出反向解析用的
            #             url = reverse('%s/%s/add_list%s/%s/add_list' % app_model_name)  # 反向解析用的基础url
            #             print('url', url)
            #             popurl = ('%s?_popbackid=%s') % (url, bfield.auto_id)  # 这是能找出是哪个的id
            #             print(popurl)
            #             temp['is_popurl'] = True
            #             temp['popurl'] = popurl
            #     new_form.append(temp)
            return render(request, "stark/change_view.html", {"form": form})
        else:
            form = model_form_class(instance=obj, data=request.POST)
            if form.is_valid():
                form.save()
                list_query_str = request.GET.get(self._query_param_key)
                list_url = '%s?%s' % (self.get_list_url(), list_query_str)
                return redirect(list_url)
            return render(request, "stark/change_view.html", {"form": form})

    def delete_views(self, request, nid, *args, **kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        list_query_str = request.GET.get(self._query_param_key)
        list_url = '%s?%s' % (self.get_list_url(), list_query_str)
        return redirect(list_url)

    @property
    def urls(self):
        return self.get_urls()


class StarkSite(object):
    def __init__(self):
        self._registy = {}

    def register(self, model_class, stark_config_class=None):
        if not stark_config_class:
            stark_config_class = StarkConfig
        self._registy[model_class] = stark_config_class(model_class, self)

    def get_urls(self):
        urlpatterns = []
        for model_class, stark_config_obj in self._registy.items():
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name
            cur_url = url(r'^%s/%s/' % (app_name, model_name), (stark_config_obj.urls, None, None))  # 不要加逗号
            urlpatterns.append(cur_url)
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), None, None


site = StarkSite()
