# -*- coding: UTF-8 -*-
'''
* 用于whenmgone的demo原型测试(时间计算)
* liangchaob@163.com 
* 2015.12.5
'''
# 引入os模块
import os
# 引入time模块
import time
# 引入sys模块，并将默认字符格式转为utf-8
from datetime import datetime,timedelta
# 引入datatime模块

class TimeCompute(object):
    """docstring for TimeCompute"""
    def __init__(self, heatbeatrate,heatbeatdelay):
        self.heatbeatrate = heatbeatrate
        self.heatbeatdelay = heatbeatdelay
        self.timenow = datetime.now()
    def heatbeatUpdate(self):
        return time.mktime(self.timenow.timetuple())
    def heatbeatSync(self):
        _timesync = self.timenow + timedelta(days=self.heatbeatrate)
        return time.mktime(_timesync.timetuple())
    def heatbeatFinal(self):
        _timefinal = self.timenow + timedelta(days=self.heatbeatrate+self.heatbeatdelay)
        # _timefinal = _timenow + timedelta(days=heatbeatdelay)
        return time.mktime(_timefinal.timetuple())

a=TimeCompute(7,7)
print a.heatbeatUpdate()
print a.heatbeatSync()
print a.heatbeatFinal()