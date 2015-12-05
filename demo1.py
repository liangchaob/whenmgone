# -*- coding: UTF-8 -*-
'''
* 用于whenmgone的demo原型测试
* liangchaob@163.com 
* 2015.12.5
'''
# 引入os模块
import os
# 引入datatime模块
import time
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
from wtforms import TextField,PasswordField,TextAreaField,SelectField
# 引入验证字段中的require、email
from wtforms.validators import DataRequired,Email,Length




# 创建一个Flask对象
app = Flask(__name__)

# 使用bootstrap初始化
bootstrap = Bootstrap(app)

# 设置跨站请求伪造保护
app.config['SECRET_KEY'] = 'hard to guess string'


# 设置数据库地址
client = pymongo.MongoClient('172.16.191.163', 27017)
# 设置数据库名
db = client['demodb']
# 设置表名
collection = db['demotable']


# 创建demo表单类
class DemoForm(Form):
    # 用户名输入框
    name = TextField('姓名', validators = [DataRequired()])
    # 密码输入框
    password = PasswordField('密码',validators = [Length(min = 8, max = 40)])
    # 遗书输入框
    note = TextAreaField('留言', validators = [DataRequired()])
    # 接收人输入框
    reciver = TextField('接收人', validators = [DataRequired()])
    # 心跳邮箱
    heatbeatmail = TextField('心跳邮箱', validators = [Email()])
    # 心跳频率
    rate_choices = [('1', '每周'), ('2', '每月'), ('3', '每3个月')]
    heatbeatrate = SelectField('心跳频率',choices = rate_choices, default = '2')
    # 心跳延迟
    delay_choices = [('1', '1周后'), ('2', '1个月后'), ('3', '3个月后')]
    heatbeatdelay = SelectField('心跳延迟',choices = delay_choices, default = '2')


        



# 指定路由
@app.route('/', methods=('GET', 'POST'))
# 定义响应函数
def index():
    # 实例化表单类
    form = DemoForm()
    # 如果接收到post提交
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        note = request.form['note']
        reciver = request.form['reciver']
        heatbeatmail = request.form['heatbeatmail']
        heatbeatrate = request.form['heatbeatrate']
        heatbeatdelay = request.form['heatbeatdelay']
        # 设置插入数据库的内容
        demo_data = {'name':name,'password':password,'note':note,'reciver':reciver,'heatbeatmail':heatbeatmail,'heatbeatrate':heatbeatrate,'heatbeatdelay':heatbeatdelay}
        # 插入数据
        collection.insert_one(demo_data)
        # 重定向回来
        return redirect('/')
    # 渲染index.html
    return render_template('index.html', form=form)

# 指定路由
@app.route('/<name>')
# 定义响应函数
def note_content(name):
    # 实例化表单类
    form = DemoForm()
    # 找到名字对应的内容
    content = collection.find_one({'name':name}).get('note')
    # 渲染index.html
    return render_template('content.html', note = content)


# 运行主函数
if __name__ == '__main__':
    # 对外开放80端口
    app.run(host='0.0.0.0',port=8080,debug=True)
