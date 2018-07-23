#!/usr/bin/env python3
#===================================
# @Version:0.1 Beta
# @Author:guiker
# @Create Time:04:50 01/05/2018
# @File Name:spider_plug.py
# @Description:
# 解析器插件
#===================================
import re
import flyCat.config as config
import os
#==============#
# 载入HTML文件 #
#==============#
def load(name):
    path = config.Config['cache_path'] + 'html/'
    files=os.listdir(path+name)
    for html_file in files:
        with open(path + name + '/' + html_file,'r',encoding='UTF-8') as f:
            yield f.read()


#============#
# 匹配IP地址 #
#============#
def ipMatch(value,http=None):
    result = {}
    if http:
        result[0]='http'
    for i in value:
        # 匹配协议，http 或 https
        if re.match(r'^(http|https)',i,re.I):
            result[0] = i
        # 匹配IP
        if re.match(r'^(?:(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:1[0-9][0-9]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:2[0-5][0-5])|(?:25[0-5])|(?:1[0-9][0-9])|(?:[1-9][0-9])|(?:[0-9]))$',i):
            result[1] = i
        # 匹配端口号
        if re.match(r'^([0-9]{3,5})$',i):
            result[2] = i
    if len(result) == 3:
        # 合并完整地址
        ip = (result[0].upper(),result[1] + ':' + result[2])
        #ip = result[0].upper()+'://'+result[1] + ':' + result[2]
        return ip
    else:
        # 如果没有完整的地址，则返回None
        return None
