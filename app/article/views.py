#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, current_app, abort, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from . import article
from ..models import News, Notice
from .. import db


@article.route('/news', methods=['GET', 'POST'])
@login_required
def news():
    news_list = News.query.all()
    return render_template('article/news.html', title=u"新闻资讯", news_list=news_list)


@article.route('/news/<int:nid>', methods=['GET', 'POST'])
@login_required
def news_detail(nid):
    cur_news = News.query.filter_by(id=nid).first_or_404()
    cur_news.visitNum = cur_news.visitNum + 1
    db.session.commit()
    return render_template('article/news_detail.html', title=u"资讯详情", news=cur_news)


@article.route('/notice', methods=['GET', 'POST'])
@login_required
def notice():
    notices_list = Notice.query.all()
    return render_template('article/notice.html', title=u"系统公告", notices_list = notices_list)


@article.route('/notice/<int:nid>', methods=['GET', 'POST'])
@login_required
def notice_detail(nid):
    cur_notices = Notice.query.filter_by(id=nid).first_or_404()
    cur_notices.visitNum = cur_notices.visitNum + 1
    db.session.commit()
    return render_template('article/notice_detail.html', title=u"公告详情", notice =cur_notices)


@article.route('/help', methods=['GET', 'POST'])
@login_required
def help():
    return render_template('article/help.html', title=u"帮助中心")


@article.route('/help/<int:hid>', methods=['GET', 'POST'])
@login_required
def help_detail(hid):
    return render_template('article/help_detail.html', title=u"问题详情")