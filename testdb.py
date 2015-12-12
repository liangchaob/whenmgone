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


today = 14
# 筛选出应该发同步邮件的人
for i in collection.find({"heatbeatSync":{"$lte":today},"heatbeatFinal":{"$gte":today}},{'userID':1,'name':1}):
    print i

ftoday = 50
# 筛选出应该发遗嘱邮件的人
for i in collection.find({"heatbeatFinal":{"$lte":ftoday}},{'userID':1,'name':1}):
    print i
