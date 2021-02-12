# -*- coding: utf-8 -*-
from flask import Blueprint
# 通过实例化一个 Blueprint 类对象创建蓝本
main = Blueprint('main', __name__)
# 两个参数 蓝本的名字和蓝本所在的包或模块
from . import views, errors