# 狗书阅读笔记 (一)

![1611120563925](Flask/1611120563925.png)

## 第一章 安装

### virtualenv基本使用

virtualenv 环境安装 `pip install virtualenv `/`pip3 install virtualenv`

安装好后`virtualenv --version` 可以查看版本

初始化一个虚拟环境 `virtualenv venv-name`

进入虚拟环境 `source venv-name/bin/activate`

退出环境`deactivate`

> Python 3.3 通过 venv 模块原生支持虚拟环境，命令为 pyvenv . pyvenv 可以替代 virtualenv 
>
> 在 Python 3.3 中使用 pyvenv 命令创建的虚拟环境不包含 pip ，你需要进行手动安装。Python 3.4 改进了这一缺陷， pyvenv 完全可以代替 virtualenv 
>
> pyvenv 使用可以参考 : https://www.daehub.com/archives/8635.html 两个其实差不多

### 书中代码使用

狗书代码地址 https://github.com/miguelgrinberg/flasky.git

可以git clone到本地 用git checkout切换分支,标签

```python
git clone https://github.com/miguelgrinberg/flasky.git
cd flasky
git checkout 1a
```

## 第二章 程序的基本结构

### 初始化

所有 Flask 程序都必须创建一个程序实例,程序实例是 Flask 类的对象，经常使用下述代码创建

```python
from flask import Flask
app = Flask(__name__)
```

> Flask 类的构造函数只有一个必须指定的参数，即程序主模块或包的名字。在大多数程序中，Python 的 \_\_name\_\_ 变量就是所需的值

### 路由和视图函数

在 Flask 程序中定义路由的最简便方式，就是使用程序实例提供的` app.route` 修饰器

```python
@app.route('/')
def index():
	return '<h1>Hello World!</h1>'
```

把 index() 函数注册为程序根地址的处理程序,在浏览器中访问 http://www.example.com 后，会触发服务器执行 index() 函数

> 这里是使用修饰器把函数注册为一个事件的处理程序

像 index() 这样的函数称为视图函数（view function）, 视图函数返回的响应可以是包含HTML 的简单字符串，也可以是复杂的表单



下面的示例可以处理更复杂的请求,匹配类似 ` http://www.facebook.com/<your-name>` 的地址

```python
@app.route('/user/<name>')
def user(name):
	return '<h1>Hello, %s!</h1>' % name
```

路由中的动态部分默认使用字符串,也可以使用别的类型

如 ` /user/<int:id>`只会匹配动态片段 id 为整数的 URL

> Flask 支持在路由中使用 int 、 float 和 path 类型
>
> path 类型也是字符串，但不把斜线视作分隔符，而将其当作动态片段的一部分

### 启动服务器

```python
if __name__ == '__main__':
    app.run(debug=True)
```

> `__name__== ' __main__ '`在这里确保直接执行这个脚本时才启动开发Web 服务器

把 debug 参数设为 True => 启用调试模式

> Flask 提供的 Web 服务器不适合在生产环境中使用,需要搭配别的服务器组件使用

### 请求-响应循环

- 程序和请求上下文

```python
from flask import request
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
```

Flask 使用上下文临时把某些对象变为全局可访问,让特定的变量在一个线程中全局可访问，与此同时却不会干扰其他线程

在 Flask 中有两种上下文：程序上下文和请求上下文,上面的示例是请求上下文

![1611123396878](Flask/1611123396878.png)

- 请求调度

程序收到客户端发来的请求时，要找到处理该请求的视图函数.为了完成这个任务，Flask会在程序的 URL 映射中查找请求的 URL

URL 映射是 URL 和视图函数之间的对应关系

Flask 使用` app.route` 修饰器或者非修饰器形式的 `app.add_url_rule() `生成映射

使用url_map查看映射

![1611123651901](Flask/1611123651901.png)

> ` /static/<filename>` 路由是Flask 添加的特殊路由，用于访问静态文件

- 请求钩子

请求钩子用于处理请求前后的一些工作

请求钩子使用修饰器实现,Flask 支持以下 4 种钩子

​	before_first_request :注册一个函数，在处理第一个请求之前运行。

​	before_request  ：注册一个函数，在每次请求之前运行。

​	after_request  ：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。

​	teardown_request  ：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

- 更丰富的响应

  添加状态码

```python
@app.route('/')
def index():
    return '<h1>Bad Request</h1>', 400
```

​	返回cookie需要使用到`make_response`

```python
from flask import make_response

@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
```

​	重定向

```python
from flask import redirect
@app.route('/')
def index():
	return redirect('http://www.example.com')
```

​	处理错误

```python
from flask import abort
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
    	abort(404)
    return '<h1>Hello, %s</h1>' % user.name
```

### Flask扩展

Flask 只有两个主要依赖：子系统Werkzeug和 模板系统 Jinja2, Werkzeug 和 Jinjia2 都是由 Flask 的核心开发者开发而成

Flask 并不原生支持数据库访问、Web 表单验证和用户认证等高级功能,这些功能以及其他大多数 Web 程序中需要的核心服务都以扩展的形式实现，然后再与核心包集成

所以Flask扩展很丰富

下面以Flask-Script来说明Flask扩展使用

> Flask-Script 是一个 Flask 扩展，为 Flask 程序添加了一个命令行解析器

安装: `pip install flask-script`

导入: `from flask_script import Manager`

> from flask.ext.xxx 已经不再使用.改为 flask_xxx

使用:

```python
from flask import Flask
from flask_script import Manager
app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    manager.run()
```

效果就是加了一些参数

![1611125055547](Flask/1611125055547.png)

运行`python hello.py runserver`

![1611125115144](Flask/1611125115144.png)

--host指定监听ip `python hello.py runserver --host 0.0.0.0`

## 第三章 模板

### Jinja2模板引擎

- 默认情况下，Flask 在程序文件夹中的 templates 子文件夹中寻找模板

  模板示例:

```html
templates/index.html:
<h1>Hello World!</h1>
templates/user.html
<h1>Hello, {{ name }}!</h1>
```

渲染模板--`render_template`

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```

 render_template 函数的第一个参数是模板的文件名, 随后的参数都是键值对，表示模板中变量对应的真实值。

在这段代码中，第二个模板收到一个名为 name 的变量.左边的“name”表示参数名，就是模板中使用的占位符；右边的“name”是当前作用域中的变量，表示同名参数的值

#### 变量

`{{ name }} `结构表示一个变量, 它是一种特殊的占位符,告诉模板引擎这个位置的值从渲染模板时使用的数据中获取

- 复杂变量使用示例:

```python
<p>A value from a dictionary: {{ mydict['key'] }}.</p> # 字典
<p>A value from a list: {{ mylist[3] }}.</p> # 列表
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p> # 列表,变量组合
<p>A value from an object's method: {{ myobj.somemethod() }}.</p> # 对象
```

- 过滤器

可以使用过滤器修改变量，过滤器名添加在变量名之后，中间使用竖线分隔

```jinja2
Hello, {{ name|capitalize }} # 以首字母大写形式显示变量 name 的值
```

常用过滤器

![1611126225191](Flask/1611126225191.png)

> 默认情况下，出于安全考虑，Jinja2 会转义所有变量,对信任的值使用safe过滤器,可以显示HTML代码

完整过滤器列表 https://jinja.palletsprojects.com/en/2.11.x/templates/#builtin-filters

#### 控制结构

条件控制

```jinja2
{% if user %}
    Hello, {{ user }}!
{% else %}
    Hello, Stranger!
{% endif %}
```

for循环

```jinja2
<ul>
    {% for comment in comments %}
        <li>{{ comment }}</li>
    {% endfor %}
</ul>
```

宏

```jinja2
{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}

<ul>
    {% for comment in comments %}
        {{ render_comment(comment) }}
    {% endfor %}
</ul>
```

为了重复使用宏，我们可以将其保存在单独的文件中，然后在需要使用的模板中导入

```jinja2
{% import 'macros.html' as macros %}

<ul>
    {% for comment in comments %}
        {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>
```

需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免重复

```jinja2
{% include 'common.html' %}
```

### 模板继承

- 基模板:  base.html

  ```jinja2
  <html>
  <head>
  	{% block head %}
      <title>{% block title %}{% endblock %} - My Application</title>
      {% endblock %}
  </head>
  <body>
      {% block body %}
      {% endblock %}
  </body>
  </html>
  ```

- block 标签定义的元素可在衍生模板中修改

  ```jinja2
  {% extends "base.html" %} # extends
  {% block title %}Index{% endblock %}
  {% block head %}
      {{ super() }} # 使用 super() 获取原来的内容(原模版此处非空)
      <style>
      </style>
  {% endblock %}
  {% block body %}
      <h1>Hello, World!</h1> 
  {% endblock 
  ```

  

### Flask-Bootstrap

安装扩展 `pip install flask-bootstrap`

扩展初始化

```python
from flask_bootstrap import Bootstrap
# ...
bootstrap = Bootstrap(app)
```

初始化 Flask-Bootstrap 之后，可以在程序中使用一个包含所有 Bootstrap 文件的基模板

```python
{% extends "bootstrap/base.html" %}
```

改写user.html

```jinja2
{% extends "bootstrap/base.html" %}

{% block title %}Flasky{% endblock %}

{% block navbar %}
<div class="navbar navbar-inverse" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle"data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">Flasky</a>
        </div>
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/">Home</a></li>
            </ul>
        </div>
    </div>
</div>
{% endblock %}
{% block content %}
<div class="container">
    <div class="page-header">
        <h1>Hello, {{ name }}!</h1>
    </div>
</div>
{% endblock %}
```

效果图

![1611127303938](Flask/1611127303938.png)

> 不过还是感觉直接写html更方便23333

###　自定义错误页面

```python
@app.errorhandler(404) # 404，客户端请求未知页面或路由时显示
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500) # 500，有未处理的异常时显示
def internal_server_error(e):
    return render_template('500.html'), 500
```

### url_for 链接

` url_for()`:使用程序 URL 映射中保存的信息生成 URL

用法: `	 url_for('index')	`=>`/`

生成绝对地址 ` url_for('index', _external=True) ` =>` http://localhost:5000/`

` url_for('user', name='john', _external=True) `=>` http://localhost:5000/user/john`

` url_for('index', page=2) `=> `/?page=2`

### 静态文件

图片、JavaScript 源码文件和 CSS等

调用`url_for('static', filename='css/styles.css', _external=True)`会得到`http://localhost:5000/static/css/styles.css`

使用示例: 

```python
{% block head %}
{{ super() }}
    <link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
    <link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}"type="image/x-icon">
{% endblock %}
```

### Flask-Moment

集成 moment.js到jinja2的一个flask拓展

安装` pip install flask-moment`

初始化:

```python
from flask_moment import Moment
# ...
moment = Moment(app)
```

> Flask-Moment 还依赖 jquery.js ,
>
> Bootstrap 已经引入了 jquery.js，因此只需引入 moment.js 即可

在基模板的 scripts 块中引入这个库

```jinja2
#templates/base.html
{% block scripts %}
    {{ super() }}
    {{ moment.include_moment() }}
{% endblock %}
```

然后

```python
from datetime import datetime
@app.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())
```

```jinja2
# templates/index.html
{% extends "base.html" %}
{% block title %}Flasky{% endblock %}
{% block page_content %}
<div class="page-header">
    <h1>Hello World!</h1>
</div>
<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
<p>That was {{ moment(current_time).fromNow(refresh=True) }}.</p>
{% endblock %}
```

format('LLL') 根据客户端电脑中的时区和区域设置渲染日期和时间

 fromNow() 渲染相对时间戳，而且会随着时间的推移自动刷新显示的时间

效果如图

![1611131969170](Flask/1611131969170.png)

moment.js : http://momentjs.com/docs/#/displaying/

## 第四章 Web表单

> 处理表单可以使用 Flask-WTF 扩展 http://pythonhosted.org/Flask-WTF/
>
> 源自WTForms（http://wtforms.simplecodes.com）

安装 ` pip install flask-wtf `

### 防御CSRF

Flask-WTF 使用secret密钥生成加密令牌，再用令牌验证请求中表单数据的真伪

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string' # 强度就取决于这个密钥
```

> 这个SECRET_KEY密钥是通用的密钥 
>
> Flask伪造session里面也见过这个密钥~

### 表单类

使用 Flask-WTF 时，每个 Web 表单都由一个继承自 Form 的类表示

Form中可包含多个字段, 每个字段都用相应类型的字段对象表示

字段对象可附属一个或多个验证函数

```python
from flask_wtf import Form # Form 基类
from wtforms import StringField, SubmitField # 字段
from wtforms.validators import Required # 验证函数
 
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()]) # validators验证函数列表
    submit = SubmitField('Submit')
```

WTForms支持的HTML标准字段:

![1611214430430](Flask/1611214430430.png)

WTForms 内建的验证函数:

![1611214460940](Flask/1611214460940.png)

将表单渲染为HTML

```html
<form method="POST">
{{ form.hidden_tag() }}
{{ form.name.label }} {{ form.name(id='my-text-field') }} # 指定该字段id属性 id='my-text-field'
{{ form.submit() }}
</form>
```

或者借助Flask-Bootstrap

```python
{% import "bootstrap/wtf.html" as wtf %} # wtf 辅助函数
{{ wtf.quick_form(form) }}
```

```python
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Hello, {% if name %}{{ name }}{% else %}Stranger{% endif %}!</h1>
</div>
	{{ wtf.quick_form(form) }}
{% endblock %}
```

然后在视图函数,实例化出一个NameForm,传给模板

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit(): # 验证表单是否提交
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=name)
```

效果大概就是 输入lonmar

![1611217839671](Flask/1611217839671.png)

### 表单处理

上面的代码就已经包含了这表单处理的功能

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit(): # 验证表单是否提交 
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=name)
```

提交表单后，如果数据能被所有验证函数接受，那么 validate_on_submit() 方法的返回值为 True ，否则返回 False 

> 这个函数的返回值决定是重新渲染表单还是处理表单提交的数据

### 使用url_for和session改善体验

提交表单之后再刷新会这样,影响用户体验

![1611218214155](Flask/1611218214155.png)

可以用下面代码改善

```python
from flask import Flask, render_template, session, redirect, url_for
# ...

# 路由
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))
```

### Flash消息

直接看代码和效果

```python
from flask import Flask, render_template, session, redirect, url_for, flash
# ...
# 路由
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!') # flash
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))
```

然后相应的base.html中要写渲染Flash消息的模板,写在block content里面

模板中使用`get_flashed_messages()`获取 flash消息

```jinja2
{% block content %}
    {#  flash  #}
    <div class="container">
        {% for message in get_flashed_messages() %}
            <div class="alert alert-info">
                <button type="button" class="close" data-dismiss="alert">&times;</button>
                {{ message }}
            </div>
        {% endfor %}
    </div>
	
    <div class="container">
        {% block page_content %}{% endblock %}
    </div>
{% endblock %}
```

效果就是

![1611219092580](Flask/1611219092580.png)



##  第五章 数据库操作

主要是Flask-SQLAlchemy的使用 http://pythonhosted.org/Flask-SQLAlchemy/

这个 Flask 扩展包装了 SQLAlchemy（http://www.sqlalchemy.org/）框架

安装 ` pip install flask-sqlalchemy`

 Flask-SQLAlchemy支持多种数据库, 数据库使用 URL 指定

```
MySQL 			   mysql://username:password@hostname/database
Postgres 		   postgresql://username:password@hostname/database
SQLite(Unix) 	   sqlite:////absolute/path/to/database
SQLite(Windows)    sqlite:///c:/absolute/path/to/database
```

> SQLite 数据库不需要使用服务器，因此不用指定 hostname、username 和password.
>
> URL 中的 database 是硬盘上文件的文件名

程序使用的数据库 URL 必须保存到 Flask 配置对象的 SQLALCHEMY_DATABASE_URI 键中

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/MysqlTest'
```

使用示例: 以 SQLite为例

```python
from flask_sqlalchemy import SQLAlchemy # 导入

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
```

`app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True` => 每次请求结束后都会自动提交数据库中的变动

`db `对象是 `SQLAlchemy `类的实例，表示程序使用的数据库

### 模型

![1611223257517](Flask/1611223257517.png)

```python
class Role(db.Model):
    __tablename__ = 'roles' # 表名
    id = db.Column(db.Integer, primary_key=True) # column 
    name = db.Column(db.String(64), unique=True) # 不允许重复
    
    # __repr__ 返回一个具有可读性的字符串表示模型
    def __repr__(self):
        return '<Role %r>' % self.name
   		
class User(db.Model):
    __tablename__ = 'users' # 表名
    id = db.Column(db.Integer, primary_key=True) # primary_key+True 设置id为主键
    username = db.Column(db.String(64), unique=True, index=True)  # unique=True 该值不允许重复
    
    def __repr__(self):
        return '<User %r>' % self.username
```

`__tablename__` : 类变量, 数据库中所使用的表名

> 如果没有定义` __tablename__ `，Flask-SQLAlchemy 会使用一个默认名字,但是可能不符合命名规范

` db.Column`: 用来实例化为列对象,可选参数如下:

![1611223756150](Flask/1611223756150.png)

常使用的一些列选项

![1611223821115](Flask/1611223821115.png)

> Flask-SQLAlchemy 要求每个模型都要定义主键 ，这一列经常命名为 id 

` __repr()__` : 可用于调试, 测试

### 关系

![1611223257517](Flask/1611223257517.png)

上面只是定义了两张表,但是两张表之间是有一对一关系的

```python
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Role %r>' % self.name
    
    users = db.relationship('User', backref='role')  # 在关系的另一个模型中添加反向引用
   		
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) # 外键 这列的值是 roles 表中行的 id 值
```

> 这个还不太懂=.=,等有时间翻一下官方文档 https://www.osgeo.cn/sqlalchemy/

### 数据库操作

- 创建表

  在python shell中

  ```python
  >>> from hello import db
  >>> db.create_all()
  ```

  会新建一个 data.sqlite 的数据库文件

  如果数据库表已经存在于数据库中，那么 db.create_all()不会重新创建或者更新这个表,需要:

  ```python
  >>> db.drop_all()
  >>> db.create_all()
  ```

  还可以使用Flask-Migrate进行数据库迁移(不会丢失数据)

- 插入数据

  需要先实例化表对象,实例化的时候带着参数,id(主键)由Flask-SQLAlchemy统一管理

  ```python
  from hello import Role, User
  admin_role = Role(name='Admin')
  mod_role = Role(name='Moderator')
  user_role = Role(name='User')
  user_john = User(username='john', role=admin_role)
  user_susan = User(username='susan', role=user_role)
  user_david = User(username='david', role=user_role)
  ```

  通过数据库会话( db.session) 管理对数据库所做的改动

  ```python
  db.session.add(admin_role)
  db.session.add(mod_role)
  db.session.add(user_role)
  db.session.add(user_john)
  db.session.add(user_susan)
  db.session.add(user_david)
  ```

  或者简写为

  ```python
  db.session.add_all([admin_role, mod_role, user_role,user_john, user_susan, user_david])
  ```

  调用 commit() 方法提交会话 => 把对象写入数据库

  ```python
  db.session.commit()
  ```

  > 数据库会话也称为事务

- 修改数据

  ```python
  admin_role.name = 'Administrator'
  db.session.add(admin_role)
  db.session.commit()
  ```

- 删除数据

  ```python
  db.session.delete(mod_role)
  db.session.commit()
  ```

- 查询数据

  Flask-SQLAlchemy 为每个模型类都提供了 query 对象,可以通过这个对象的方法进行查询

  ```python
  Role.query.all() # 查询表中所有数据
  # [<Role u'admin'>, <Role u'Moderator'>, <Role u'User'>]
  
  User.query.filter_by(role=user_role).all() # filter_by()过滤器
  # [<User u'susan'>, <User u'david'>]
  ```

  查看原生的sql语句

  ```sql
  >>> str(User.query.filter_by(role=user_role))
  'SELECT users.id AS users_id, users.username AS users_username, users.role_id AS users_role_id \nFROM users \nWHERE ? = users.role_id'
  ```

  退出shell后.再重新进入

  ```python
  from hello import Role
  user_role = Role.query.filter_by(name='User').first()
  # user_role直接就是一个对象了,不需要再实例化
  ```

  常见过滤器,完整的可以参考http://docs.sqlalchemy.org

  ![1611295414659](Flask/1611295414659.png)

还有一些执行查询的方法

> `Role.query.filter_by(name='User')`
>
> => ` <flask_sqlalchemy.BaseQuery object at 0x000000000338A848>`
>
> `Role.query.filter_by(name='User').all()`
>
> => `[<Role u'User'>]`

![1611295488079](Flask/1611295488079.png)

### 在视图函数操作数据库

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        testUser = User.query.filter_by(username=form.name.data).first()
        if testUser is None:
            testUser = User(username=form.name.data)
            db.session.add(testUser)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
            session['name'] = form.name.data
            form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))
```

### 集成Python shell

让 Flask-Script 的 shell 命令自动导入特定的对象,如db,Role等

```python
from flask_script import Shell, Manager
# ...
manager = Manager(app)
# ...
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
# ...
if __name__ == '__main__':
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.debug = True
    manager.run()
```

然后python hello.py shell

![1611297903445](Flask/1611297903445.png)

### 数据库迁移

SQLAlchemy 的主力开发人员编写了一个迁移框架,Alembic(https://alembic.readthedocs.org/en/latest/index.html)

Flask 程序还可使用 Flask-Migrate(http://flask-migrate.readthedocs.org/en/latest/)扩展

这个扩展对 Alembic 做了轻量级包装，并集成到了 Flask-Script 中

安装 `pip install flask-migrate`

使用:

```python
from flask_migrate import Migrate, MigrateCommand
# ...
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
```

为了导出数据库迁移命令，Flask-Migrate 提供了一个 MigrateCommand 类，可附加到 Flask-Script 的 manager 对象上

`python hello.py db init` 创建迁移仓库,这个命令会创建 migrations 文件夹，所有迁移脚本都存放其中

`python hello.py db migrate -m "initial migration"` 创建迁移脚本

`python hello.py db upgrade` 将迁移应用到数据库

> 没搞懂什么原理,数据库模型做出更改时执行`python hello.py db upgrade`应该就行了

## 第六章 电子邮件

安装 `pip install flask-mail`

使用和配置:

Flask-Mail SMTP服务器的配置

![1611300161723](Flask/1611300161723.png)

书中只给了连接Gmail的SMTP服务的具体使用方法

```python
import os
from flask_mail import Mail
# ...
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
```

然后在系统shell里面设置环境变量(防止信息泄露),只在当前命令行下有效

```python
# linux
export MAIL_USERNAME=<Gmail username>
export MAIL_PASSWORD=<Gmail password>
# Windows 
set MAIL_USERNAME=<Gmail username>
set MAIL_PASSWORD=<Gmail password>
```

QQmail SMTP服务使用: https://blog.csdn.net/qq_28388339/article/details/87898940

qq mail使用: `MAIL_DEFAULT_SENDER/SENDER`和`MAIL_USERNAME`必须保持一致

```python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
app.config['MAIL_SERVER'] = 'smtp.qq.com'   # 邮箱服务器
app.config['MAIL_PORT'] = 465               # 端口
app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
app.config['MAIL_USERNAME'] = 'xxxxxxxxx@qq.com' # qq Mail
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxxxxxxxxxx' # 授权码
app.config['MAIL_DEFAULT_SENDER'] = 'xxxxxxxxx@qq.com'  # 填邮箱，默认发送者
mail = Mail(app)

if __name__ == '__main__':
    msg = Message(subject='Hello World',
                  sender="xxxxxxxxx@qq.com",  # 需要使用默认发送者则不用填
                  recipients=['xxxxxxxxx@qq.com'])
    msg.body = 'sended by flask-email'
    msg.html = '<b>测试Flask发送邮件<b>'
    with app.app_context(): 
        # Flask-Mail 中的 send() 函数使用 current_app ，因此要在激活的程序上下文中执行
        mail.send(msg)
```

- 异步发送电子邮件

```python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)
app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
app.config['MAIL_SERVER'] = 'smtp.qq.com'   # 邮箱服务器
app.config['MAIL_PORT'] = 465               # 端口
app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
app.config['MAIL_USERNAME'] = 'xxxxxxxxx@qq.com' # qq Mail
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxxxxxxxxxx' # 授权码
app.config['MAIL_DEFAULT_SENDER'] = 'xxxxxxxxx@qq.com'  # 填邮箱，默认发送者
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

if __name__ == '__main__':
    msg = Message(subject='Hello World',
                  sender="xxxxxxxxx@qq.com",  # 需要使用默认发送者则不用填
                  recipients=['xxxxxxxxx@qq.com'])
    msg.body = 'sended by flask-email'
    msg.html = '<b>测试Flask发送邮件<b>'
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
```

## 第七章 大型程序的结构

调整一下结构就成下面这样了

```
├─app
│  	│--email.py
│  	│--models.py
│  	│--__init__.py
│  	├─main
│  	│    |--errors.py
│  	│    |--forms.py
│  	│    |--views.py
│  	│    |--__init__.py
│  	├─static
│  	│
│  	└─templates
│      	│--404.html
│      	│--index.html
|	    | ... 省略一些
│      	└─mail
│             |--new_user.html
│             |--new_user.txt
│--config.py
│--manage.py
├─tests
│     |--test_basics.py
│     |--__init__.py
│--data-dev.sqlite
│--data-test.sqlite
│--data.sqlite
│--requirements.txt
│--tree.txt
├─migrations
├─venv
└─.idea
```

最主要的就是app文件夹,然后config.py是配置文件,manage.py是启动管理文件

tests文件夹里面是测试文件

然后还要数据库文件等等.

分析一下这个结构

### 配置选项的改动

配置选项集成到了一个文件config.py, 下面是代码

```python
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# 层次结构的配置类
# 基类 Config 通用配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'

    FLASKY_MAIL_SENDER = 'xxxxxxxx@xx.com'
    FLASKY_ADMIN = 'xxxxxxx@xx.com'

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'xxxxxxxx@xx.com'
    MAIL_PASSWORD = 'xxxxxxxxxxxxxxxx'

    @staticmethod
    def init_app(app):  # 参数是程序实例
        pass            # 可以执行对当前环境的配置初始化

# 开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

# 测试环境配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                'sqlite:///' + os.path.join(basedir, 'data.sqlite')
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

​	一种配置写成一种类,有基类Config,然后别的配置类安装需求由基类派生出来

​	值得注意的是配置基类中有一个init_app()方法.这个方法在app工厂里面用来初始化扩展

### 然后是最主要的app包

里面集成了static静态文件, templates模板文件(里面有一个mail文件夹放着mail模板)

然后为了更改配置,使用工厂函数.在`app/__init.py__` 中定义.内容如下

```python
# encoding=utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]) # 加载配置文件
    config[config_name].init_app(app)

    # init_app
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 附加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app  # 工厂函数返回创建的程序示例
```

在这里面集成和初始化Flask的扩展.返回一个实例化对象.

主要函数就是`create_app()` , 同时还要在里面注册蓝本,来导入路由等

> 然而并没看懂哪里有优势了,更难懂了.其中部分代码还不是很理解.后面再看

### 路由-蓝本

然后在一个叫蓝本里面的东西定义路由之类的.需要在一个包里面.就是结构中的main文件夹

然后在 `app/main/__init__.py` 初始化这个蓝本

```python
# -*- coding: utf-8 -*-
from flask import Blueprint
# 通过实例化一个 Blueprint 类对象创建蓝本
main = Blueprint('main', __name__)
# 两个参数 蓝本的名字和蓝本所在的包或模块
# 一定要在最后导入,否则可能循环导入
from . import views, errors # 导入路由和错误处理的路由
```

然后views.py 就是一些视图函数.

```python
# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app
# . 是当前路径, ..就是上一级路径
from .. import db # 引入app/__init__下的数据库对象
from ..models import User # User类
from ..email import send_email # send_email函数
from . import main # 引入整个蓝本
from .forms import NameForm # 引入Form类
from datetime import datetime

# main.route
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
		# Flask 会为蓝本中的全部端点加上一个命名空间,命名空间就是蓝本的名字
        return redirect(url_for('.index'))
		#  url_for('main.index')或者胜利main url_for('.index')
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
```

errors.py

```python
# -*- coding: utf-8 -*-
from flask import render_template
from . import main

#@main.app_errorhandler
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

这里使用的是`@main.app_errorhandler`而不是 `@main.errorhandler`

` errorhandler`:只处理蓝本里面的错误

`app_errorhandler`:处理全局错误

然后不知道forms.py为啥也在蓝本

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
```

### 启动脚本

```python
# -*- coding: utf-8 -*-
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

### Other

- requirements.txt可以用这条命令生成`pip freeze >requirements.txt`

-  `pip install -r requirements.txt`

- 单元测试,书中给了如下的代码,讲解也很少

```python
import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
```

使用 unittest 包编写 https://docs.python.org/2/library/unittest.html

 setUp() 和 tearDown() 方法分别在各测试前后运行

以 test_ 开头的函数都作为测试执行 

然后书中给了在manger.py里面编写测试函数的示例

```python
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
```

### 值得注意的引用

一些比较重要的各个文件直接的交叉引用

蓝本里面`app/main/__init__.py` 会引用views和errors

```python
from . import views, errors
```

views和errors又会引用蓝本`app/main/__init__.py` 

```python
from . import main
```

然后就基本用到什么就导入什么,只是这种导入还不习惯.

```python
from . import xxx
from .xxx import xxx
from ..xxx import xxx
```

> 基础知识就到这
>
> 整个代码打包放在了GitHub. https://github.com/L0nm4r/FlaskLearn

