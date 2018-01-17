from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from utils import constants
# Create your models here.


class User(AbstractUser, BaseModel):
    """用户"""
    class Meta:
        db_table = "df_users"

    def generate_active_token(self):
        """生成用户激活的令牌"""
        # 创建序列化对象
        s = Serializer(settings.SECRET_KEY, constants.USER_ACTIVE_EXPIRES)
        # 转换对象 生成令牌
        token = s.dumps({"user_id": self.id})
        token = token.decode()  # 将字节转换为字符串 因为路径中传输的是字符串
        return token


class Address(BaseModel):
    """地址"""
    user = models.ForeignKey(User, verbose_name="所属用户")
    receiver_name = models.CharField(max_length=20, verbose_name="收件人")
    receiver_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    detail_addr = models.CharField(max_length=256, verbose_name="详细地址")
    zip_code = models.CharField(max_length=6, verbose_name="邮政编码")

    class Meta:
        db_table = "df_address"




