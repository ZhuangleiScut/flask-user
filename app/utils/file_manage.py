#! /usr/bin/env python
# -*- coding: utf-8 -*-


def get_file_type(form_file_type):
    """ 获取 form 表单上传文件的类型, 这里只是做一个简单的映射。

    @from_file_type: Flask 获取到的 mimetype 类型

    Flask 通过 werkzeug 来获取文件类型, 代码如下:
    if filename and content_type is None:
        content_type = mimetypes.guess_type(filename)[0] or \
            'application/octet-stream'

    mimetypes 是 python 的文件类型检测模块, guess_type 用来猜测文件类型,
    所有的 mime_type 在下面的链接中给出:
        https://www.iana.org/assignments/media-types/media-types.xhtml
    """

    file_type_dict = {
        # 'application/msword': 'doc',
        'application/pdf': 'pdf',
        'application/msword': 'word',
        'video/mp4': 'video',
        'audio/mp3': 'audio',
        # 'application/vnd.ms-powerpoint': 'ppt',
        # 'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'ppt',
        'video/x-matroska': 'video',
        'audio/mpeg': 'audio',
        'image/png': 'img',
        'image/jpeg': 'img',
        'image/bmp': 'img',
        'text/plain': 'code',
        'text/css': 'code',
        'text/html': 'code',
        'text/javascript': 'code',
        'application/javascript': 'code',
        'text/x-python-script': 'code',
        'text/x-fortran': 'code',
        'text/x-python': 'code',
        'text/x-csrc': 'code',
        'text/x-c++src': 'code',
        'application/x-gzip': 'wrap',
        'application/zip': 'wrap',
        'application/x-tar': 'wrap',
        'application/x-rar-compressed': 'wrap',
        'application/vnd.ms-excel': 'excel'
    }

    return file_type_dict.get(form_file_type, "Unknown")
