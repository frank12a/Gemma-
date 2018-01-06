import  importlib
from django.conf import  settings
def send_message(subject,body,to,name):
    for cls_path in settings.MESSAGE_CLASSES:
        # cls_path是字符串
        module_path, class_name = cls_path.rsplit('.', maxsplit=1)
        m = importlib.import_module(module_path)  #用字符串作为导入路径
        obj = getattr(m, class_name)()#加上括号说明运行函数
        obj.send(subject, body, to, name, )
