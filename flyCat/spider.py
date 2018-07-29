#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#===================================
# 解析器
#===================================


#========================================#
#--------* 特 * 别 * 提 * 示 *-----------#
# 载入模块必须加别名，别名必须加下划线 _ #
# 在此文件下,                            #
# 除spider以外的任何函数必须加下划线 _   #
# 缓存文件默认保存在 ./flyCat/cache/ 下  #
# 文件名与自建spider函数同名             #
#========================================#

#载入BeautifulSoup
from bs4 import BeautifulSoup as _BeautifulSoup
#载入plug
import flyCat.spider_plug as _plug

#================#
# spider by 西刺 #
#================#
def xici():
    'http://www.xicidaili.com/nn/<1,2>'
    load = _plug.load('xici')
    allip = set()
    for html in load:  
        soup = _BeautifulSoup(html,'lxml')
        td = soup.find_all('td',class_ = 'country')
        for b in td:
            l = []
            for d in b.next_siblings:
                if d.string != '\n':
                    l.append(str(d.string))
            if l != []:
                result = _plug.ip_match(l)
                if result:
                    allip.add(result)
    return allip


#================#
# spider by 66IP #
#================#
def llip():
    'http://www.66ip.cn/<2,2>.html'
    load = _plug.load('llip')
    allip = set()
    for html in load:
        soup = _BeautifulSoup(html,'lxml')
        tab = soup.find('table',bordercolor = '#6699ff')
        tr_all = tab.find_all('tr')
        for tr in tr_all:
            l = []
            for td in tr:
                for td_str in td.children:
                    l.append(td_str)
            result = _plug.ip_match(l,protocol = 'http')
            if result:
                allip.add(result)
    return allip

#================#
# spider by 89ip #
#================#
def bgip():
    'http://www.89ip.cn/index_<2,2>.html'
    load = _plug.load('bgip')
    allip = set()
    for html in load:
        soup = _BeautifulSoup(html,'lxml')
        tbody = soup.find('tbody')
        for tr in tbody:
            l = []
            for td in tr:
                for td_str in td:
                    l.append(td_str.strip())
            result = _plug.ip_match(l,protocol = 'http')
            if result:
                allip.add(result)
    return allip
