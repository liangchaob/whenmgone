# coding: utf-8  
# 导入pymongo模块
import pymongo
# 设置数据库地址
client = pymongo.MongoClient('172.16.191.163', 27017)
# 设置数据库名
db = client['demodb']
# 设置表名
collection = db['demotable']

# userID = 'liangchaob'
# password = 'P@ssw0rd'
# name = '良朝'
# phone = '18600295379'
# content01 = '快到碗里来'
# content02 = '别相信他'
# heatbeatmail = 'liangchaob@163.com'
# heatbeatrate = '7day'
# heatbeatdelay = '3day'
# heatbeatUpdate = '20151211'
# heatbeatSync = '20151218'
# heatbeatFinal = '20151221'

# demo_data = {
#         'userID':userID,
#         'password':password,
#         'name':name, 
#         'phone':phone, 
#         'note01':{
#             'content':content01,
#             'link':['content01','content02']
#             },
#         'note02':{
#             'content':content02,
#             'link':['content03']
#             },
#         'contact01':{
#             'mail':'hehe@126.com',
#             'phone':'13821647463',
#             'name':'小白'
#             },
#         'contact02':{
#             'mail':'haha@126.com',
#             'phone':'13821647464',
#             'name':'小黑'
#             },
#         'contact03':{
#             'mail':'keke@126.com',
#             'phone':'13821647465',
#             'name':'无常'
#             },
#         'heatbeatMail':heatbeatmail,
#         'heatbeatRate':heatbeatrate,
#         'heatbeatDelay':heatbeatdelay,
#         'heatbeatUpdate':heatbeatUpdate,
#         'heatbeatSync':heatbeatSync,
#         'heatbeatFinal':heatbeatFinal,
#         'deathConfirm':False,
#         'notesendConfirm':False,
#         'serviceState':True
#     }
# collection.insert_one(demo_data)


# today = 14
# # 筛选出应该发同步邮件的人
# for i in collection.find({"heatbeatSync":{"$lte":today},"heatbeatFinal":{"$gte":today}},{'userID':1,'name':1}):
#     print i.get('name')

# ftoday = 50
# # 筛选出应该发遗嘱邮件的人
# for i in collection.find({"heatbeatFinal":{"$lte":ftoday}},{'userID':1,'name':1}):
#     print i.get('name')




#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from datetime import datetime,timedelta

now = datetime.now()

yestoday = now - timedelta(days=1)
tommorow = now + timedelta(days=1)

next_year = now + timedelta(days = 365)
last_year = now - timedelta(days = 365)

print yestoday

print tommorow

print next_year
print last_year

# a = "Sat Mar 28 22:24:24 2009"

# a = time.strftime("%Y-%m-%d %H:%M:%S")

# b = time.mktime(time.strptime(a,"%Y-%m-%d %H:%M:%S"))

# print a
# print b

# a = time.time()


# 导入时间模块
import time

# 获取当前时刻时间戳
timenow = time.time()

# 定义查询时间函数,获取
livecheck = collection.find({"heatbeatSync":{"$lte":timenow},"heatbeatFinal":{"$gte":timenow}},{'userID':1,'name':1,'heatbeatmail':1})

# 显示查询结果
print livecheck

for i in livecheck:
    userID = i.get('userID')
    name = i.get('name')
    mailaddr = i.get('heatbeatmail')
    livecheck(userID,name,mailaddr)




# 邮件相关
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib


# 邮件服务测试
def livecheck_mail(userID,name,mailaddr):

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    from_addr = 'whenmgonetest'
    password = 'P@ssw0rdP@ssw0rd'
    to_addr = mailaddr
    smtp_server = 'smtp.163.com'

    msg = MIMEText('<h2>亲爱的' + name + '，whenmgone向您个安！</h2>' 
        + '\n' + '<form action="#" method="POST"><button type="submit">平身罢</button></form>',
         'html',  'utf-8')
    msg['From'] = _format_addr('whenmgone <%s>' % from_addr)
    msg['To'] = _format_addr(name + ' <%s>' % to_addr)
    msg['Subject'] = Header('whenmgone定期心跳', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()




