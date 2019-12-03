import os
import re
from PIL import Image
from app.utils.file_manage import get_file_type
from .. import db
from app.models import User
from . import user
from flask import render_template, redirect, request, url_for, current_app, abort, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from ..utils.utils import generate_password, clear_session_cookie


@user.route('/reg/', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template("user/reg.html", title=u"账号注册")
    elif request.method == 'POST':
        _form = request.form
        username = _form['username']
        email = _form['email']
        password = _form['password']
        password2 = _form['password2']

        """此处可继续完善后端验证，如过滤特殊字符等"""
        message_e, message_u, message_p = "", "", ""
        if User.query.filter_by(username=username).first():
            message_u = u'用户名已存在'
        if User.query.filter_by(email=email).first():
            message_e = u'邮箱已存在'
        if password != password2:
            message_p = u'两次输入密码不一致'

        if not re.search('^[a-zA-Z][a-zA-Z0-9]{2,12}$', username):
            message_u = u'用户名必须以字母开头,只能包含字母或数字, 且不能小于3位大于11位'
        # if not re.search('^[a-zA-Z][a-zA-Z0-9]{5,}$', password):
        #     message_p = u'密码只能包含字母与数字, 且不能小于6位'

        data = None
        if message_u or message_e or message_e:
            data = _form
        if message_u or message_p or message_e:
            return render_template("user/reg.html", form=_form,
                                   title=u'账号注册',
                                   message_u=message_u,
                                   message_p=message_p,
                                   message_e=message_e,
                                   data=data)
        else:
            reg_user = User()
            reg_user.email = email
            reg_user.password = password
            reg_user.username = username
            reg_user.avatar_url = current_app.config['DEFAULT_AVATAR']
            reg_user.api_password = generate_password()
            db.session.add(reg_user)
            db.session.commit()
            login_user(reg_user)
            reg_user.last_login = datetime.now()
            db.session.commit()
            return redirect(url_for('main.index'))


@user.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("user/login.html", title=u"用户登录")
    elif request.method == 'POST':
        _form = request.form
        u = User.query.filter_by(email=_form['email']).first()

        if u is None:
            message_e = u'邮箱不存在'
            return render_template('user/login.html',
                                   title=u"用户登录",
                                   data=_form,
                                   message_e=message_e)

        next_url = request.args.get('next')
        if u and u.verify_password(_form['password']):
            login_user(u)
            u.last_login = datetime.now()
            db.session.commit()
            return redirect(next_url or url_for('main.index'))
        else:
            message_p = u"密码错误"
            return render_template('user/login.html',
                                   title=u"用户登录",
                                   data=_form,
                                   message_p=message_p)


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    clear_session_cookie(session)
    return redirect(url_for('user.login'))


@user.route('/setting/information', methods=['GET', 'POST'])
@login_required
def setting_information():
    if request.method == 'GET':
        return render_template('user/setting_information.html', title=u'个人设置')
    elif request.method == 'POST':
        _form = request.form
        cur_user = User.query.filter_by(email=current_user.email).first()
        cur_user.phone = _form['phone']
        cur_user.real_name = _form['real_name']
        cur_user.address = _form['address']
        db.session.commit()
        return render_template('user/setting_information.html',
                               title=u'个人设置',
                               status='success')


@user.route('/setting/password', methods=['GET', 'POST'])
@login_required
def setting_password():
    if request.method == 'GET':
        return render_template('user/setting_password.html', title=u'个人设置')
    elif request.method == 'POST':
        _form = request.form
        cur_user = User.query.filter_by(email=current_user.email).first()
        if cur_user.verify_password(_form['origin_password']):
            if _form['new_password'] == _form['new_password2']:
                cur_user.password = _form['new_password']
                db.session.commit()
                return render_template('user/setting_password.html', title=u'个人设置', status='success')
            else:
                fail_message = u'两次输入新密码不一致，请重新输入'
        else:
            fail_message = u'初始密码错误，请重新输入'

        return render_template('user/setting_password.html',
                               title=u'个人设置',
                               fail_message=fail_message)


@user.route('/setting/avatar', methods=['GET', 'POST'])
@login_required
def setting_avatar():
    if request.method == 'GET':
        return render_template('user/setting_avatar.html', title=u'个人设置')
    elif request.method == 'POST':
        _file = request.files['file']
        avatar_folder = current_app.config['AVATAR_FOLDER']
        file_type = get_file_type(_file.mimetype)
        if _file and '.' in _file.filename and file_type == "img":
            im = Image.open(_file)
            im.thumbnail((128, 128), Image.ANTIALIAS)
            image_path = os.path.join(avatar_folder, "%d.png" % current_user.id)
            im.save(image_path, 'PNG')
            unique_mark = os.stat(image_path).st_mtime
            current_user.avatar_url = '/static/upload/avatar/' + '%d.png?t=%s' % (current_user.id, unique_mark)

            db.session.commit()
            message_success = u'更新图片成功'
            return render_template('user/setting_avatar.html', message_success=message_success)
        else:
            message_fail = u"无效的文件类型"
            return render_template('user/setting_avatar.html', message_fail=message_fail)