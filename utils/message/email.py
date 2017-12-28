import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


from .base import BaseMessage

class Email(BaseMessage):
    def __init__(self):
        self.email = "18721892893@163.com"
        self.user = "frank"
        self.pwd = '147258369a'

    def send(self, subject, body, to, name):
            print('11111')
            msg = MIMEText(body, 'plain', 'utf-8')  # 发送内容
            msg['From'] = formataddr([self.user, self.email])  # 发件人
            msg['To'] = formataddr([name, to])  # 收件人
            msg['Subject'] = subject  # 主题

            server = smtplib.SMTP("smtp.163.com", 25)  # SMTP服务
            server.login(self.email, self.pwd)  # 邮箱用户名和密码
            server.sendmail(self.email, [to, ], msg.as_string())  # 发送者和接收者
            print('222222')
            server.quit()