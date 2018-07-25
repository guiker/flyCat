#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#===================================
# 下载器
#===================================
import flyCat.agents as agents
import flyCat.log as log
import urllib.request
import urllib.error
import socket
#import random
class Begin:
    #初始化proxy
    proxy = {}
    #proxy开关
    proxySwitch = False
    #载入User-Agent
    header = agents.userAgents()

    #==================#
    # 实例化downloader #
    #==================#
    def __init__(self,proxy = {}):
        '''
        Read读取代理网站HTML数据
        1、确认是否需要用代理IP访问代理网站
        '''
        if proxy:
            # 1、判断是否有初始代理IP传入，选择不同的request方式
            self.proxy = proxy

    #=============#
    # 读取URL数据 #
    #=============#
    def readURL(self,url):
        '''
        读取RUL的内容，并返回
        '''
        try:
            if self.proxy:
                #如果有使用初始代理IP访问代理网站，则选择此response方法 
                proxySupport = urllib.request.ProxyHandler(self.proxy)
                opener = urllib.request.build_opener(proxySupport)
                #载入User-Agent
                opener.addheaders = {('User-Agent',self.header)}
                urllib.request.install_opener(opener)
                log.msg('reduced',u'[proxy]抓取 %s ' % url)
                read_url = urllib.request.urlopen(url).read()
            else:
                log.msg('reduced',u'抓取 %s ' % url)
                req = urllib.request.Request(url,headers = {'User-Agent':self.header})
                read_url = urllib.request.urlopen(req,timeout = 20).read()
            #返回读取内容
            try:
                html = read_url.decode('UTF-8')
                log.msg('reduced',u'网页编码为UTF-8，已解码...')
            except:
                html = read_url.decode('GBK')
                log.msg('reduced',u'网页编码为GBK，已解码...')
            return html
        except urllib.error.HTTPError as e:
            log.msg('tightened',u'HTTP错误，错误代码是:' + str(e.code))
            return False
        except urllib.error.URLError as e:
            log.msg('tightened',u'URL错误，错误代码是:' + str(e.reason))
            return False
        except socket.timeout as e:
            log.msg('tightened',u'socket.timeout !')
            return False
    def result(self):
        pass

