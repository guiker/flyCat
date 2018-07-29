#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#===================================
# 下载器
#===================================
import flyCat.agents as agents
import flyCat.log as log
import flyCat.config as config
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
    #抓取超时
    spider_timeout = config.Config['spider_timeout']

    def __init__(self,proxy = {}):
        '''
        Read读取代理网站HTML数据
        1、确认是否需要用代理IP访问代理网站
        '''
        if proxy:
            # 1、判断是否有初始代理IP传入，选择不同的request方式
            self.proxy = proxy

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
                response = urllib.request.urlopen(url)
                read_url = response.read()
                response.close()
            else:
                log.msg('reduced',u'抓取 %s ' % url)
                req = urllib.request.Request(url,headers = {'User-Agent':self.header})
                response = urllib.request.urlopen(req,timeout = self.spider_timeout)
                read_url = response.read()
                response.close()
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
            log.msg('tightened',u'连接超时...')
            return False
    def result(self):
        pass

