from .base import BaseMessage
class Msg(BaseMessage):
    def __init__(self):
        pass
    def send(self, subject, body, to, name):
        print('短信发送完毕')