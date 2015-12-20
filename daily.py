# -*- coding: UTF-8 -*-
# 引入sys模块，并将默认字符格式转为utf-8
import sys
sys.path.append("./")
reload(sys)
sys.setdefaultencoding( "utf-8" )

# 邮件相关
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib



# 邮件服务测试——心跳检测
def livecheck_mail(userID,name,mailaddr):

    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    from_addr = 'whenmgonetest@163.com'
    password = 'awhhatnazgnrjsya'
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


# 邮件服务测试——遗嘱发送
def notesend_mail(userID,name,contactname,mailaddr):

    def _format_addr(s):
        contactname, addr = parseaddr(s)
        return formataddr((Header(contactname, 'utf-8').encode(), addr))

    from_addr = 'whenmgonetest@163.com'
    password = 'awhhatnazgnrjsya'
    to_addr = mailaddr
    smtp_server = 'smtp.163.com'

    msg = MIMEText('<h2>' + contactname + '：<br>您好，我们受 <b>' + name +'</b> 委托，向您发送他最后的留言，请点击如下链接进行查收！</h2>' 
        + '\n' + '<form action="#" method="POST"><button type="submit">留言</button></form>',
         'html',  'utf-8')
    msg['From'] = _format_addr('whenmgone <%s>' % from_addr)
    msg['To'] = _format_addr(contactname + ' <%s>' % to_addr)
    msg['Subject'] = Header('whenmgone网络遗嘱', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()





# 导入pymongo模块
import pymongo
# 设置数据库地址
client = pymongo.MongoClient('172.16.191.163', 27017)
# 设置数据库名
db = client['demodb']
# 设置表名
collection = db['demotable']

# 导入时间模块
import time

# 获取当前时刻时间戳
timenow = time.time()

# 获取所有的该发送定时心跳的对象
livecheck = collection.find({"heatbeatSync":{"$lte":timenow},"heatbeatFinal":{"$gte":timenow}},{'userID':1,'name':1,'heatbeatmail':1})

# 获取所有的该发送遗嘱的对象
deathcheck = collection.find({"heatbeatFinal":{"$lte":timenow}},{'userID':1,'name':1,'heatbeatMail':1,'contact01':1})


# 检查心跳并发送主循环
for i in livecheck:
    userID = i.get('userID')
    name = i.get('name')
    mailaddr = i.get('heatbeatMail')
    print userID,name,mailaddr
    livecheck_mail(userID,name,mailaddr)

# 检查无回应并发送主循环
for i in deathcheck:
    userID = i.get('userID')
    name = i.get('name')
    mailaddr = i.get('heatbeatMail')
    contact01 = i.get('contact01').get('name')
    print userID,name,mailaddr,contact01
    notesend_mail(userID,name,contact01,mailaddr)



