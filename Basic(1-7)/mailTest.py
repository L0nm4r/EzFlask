# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_mail import Mail, Message
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


app = Flask(__name__)
app.config['MAIL_DEBUG'] = True  # 开启debug，便于调试看信息
app.config['MAIL_SUPPRESS_SEND'] = False  # 发送邮件，为True则不发送
app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 邮箱服务器
app.config['MAIL_PORT'] = 465  # 端口
app.config['MAIL_USE_SSL'] = True  # 重要，qq邮箱需要使用SSL
app.config['MAIL_USE_TLS'] = False  # 不需要使用TLS
app.config['MAIL_USERNAME'] = 'xxxxxxxxxxx@qq.com'
app.config['MAIL_PASSWORD'] = 'xxxxxxxxxx' # 授权码
app.config['MAIL_DEFAULT_SENDER'] = 'xxxxxxxxxxx@qq.com'  # 填邮箱，默认发送者
mail = Mail(app)

if __name__ == '__main__':
    msg = Message(subject='Hello World',
                  sender="xxxxxxxxxxxx@qq.com",  # 需要使用默认发送者则不用填
                  recipients=['xxxxxxxxxxxxxx@qq.com'])
    msg.body = 'sended by flask-email'
    msg.html = '<b>测试Flask发送邮件<b>'
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
