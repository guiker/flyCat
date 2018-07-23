#!/usr/bin/env python3
#===================================
# @Version:0.1 Beta
# @Author:guiker
# @Create Time:00:37 01/05/2018
# @File Name:__init__.py
# @Description:
# 主程序
#===================================
import flyCat.downloader as downloader
import flyCat.spider as spider
import flyCat.urltest as urltest
import flyCat.config as config
import flyCat.log as log
import pandas as pd
import re
import os
import time
class Paw:
    config = {}
    spider_dict = {}
    start_proxy={}

    #============#
    # 解析spider #
    #============#
    def _dir_spider(self):
        '''
        private
        遍历用户设置的spider模块,返回new_spider列表
        '''
        old_spider = dir(spider)
        new_spider = []
        spider_dict = {}
        for each in old_spider:
            if re.match(r'[^_]',each):
                new_spider.append(each)
        for name in new_spider:
            doc = eval('spider.' + name + '.__doc__')
            spider_dict[name] = doc
        return spider_dict
    #================#
    # spider页面解析 #
    #================#
    def _spider_page(self,page):
        page_list=[]
        pre=re.search(r'\<.*\>',page)
        if pre:
            turn=re.sub(r'\<|\>','',pre.group()).split(',')
            for i in range(int(turn[1])):
                page_list.append(page.replace(pre.group(),str(int(turn[0])+i)))
        else:
            page_list.append(page)
        return page_list

    #==========#
    # 保存数据 #
    #==========#
    def _save(self,data):
        ipdata = list()
        for ip in data:
            ipdata.append(list(ip))
        df = pd.DataFrame(ipdata)
        df.to_csv('ip_pool.csv' , index = 0 , header = 0)
        log.msg('tightened',u'数据保存成功！^_^')

    #==========#
    # 启动程序 #
    #==========#
    def start(self):
        '''
        启动flyCat
        starProxy()-访问代理IP网站的代理IP
        '''
        log.msg('tightened',u'flyCat 代理IP抓取程序已启动...')
        data_all = set()
        # 遍历spider_dict
        for name in self.spider_dict:
            page_list=self._spider_page(self.spider_dict[name])
            log.msg('reduced',u'正在读取 %s 抓取配置...' % name)
            num=1
            for page in page_list:
                # 初始化downloader
                down = downloader.Begin(self.start_proxy) 
                # 读取代理网站HTML数据
                html = str(down.readURL(page))
                # 将数据写入缓存
                log.msg('reduced',u'写入缓存...')
                with open(self.config['cache_path'] + 'html/' + name + '/' + str(num) + '.html','w+',encoding='UTF-8') as f:
                    f.write(html)
                num += 1
                # 运行spider解析HTML数据
            data = eval('spider.' + name + '()')
            data_all.update(data)
        self._save(data_all)

    #=======#
    # debug #
    #=======#
    def debug(self,name):
        #data_all=set()
        if name:
            log.msg('tightened',u'flyCat 开始调试 %s ,请耐心等待...' % name)
            path = self.spider_dict[name]
            page_list = self._spider_page(path)
            log.msg('reduced',u'读取 %s 抓取配置...' % name)
            num=1
            for page in page_list:
                down = downloader.Begin(self.start_proxy)
                html = str(down.readURL(page))
                log.msg('reduced',u'写入缓存...')
                with open(self.config['cache_path'] +  'html/' + name + '/' + str(num) + '.html','w+',encoding='UTF-8') as f:
                    f.write(html)
                f.close()
                num+=1
                time.sleep(2)
                # 运行spider解析HTML数据
            log.msg('reduced',u'解析 %s 数据...' % name)
            data = eval('spider.' + name + '()')
            print(data)
        else:
            log.msg('tightened',u'debug需要name参数....')
                #data_all = data_all | data
        #print(data_all)

    #=============#
    # flyCat init #
    #=============#
    def __init__(self,startProxy={}):
        self.spider_dict = self._dir_spider()
        self.config = config.Config
        self.start_proxy=startProxy
        #初始化缓存路径
        for path in self.spider_dict:
            if not os.path.exists(self.config['cache_path']+'html/'+path):
                os.mkdir(self.config['cache_path']+'html/'+path)


