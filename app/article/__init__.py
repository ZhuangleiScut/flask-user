#! /usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Blueprint
article = Blueprint('article', __name__)
from . import views
