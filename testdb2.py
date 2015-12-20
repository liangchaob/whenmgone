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
# 引入datatime模块
from datetime import datetime,timedelta

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

# 时间计算用例
a=TimeCompute(7,7)
print a.heatbeatUpdate()
print a.heatbeatSync()
print a.heatbeatFinal()