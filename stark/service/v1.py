from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.urls import reverse
# from django.core.paginator import Paginator
from utils.pager import Pagination
from django.http import QueryDict
from django.db.models import Q


class ChangeList(object):
    def __init__(self, config, queryset):
        self.config = config
        self.list_display = config.get_list_display()
        self.model_class = config.model_class
        self.request = config.request
        self._query_param_key = '_listfilter'

        def get_show_add_btn(self):
            return self.show_add_btn

        from utils.pager import Pagination
        current_page = self.request.GET.get('page', 1)
        total_count = queryset.count()
        page_obj = Pagination(current_page, total_count, self.request.path_info, self.request.GET, )
        self.page_obj = page_obj
        self.data_list = queryset[page_obj.start:page_obj.end]

    def get_change_url(self, nid):
        name = '%s/%s/change_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        change_url = reverse(name, args=(nid,))
        return change_url

    def get_delete_url(self, nid):
        name = '%s/%s/delete_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        delete_url = reverse(name, args=(nid,))
        return delete_url

    def head_list(self):
        result = []
        for field_name in self.list_display:
            if isinstance(field_name, str):
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name
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
                    val = getattr(row, field_name)
                else:
                    val = field_name(self, row)
                temp.append(val)
            new_data_list.append(temp)
        print('new_data_list', new_data_list)
        return new_data_list

    def get_add_url(self):
        name = '%s/%s/add_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        add_url = reverse(name)
        return add_url

    def add_url(self):
        return self.config.get_add_url


class StarkConfig(object):
    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        return mark_safe("<input type='checkbox' name='pk' value='%s'>" % (obj.id,))

    def edit(self, obj=None, is_header=False):
        if is_header:
            return '编辑'
        query_str = self.request.GET.urlencode()
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
            params = QueryDict(mutable=True)
            params[self._query_param_key] = query_str
            return mark_safe("<a href='%s?%s'>删除</a>" % (self.get_delete_url(obj.id), params.urlencode(),))
        return mark_safe("<a href='%s'>删除</a>" % (self.get_delete_url(obj.id)))

    list_display = []

    # 编辑页面的路由系统的反射
    # def get_change_url(self, nid):
    #     name = '%s/%s/change_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
    #     change_url = reverse(name, args=(nid,))
    #     return change_url
    # 增加页面的路由系统的反射
    # def get_add_url(self):
    #     name = '%s/%s/add_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
    #     add_url = reverse(name)
    #     return add_url
    # 删除页面
    # def get_delete_url(self, nid):
    #     name = '%s/%s/delete_list' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
    #     delete_url = reverse(name, args=(nid,))
    #     return delete_url
    # 展示页面的路由系统的反射
    # def get_list_url(self):
    #     name = '%s/%s/show_lists' % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
    #     list_url = reverse(name)
    #     return list_url
    # 需要页面显示的字段
    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0, StarkConfig.checkbox)
        return data

    # 添加按钮
    show_add_btn = True

    # 显示按钮
    def get_show_add_btn(self):
        return self.show_add_btn

    search_fields = []

    def get_search_fields(self):
        result = []
        if self.search_fields:
            result.extend(self.search_fields)
        return result

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None
        self._query_param_key = '_listfilter'

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
        if request.method == 'GET':
            print('数据', request.GET.get('q'))
            key_word = request.GET.get('q')
            search_fields = self.get_search_fields()
            q1 = Q()
            q1.connector = 'or'
            if key_word:
                for field_name in search_fields:
                    q1.children.append((field_name, key_word))
            queryset = self.model_class.objects.filter(q1)
            cl = ChangeList(self, queryset)
            print(cl.body_list)
            return render(request, "stark/changelist.html", {'cl': cl})

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

    # 增加页面
    def add_views(self, request, *args, **kwargs):
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class()
            return render(request, 'stark/add_view.html', {'form': form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                # list_query_str = request.GET.get(self._query_param_key)
                # list_url = '%s?%s' % (self.get_list_url(), list_query_str)
                # return redirect(list_url)
                return redirect(self.get_list_url())
            return render(request, 'stark/add_view.html', {'form': form})

    def change_views(self, request, nid, *args, **kwargs):
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)
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
        # return redirect(self.get_list_url())

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
