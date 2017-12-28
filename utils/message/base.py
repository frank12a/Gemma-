
class BaseMessage(object):#先定义一个类，让它继承
    def send(self, subject, body, to, name):
        raise NotImplementedError('未实现send方法')