from flask import current_app
from flask_login import UserMixin
from itsdangerous import Serializer
from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # 用户名、密码与邮箱，以邮箱作为登录主要凭据
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)

    # 基本信息
    description = db.Column(db.String(128))
    real_name = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    address = db.Column(db.String(128))
    last_login = db.Column(db.DateTime(), default=datetime.now)
    date_joined = db.Column(db.DateTime(), default=datetime.now)
    permissions = db.Column(db.Integer, default=1, nullable=False)  # 权限控制：管理员0, 用户1

    # 业务信息
    is_auth = db.Column(db.Integer, default=0, nullable=False)      # 是否被管理员通过认证。默认为0(未认证), 1(已认证)
    avatar_url = db.Column(db.String(128))                          # 头像路径，建议设置为一个本地的相对路径的URL

    # 外键
    logs = db.relationship('Log', backref='user', lazy='dynamic')

    # 以下三个函数分别用于对用户密码进行读取保护、散列化以及验证密码
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 以下两个函数用于token的生成和校验
    def generate_reset_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        uid = data.get('id')
        if uid:
            return User.query.get(uid)
        return None


# 插件flask_login的回调函数，用于读取用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


"""
日志监控
@Log:存储用户的操作日志
"""


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))  # 操作涉及的用户
    content = db.Column(db.Text(), nullable=False)  # 操作的主要内容
    """
    type_flag 用于记录操作类型:0代表普通操作如登录等,1代表,2代表,3代表
    """
    type_flag = db.Column(db.Integer, default=0)
    created_time = db.Column(db.DateTime(), default=datetime.now)  # 记录日志时的时间


"""
资讯类管理
@News：新闻资讯
@Notices：系统公告
"""


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)                  # 资讯 ID
    title = db.Column(db.String(128), nullable=False)             # 资讯标题
    poster = db.Column(db.String(128), nullable=False)            # 发布者
    content = db.Column(db.Text(), nullable=False)                # 资讯正文
    visitNum = db.Column(db.Integer, default=0)                   # 浏览次数
    updatedTime = db.Column(db.DateTime(), default=datetime.now)  # 更新时间


class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)                  # 公告 ID
    title = db.Column(db.String(128), nullable=False)             # 公告标题
    poster = db.Column(db.String(128), nullable=False)            # 发布者
    content = db.Column(db.Text(), nullable=False)                # 公告正文
    visitNum = db.Column(db.Integer, default=0)                   # 浏览次数
    updatedTime = db.Column(db.DateTime(), default=datetime.now)  # 更新时间

