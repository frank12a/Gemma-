from stark.service import v1
from django.shortcuts import HttpResponse, redirect, render
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf.urls import url
import json
from  crm  import models
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