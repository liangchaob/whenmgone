# -*- coding: UTF-8 -*-
'''
* 用于whenmgone的demo原型测试
* liangchaob@163.com 
* 2015.12.5
'''
# 引入os模块
import os
# 引入time模块
import time
# 引入datatime模块
from datetime import datetime,timedelta

# 引入sys模块，并将默认字符格式转为utf-8
import sys
sys.path.append("./")
reload(sys)
sys.setdefaultencoding( "utf-8" )

# 导入pymongo模块
import pymongo

# 引入flask模块
from flask import Flask, render_template, redirect, request
# 引入flask-bootstrap模块
from flask.ext.bootstrap import Bootstrap

# 引入flask-WTF模块
from flask_wtf import Form
# 引入文本字段、密码字段、多行文本字段、下拉列表字段
from wtforms import TextField,PasswordField,TextAreaField,SelectField,SubmitField
# 引入验证字段中的require、email
from wtforms.validators import DataRequired,Email,EqualTo


# 用户注册
class UserRegister(Form):
    """用户注册表单"""
    # 邮箱
    email_address = TextField('常用邮箱', validators = [Email()])
    # 密码
    password = PasswordField('密码',validators = [DataRequired(),EqualTo('password_repeat',message = '两次输入不匹配')])
    # 重复密码
    password_repeat = PasswordField('重复密码',validators = [DataRequired()])
    # 用户名输入框
    name = TextField('真实姓名', validators = [DataRequired()])
    # 用户手机输入框
    phone = TextField('手机', validators = [DataRequired()])
    # 提交
    submit = SubmitField('提交')


