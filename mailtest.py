# coding: utf-8  
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = raw_input('enter mailaddr:')
password = raw_input('enter password:')
to_addr = 'idk2idk2@126.com'
smtp_server = 'smtp.163.com'

msg = MIMEText('<html><body><h1>whenmgone网络遗书</h1>' +
    '<p>send by <a href="http://www.python.org">whenmgone.com</a>...</p>' +
    '</body></html>', 'html',  'utf-8')
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

