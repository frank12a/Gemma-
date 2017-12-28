from .base import BaseMessage
class Wechat(BaseMessage):
    def __init__(self):
        pass
    def send(self, subject, body, to, name):
        print('微信已经发过')