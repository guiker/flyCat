#!/usr/bin/env python3
#===================================
# @Version:
# @Author:guiker
# @Create Time:09:32 29/04/2018
# @File Name:log.py
# @Description:
#
#===================================
import flyCat.config as config
import time
'''
log有四种等级：
宽松：REDUCED
正常：NORMAL
严格：TIGHTENED
完全不显示：NO
'''
def msg(level,msg,save=False):
    levels={}
    levels['no']        = 0
    levels['tightened'] = 1
    levels['normal']    = 2
    levels['reduced']   = 3
    now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    try:
        if levels[config.Config['msg_level']] >= levels[level]:
            print(now_time + '   ' + msg)
    except:
        print(u'消息显示错误，请检查config.py文件....')

