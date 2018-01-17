from celery import Celery
# 导入系统文件包
import os
# 将django项目的配置文件信息保存到操作系统中
os.environ['DJANGO_SETTINGS_MODULE'] = "daylifresh.settings"

# 让django初始化一下，django会读入配置文件信息
# django.setup()会询问系统django配置文件的位置，读入配置文件信息 也就是初始化
# 在启动celery时候需要 在启动django时候不需要 可以主小调
import django
django.setup()

# send_active_email("123","www.itcast.cn","ler_zoe@163.com")


from django.core.mail import send_mail
from django.conf import settings
# 创建celery应用
app = Celery("daylifresh", broker="redis://127.0.0.1:6379/0")
# 定义任务


@app.task
def send_active_email(user_name, url_active, email):
    """发送激活邮件"""
    # send_mail(邮件标题，邮件内容，发件人，收件人，htmlmessage = html格式的邮件内容)
    html_message = """
           <h1>欢迎登录天天生鲜用户激活</h1>
           <h2>尊敬的用户%s,感谢您注册天天生鲜，请在24小时以内激活账户</h2>
           <a href=%s>%s</a>
           """ % (user_name, url_active, url_active)
    send_mail("天天生鲜激活邮件", "", settings.EMAIL_FROM, [email], html_message=html_message)
