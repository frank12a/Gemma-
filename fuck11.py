import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

msg = MIMEText('学会用编程发送信息，再来一次。', 'plain', 'utf-8')  # 发送内容
msg['From'] = formataddr(["frank", '18721892893@163.com'])  # 发件人
msg['To'] = formataddr(["二毛", '1448486438@qq.com'])  # 收件人
msg['Subject'] = "【请回复】第一次用邮箱发信息"  # 主题

server = smtplib.SMTP("smtp.163.com", 25) # SMTP服务
server.login("18721892893@163.com", "这是授权码") # 邮箱用户名和授权码
server.sendmail('18721892893@163.com', ['1448486438@qq.com', ], msg.as_string()) # 发送者和接收者
server.quit()



# import smtplib
# from email.mime.text import MIMEText
# from email.utils import formataddr
#
# msg = MIMEText('学会用编程发送信息。', 'plain', 'utf-8')  # 发送内容
# msg['From'] = formataddr(["frank", '发件人的邮箱'])  # 发件人
# msg['To'] = formataddr(["二毛", '1448486438@qq.com'])  # 收件人
# msg['Subject'] = "【请回复】第一次用邮箱发信息"  # 主题
#
# server = smtplib.SMTP("smtp.163.com", 25) # SMTP服务
# server.login("18721892893@163.com", "这是授权密码") # 邮箱用户名和密码
# server.sendmail('18721892893@163.com', ['1448486438@qq.com', ], msg.as_string()) # 发送者和接收者
# server.quit()
