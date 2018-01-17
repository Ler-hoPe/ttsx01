from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
import re
# Create your views here.

#
# def register(request):
#     """注册视图"""
#     if request.method == "GET":
#         return render(request, 'register.html')
#     else:
#         # 处理逻辑
#         pass
from users.models import User
from django.core.mail import send_mail
# 倒入设置文件 send_mail函数里填写收件人和发件人
from django.conf import settings
# 在视图要解析令牌 必须使用的密匙
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 导入静态文件 使用过期时间
from utils import constants
# 解析令牌可能出现异常 例如激活码过期
from itsdangerous import SignatureExpired
from celery import Celery

# 导包 调用send_active_email函数
from celery_task.tasks import send_active_email

class RegisterView(View):
    """注册类视图"""
    print("daozheli")

    def get(self, request):
        print("jiexialai")
        return render(request, "register.html")

    def post(self, request):
        # 1：获取参数
        user_name = request.POST.get("user_name")  # None
        password = request.POST.get("pwd")
        password2 = request.POST.get("cpwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")

        # 2：校验参数
        # 使用 all(）函数 判断表单框内是否有数据
        # 参数为一个列表，列表元素为表单标签的属性
        if not all([user_name, password, password2, email, allow]):
            url = reverse("users:register")
            # 如果表单内容不完整 则重定向到注册页面
            return redirect(url)

        # 3：业务实现
        # 判断两次密码是否一致 如果不一致则提醒客户 两次密码不一致
        if password != password2:
            # 使用模板函数 提示客户密码不一致 {"errmsg":"两次密码不一致"}
            return render(request, "register.html", {"errmsg": "两次密码不一致"})

        # 判断邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
            # 如果匹配到则返回结果集  如果没有匹配到则返回 None
            return render(request, "register.html", {"errmsg": "邮箱格式不正确"})

        # 判断是否勾选了协议
        # 注意 checkbox属性  若勾选则会返回一个字符串
        if allow != "on":
            return render(request, "register.html", {"errmsg": "请勾选协议"})
        # 4：保存到数据库
        # django提供Abstract提供了creat_user()的函数 用来创建用户
        # 并且会加密密码然后保存到数据库
        try:
            user = User.objects.create_user(user_name, email, password)
        except IntegrityError as e:
            # django将所有数据库的异常 都封装到了 django.db import IntegrityError 里面
            # 表示用户已经注册
            return render(request, "register.html", {"errmsg": "用户已经注册"})

        # 更改用户的激活状态
        user.is_active = False
        user.save()

        # 生成用户激活的令牌
        token = user.generate_active_token()
        # 拼接激活的链接
        url_active = "http://127.0.0.1:8000/users/active/"+token
        # 5：发送激活邮件  先到setting中进行配置
        # # send_mail(邮件标题，邮件内容，发件人，收件人，htmlmessage = html格式的邮件内容)
        # html_message ="""
        # <h1>欢迎登录天天生鲜用户激活</h1>
        # <h2>尊敬的用户%s,感谢您注册天天生鲜，请在24小时以内激活账户</h2>
        # <a href=%s>%s</a>
        # """ % (user_name, url_active, url_active)
        # send_mail("天天生鲜激活邮件", "", settings.EMAIL_FROM, [email], html_message=html_message)

        #  不在直接发送邮件 而是以Celery的方式发送邮件 异步的方式
        # delay()封装了发布任务的过程
        send_active_email.delay(user_name, url_active, email)
        # 6：返回值

        return HttpResponse("这是登录页面")


class UserActiveView(View):
    def get(self, request, user_token):
        """
        用户激活
        :param request:
        :param user_token: 用户的激活令牌  序列化以后的id
        :return:
        """
        # 在这里解析令牌  必须使用相同的密匙 使用itsdangerous模块 创建同样的对象
        # 创建转换工具对象（序列化器）
        s = Serializer(settings.SECRET_KEY, constants.USER_ACTIVE_EXPIRES)

        try:
            # 使用loads()方法解析令牌
            data = s.loads(user_token)
        except SignatureExpired as e:
            # 表示激活码已经过期 则需要重新注册
            # return render(request, )
            return HttpResponse("激活码已经过期，请重新注册")

        # 注意解析以后的id是一个 字典{"user_id": user_id}
        user_id =data.get("user_id")

        # 修改的时候可能出现异常 如果id不存在 已经被人删除 出现DoesNotExist的异常
        try:
            # 获得用户id以后 将用户修改为已经激活状态 is_active 改为True
            User.objects.filter(id=user_id).update(is_active=True)
            # DoesNotExist 属于模型类的异常
        except User.DoesNotExist:
            # 如果不存在会抛出这个异常
            return HttpResponse("用户不存在")
        return HttpResponse("登陆页面")
