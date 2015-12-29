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
from wtforms.validators import DataRequired,Email,Length,EqualTo

# 引入密码哈希加密
from werkzeug.security import generate_password_hash,check_password_hash




# 创建一个Flask对象
app = Flask(__name__)

# 使用bootstrap初始化
bootstrap = Bootstrap(app)


# app.config.update(
#     BOOTSTRAP_USE_CDN = False
# )
app.config.setdefault('BOOTSTRAP_USE_CDN', False)



# 设置跨站请求伪造保护
app.config['SECRET_KEY'] = 'hard to guess string'


# 设置数据库地址
client = pymongo.MongoClient('172.16.191.163', 27017)
# 设置数据库名
db = client['demodb']
# 设置表名
collection = db['demotable']


# # 创建demo表单类
# class DemoForm(Form):
#     # 用户注册id名
#     userID = TextField('用户名', validators = [DataRequired()])
#     # 密码输入框
#     password = PasswordField('密码',validators = [Length(min = 8, max = 40)])
#     # 用户名输入框
#     name = TextField('真实姓名', validators = [DataRequired()])
#     # 用户手机输入框
#     phone = TextField('手机', validators = [DataRequired()])
#     # 遗书输入框
#     content01 = TextAreaField('留言1', validators = [DataRequired()])
#     # content02 = TextAreaField('留言2', validators = [DataRequired()])
#     # 接收人输入框
#     contact01Name = TextField('接收人1姓名', validators = [DataRequired()])
#     contact01Mail = TextField('接收人1邮箱', validators = [DataRequired()])
#     contact01Phone = TextField('接收人1电话', validators = [DataRequired()])

#     # contact02Name = TextField('接收人2姓名', validators = [DataRequired()])
#     # contact02Mail = TextField('接收人2邮箱', validators = [DataRequired()])
#     # contact02Phone = TextField('接收人2电话', validators = [DataRequired()])

#     # contact03Name = TextField('接收人3姓名', validators = [DataRequired()])
#     # contact03Mail = TextField('接收人3邮箱', validators = [DataRequired()])
#     # contact03Phone = TextField('接收人3电话', validators = [DataRequired()])
  
#     # 心跳邮箱
#     heatbeatmail = TextField('心跳邮箱', validators = [Email()])
#     # 心跳频率
#     rate_choices = [('7', '每周'), ('30', '每月'), ('90', '每3个月')]
#     heatbeatrate = SelectField('心跳频率',choices = rate_choices, default = '30')
#     # 心跳延迟
#     delay_choices = [('7', '1周后'), ('30', '1个月后'), ('90', '3个月后')]
#     heatbeatdelay = SelectField('心跳延迟',choices = delay_choices, default = '30')
#     # 最后更新时间



# 设置时间计算模块儿
class TimeCompute(object):
    """用于计算遗书服务更新时间"""
    # 初始化模块儿参数心跳频率和时间时间
    def __init__(self, heatbeatrate,heatbeatdelay):
        self.heatbeatrate = heatbeatrate
        self.heatbeatdelay = heatbeatdelay
        self.timenow = datetime.now()
    # 最后更新时间戳
    def heatbeatUpdate(self):
        return time.mktime(self.timenow.timetuple())
    # 下次同步时间戳
    def heatbeatSync(self):
        _timesync = self.timenow + timedelta(days=self.heatbeatrate)
        return time.mktime(_timesync.timetuple())
    # 最晚延时时间戳
    def heatbeatFinal(self):
        _timefinal = self.timenow + timedelta(days=self.heatbeatrate+self.heatbeatdelay)
        # _timefinal = _timenow + timedelta(days=heatbeatdelay)
        return time.mktime(_timefinal.timetuple())
        


# # 用户表单
# @app.route('/', methods=('GET', 'POST'))
# # 定义响应函数
# def index():
#     # 实例化表单类
#     form = DemoForm()
#     # 如果接收到post提交
#     if request.method == 'POST':
#         userID = request.form['userID']
#         password = request.form['password']
#         name = request.form['name']
#         phone = request.form['phone']
#         content01 = request.form['content01']
#         # content02 = request.form['content02']
#         contact01Mail = request.form['contact01Mail']
#         contact01Phone = request.form['contact01Phone']
#         contact01Name = request.form['contact01Name']

#         # contact02Mail = request.form['contact02Mail']
#         # contact02Phone = request.form['contact02Phone']
#         # contact02Name = request.form['contact02Name']

#         # contact03Mail = request.form['contact03Mail']
#         # contact03Phone = request.form['contact03Phone']
#         # contact03Name = request.form['contact03Name']

#         heatbeatmail = request.form['heatbeatmail']
#         heatbeatrate = request.form['heatbeatrate']
#         heatbeatdelay = request.form['heatbeatdelay']
#         # heatbeatUpdate = str(time.strftime("%Y-%m-%d %H:%M:%S"))
#         # heatbeatSync = str(time.strftime("%Y-%m-%d %H:%M:%S")) + 'heatbeatrate'
#         # heatbeatFinal = str(time.strftime("%Y-%m-%d %H:%M:%S")) + 'heatbeatrate' + 'heatbeatdelay'
#         heatbeatrate=int(heatbeatrate)
#         heatbeatdelay=int(heatbeatdelay)

#         T = TimeCompute(heatbeatrate,heatbeatdelay)

#         # 设置插入数据库的内容
#         demo_data = {
#         'userID':userID,
#         'password':password,
#         'name':name, 
#         'phone':phone, 
#         'note01':{
#             'content':content01,
#             'link':['content01']
#             },
#         # 'note02':{
#         #     'content':content02,
#         #     'link':['content03']
#         #     },
#         'contact01':{
#             'mail':contact01Mail,
#             'phone':contact01Phone,
#             'name':contact01Name
#             },
#         # 'contact02':{
#         #     'mail':contact02Mail,
#         #     'phone':contact02Phone,
#         #     'name':contact02Name
#         #     },
#         # 'contact03':{
#         #     'mail':contact03Mail,
#         #     'phone':contact03Phone,
#         #     'name':contact03Name
#         #     },
#         'heatbeatMail':heatbeatmail,
#         'heatbeatRate':heatbeatrate,
#         'heatbeatDelay':heatbeatdelay,
#         'heatbeatUpdate':T.heatbeatUpdate(),
#         'heatbeatSync':T.heatbeatSync(),
#         'heatbeatFinal':T.heatbeatFinal(),
#         'deathConfirm':False,
#         'notesendConfirm':False,
#         'serviceState':True
#         }
#         # 插入数据
#         collection.insert_one(demo_data)
#         # 重定向回来
#         return redirect('/')
#     # 渲染demo_index.html
#     return render_template('demo_index.html', form=form)

# # 用户遗嘱
# @app.route('/profile/<name>')
# # 定义响应函数
# def note_content(name):
#     # 实例化表单类
#     form = DemoForm()
#     # 找到名字对应的内容
#     content = collection.find_one({'userID':name}).get('note01.content')
#     # 渲染demo_index.html
#     return render_template('content.html', note = content)





# 关于用户的会话在线

# 引入flask-login
from flask.ext.login import LoginManager
from flask.ext.login import UserMixin, current_user, login_required, login_user, logout_user

login_manager = LoginManager()
login_manager.setup_app(app)



class User():
    def __init__(self, email=None):
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.email)

@login_manager.user_loader
def load_user(email):
    u = collection.find_one({'email_address':email})
    if not u:
        return None
    return User(u['email_address'])




# 用户登录
class UserLogin(Form):
    """用户登录表单"""
    # 邮箱
    email_address = TextField('常用邮箱', validators = [Email()])
    # 密码
    password = PasswordField('密码',validators = [DataRequired()])
    # 提交
    submit = SubmitField('登录')

# 用户遗嘱首页
@app.route('/login', methods=('GET', 'POST'))
# 定义响应函数
def logintest():
# 实例化表单类
    form = UserLogin()
    # 如果接收到post提交
    if request.method == 'POST':
        # 拿用户名找密码
        # testname = collection.find_one({'email_address':form.email_address.data})
        # testname = collection.find_one({'email_address':'haha@123.com'})
        user_obj = collection.find_one({'email_address':form.email_address.data})
        if user_obj == None:
            message = '账户不存在！'
            return render_template('login.html', form=form, message=message)
            print yes
        else:
            password_hash = user_obj.get('password')
            # 验证登录
            if check_password_hash(password_hash,form.password.data) == True:
                # 将得到的用户名加入使用login实例化
                login_obj = load_user(form.email_address.data)
                # 使用login函数载入用户
                login_user(login_obj)
                # 带着用户名参数重定向到指定页面
                return redirect('/contact')
            else:
                message = '用户名或密码错误！'
                print message
                return render_template('login.html', form=form, message=message)
    # 渲染demo_index.html
    return render_template('login.html', form=form)




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

# 用户遗嘱注册
@app.route('/register', methods=('GET', 'POST'))
# 定义响应函数
def registertest():
# 实例化表单类
    form = UserRegister()
    # 如果接收到post提交
    if request.method == 'POST':
        # 密码加密
        password = generate_password_hash(form.password.data)
        # 设置插入数据库的内容
        db_update = {
        'email_address':form.email_address.data,
        'password':password,
        'name':form.name.data, 
        'phone':form.phone.data, 
        'deathConfirm':False,
        'notesendConfirm':False,
        'serviceState':True
        }
        # 插入数据
        collection.insert_one(db_update)
        # 重定向回来
        return redirect('/login')
    # 渲染demo_index.html
    return render_template('register.html', form=form)




# 用户注册
class UserContact(Form):
    """用户注册表单"""
    # 邮箱
    contact01Mail = TextField('常用邮箱', validators = [Email()])
    # 用户名输入框
    contact01Name = TextField('姓名', validators = [DataRequired()])
    # 用户手机输入框
    contact01Phone = TextField('手机', validators = [DataRequired()])
    # 提交
    submit = SubmitField('提交')


# 联系人step
@app.route('/contact', methods=('GET', 'POST'))
# 需要login登录修饰
@login_required
# 定义响应函数
def contacttest():
    # 实例化表单类
    form = UserContact()
    # 如果接收到post提交
    if request.method == 'POST':
        # 更新添加联系人数据
        collection.update({'email_address':current_user.email },
            {
                "$set":{
                    'contact01':{
                            'mail':form.contact01Mail.data,
                            'phone':form.contact01Phone.data,
                            'name':form.contact01Name.data
                    },
                }
            }
        )
        # 重定向回来
        return redirect('/contact')
    # 渲染demo_index.html
    return render_template('contact.html', form=form)










# 遗嘱step
@app.route('/lastwill')
# 需要login登录修饰
@login_required
# 定义响应函数
def lastwilltest():
    # 渲染index.html
    return render_template('lastwill.html')


# 心跳设置step
@app.route('/heatbeat')
# 需要login登录修饰
@login_required
# 定义响应函数
def heatbeattest():
    # 渲染index.html
    return render_template('heatbeat.html')





# 预览step
@app.route('/preview')
# 需要login登录修饰
@login_required
# 定义响应函数
def previewtest():
    # preview.html
    return render_template('preview.html')


# 最终展示step
@app.route('/noteshow')
# 定义响应函数
def noteshowtest():
    # 渲染noteshow.html
    return render_template('noteshow.html')







# 运行主函数
if __name__ == '__main__':
    # 对外开放80端口
    app.run(host='0.0.0.0',port=8080,debug=True)

