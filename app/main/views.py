from flask import render_template
from flask_login import login_required, current_user

from app import db
from app.models import News, Notice
from . import main

"""
本文件主要存储用户端首页数据, 以及各种图表的数据源
"""


@main.route('/')
@login_required
def index():
    # 计算用户资料完整度profile_ratio
    profile_num = 0
    if current_user.real_name is not None and current_user.real_name != '':
        profile_num += 1
    if current_user.phone is not None and current_user.phone != '':
        profile_num += 1
    if current_user.address is not None and current_user.address != '':
        profile_num += 1
    profile_ratio = 40 + profile_num * 20

    # 取出最新的四条系统公告与四条新闻资讯
    news = News.query.order_by(db.desc(News.id)).limit(4)
    notices = Notice.query.order_by(db.desc(Notice.id)).limit(4)

    return render_template("main/index.html",
                           profile_ratio=profile_ratio,
                           news_list=news,
                           notice_list=notices,
                           title=u"我的主页")

