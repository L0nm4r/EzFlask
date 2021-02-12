# -*- coding: utf-8 -*-
from flask import Blueprint
from datetime import datetime

# 通过实例化一个 Blueprint 类对象创建蓝本
main = Blueprint('main', __name__)
# 两个参数 蓝本的名字和蓝本所在的包或模块
from . import views, errors  # 一定要在蓝本创建之后引入
from ..models import Permission


# 下文处理器 避免每次调用 render_template() 时都多添加一个模板参数
@main.app_context_processor
def inject_permissions():  # 能让变量在所有模板中全局可访问
    return dict(Permission=Permission,
                current_time=datetime.utcnow())
