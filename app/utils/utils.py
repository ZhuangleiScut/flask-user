#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import re

"""
    本文件包含一些常用的工具函数
"""


def reset_domain_url(root_url, proxy_url):
    """root_url为当前主域名的url，proxy_url为API后端返回的URL，需要把root_url与proxy_url的端口组合起来"""
    reobj = re.compile(r'''(?x)\A
    [a-z][a-z0-9+\-.]*://                   # Scheme
    ([a-z0-9\-._~%!$&'()*+,;=]+@)?          # User
    ([a-z0-9\-._~%]+                        # Named or IPv4 host
    |\[[a-z0-9\-._~%!$&'()*+,;=:]+\])       # IPv6+ host
    :(?P<port>[0-9]+)                       # Port number
    ''')

    match = reobj.search(proxy_url)
    if match:
        port = match.group(3)
    else:
        return "error proxy_url"

    return root_url[:-1] + ':' + port


def generate_password():
    """随机生成8位的数字字母的密码"""
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))


def clear_session_cookie(session):
    """清空session中cookie"""
    session['login_cookie'] = None
    session['expire_time'] = None
    print('clear the API cookie in session')


