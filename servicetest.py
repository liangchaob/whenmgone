# coding: utf-8  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 邮件服务测试
def service_test(name,usermail,note,contact,contactmail,heatbeatUpdate):
    content = '您好，这是一封网络遗嘱服务邮件，受到' + name + '的委托' + '代他发送给您的留言如下：' + '\n' + note

    from_addr = raw_input('enter mailaddr:')
    password = raw_input('enter password:')
    to_addr = contactmail
    smtp_server = 'smtp.163.com'

    msg = MIMEText('<html><body><h1>whenmgone网络遗书</h1>' +
        '<p>' + content + '</p>' +
        '</body></html>', 'html',  'utf-8')
    msg['From'] = _format_addr('whenmgone网络遗书服务 <%s>' % from_addr)
    msg['To'] = _format_addr(contact + ' <%s>' % to_addr)
    msg['Subject'] = Header('来自' + name +'先生的遗嘱', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


name = '良朝'
usermail = 'liangchaob'
note = '快进到我的碗里来'
contact = '小冷'
contactmail = 'idk2idk2@126.com'
heatbeatUpdate = 12

service_test(name,usermail,note,contact,contactmail,heatbeatUpdate)
