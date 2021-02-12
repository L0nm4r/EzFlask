## Werkzeug=>Hash
- 使用Werkzeug实现密码散列: Werkzeug 中的 security 模块能够很方便地实现密码散列值的计算

usage:
- generate_password_hash(password,method=pbkdf2:sha1,salt_length=8) //create hash
- check_password_hash(hash, password) //check hash

```python
# UserModel
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin, db.Model):
  __tablename__ = 'users'
  password_hash = db.Column(db.String(128))

  # ...
  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  # ...
```
## Flask-Login

**Flask-Login 初始化**

Flask-Login 在程序的工厂函数中初始化  `app/__init__.py`:

```python
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong' # 保护等级 None/'basic'/'strong' 
# Flask-Login 会记录客户端 IP 地址和浏览器的用户代理信息,如果发现异动就登出用户
login_manager.login_view = 'auth.login'

def create_app(config_name):
  ...
  login_manager.init_app(app)
  ...
```

**导入**

在Models里面 app/models.py

```python
from . import login_manager

@login_manager.user_loader # callback function
def load_user(user_id):   # 使用指定的标识符(Unicode)加载用户
  return User.query.get(int(user_id))
  # return none/用户对象
```

**登录认证**

methods:
- is_authenticated() 如果用户已经登录，必须返回 True ，否则返回 False
- is_active() 如果允许用户登录，必须返回 True ，否则返回 False 。如果要禁用账户，可以返回 False
- is_anonymous() 对普通用户必须返回 False
- get_id() 必须返回用户的唯一标识符，使用 Unicode 编码字符串

可以让UserModel继承Flask-Login的UserMixin类,这个类实现了上面四个方法

```python
# UserModel
from flask_login import UserMixin
class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(64), unique=True, index=True)
  username = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String(128))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

**访问控制**

@login_required =>只让认证用户访问
```python
from flask_login import login_required
@app.route('/secret')
@login_required
def secret():
  return 'Only authenticated users are allowed!'
```

## itsdangerous => Create Token

使用  TimedJSONWebSignatureSerializer 生成具有过期时间的 JSON Web 签名

这个类的构造函数接收的参数是一个密钥,在 Flask 程序中可使用 SECRET_KEY 设置

dumps() 方法为指定的数据生成一个加密签名，然后再对数据和签名进行序列化，生成令牌字符串

expires_in 参数设置令牌的过期时间,单位为秒

为了解码令牌,序列化对象提供了 loads() 方法,其唯一的参数是令牌字符串

usage:
```python
from manage import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 生成token
s = Serializer(app.config['SECRET_KEY'], expires_in = 3600) 
token = s.dumps({ 'confirm': 123456 })

# 解密token
data = s.loads(token) # {u'confirm': 123456}
```

邮箱验证:激活用户,确认信息等
```python
class User(UserMixin, db.Model):
  def generate_confirmation_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'confirm': self.id})
  def confirm(self, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
    except:
      return False
    if data.get('confirm') != self.id:
      return False
    self.confirmed = True
    db.session.add(self)
    return True
```


## MarkDown

two options 
- Flask-PageDown ` pip install flask-pagedown markdown bleach`
- flask-misaka https://flask-misaka.readthedocs.io/en/latest/

some problems for flask-misaka https://my.oschina.net/zbfree/blog/2051989

