#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
主程序
'''
# 下载器
import flyCat.downloader as downloader
# spider
import flyCat.spider as spider
# 配置文件
import flyCat.config as config
# 日志文件
import flyCat.log as log
# 数据库文件
import flyCat.database as db
#import pandas as pd
import re
import os
import time
class Paw:
    config = {}
    spider_dict = {}
    start_proxy = {}

    def _dir_spider(self):
        '''
        解析spider
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

    def _spider_page(self,page):
        '''
        spider分页面解析
        '''
        page_list=[]
        pre = re.search(r'\<.*\>',page)
        if pre:
            turn = re.sub(r'\<|\>','',pre.group()).split(',')
            for i in range(int(turn[1])):
                page_list.append(page.replace(pre.group(),str(int(turn[0])+i)))
        else:
            page_list.append(page)
        return page_list

    def _save(self,data):
        '''
        保存数据
        对抓取结果进行保存，暂时只保存为CSV
        '''
        log.msg('tightened',u'正在保存数据...')
        db.insert(data)
        log.msg('tightened',u'数据保存成功！^_^')

    def start(self):
        '''
        启动flyCat
        starProxy()-访问代理IP网站的代理IP
        '''
        log.msg('tightened',u'flyCat 代理IP抓取程序已启动...')
        #data_all = set()
        # 遍历spider_dict
        for name in self.spider_dict:
            data_all = set()
            page_list = self._spider_page(self.spider_dict[name])
            log.msg('reduced',u'正在读取 %s 抓取配置...' % name)
            num = 1
            for page in page_list:
                # 初始化downloader
                down = downloader.Begin(self.start_proxy) 
                # 读取代理网站HTML数据
                html = down.readURL(page)
                if html:
                    # 将数据写入缓存
                    log.msg('reduced',u'写入缓存...')
                    with open(self.config['cache_path'] + 'html/' + name + '/' + str(num) + '.html','w+',encoding='UTF-8') as f:
                        f.write(str(html))
                num += 1
                # 运行spider解析HTML数据
            data = eval('spider.' + name + '()')
            data_all.update(data)
            self._save(data_all)
        #self._save(data_all)

    def debug(self,name):
        '''
        用于对spider抓取规则的调试，
        抓取完成以后print()出结果，不执行保存
        '''
        #data_all=set()
        if name:
            log.msg('tightened',u'flyCat 开始调试 %s ,请耐心等待...' % name)
            path = self.spider_dict[name]
            page_list = self._spider_page(path)
            log.msg('reduced',u'读取 %s 抓取配置...' % name)
            num = 1
            for page in page_list:
                down = downloader.Begin(self.start_proxy)
                html = down.readURL(page)
                if html:
                    log.msg('reduced',u'写入缓存...')
                    with open(self.config['cache_path'] +  'html/' + name + '/' + str(num) + '.html','w+',encoding='UTF-8') as f:
                        f.write(str(html))
                    num += 1
                #time.sleep(2)
            # 运行spider解析HTML数据
            log.msg('reduced',u'解析 %s 数据...' % name)
            data = eval('spider.' + name + '()')
            print(data)
        else:
            log.msg('tightened',u'debug需要name参数....')
                #data_all = data_all | data
        #print(data_all)

    def __init__(self,startProxy={}):
        # 初始化spider
        self.spider_dict = self._dir_spider()
        # 载入配置文件
        self.config = config.Config
        # 载入代理
        self.start_proxy = startProxy
        # 初始化缓存路径
        if not os.path.exists(self.config['cache_path']):
            os.mkdir(self.config['cache_path'])
        if not os.path.exists(self.config['cache_path'] + 'html/'):
            os.mkdir(self.config['cache_path'] + 'html/')
        # 初始化数据保存路径
        if not os.path.exists(self.config['data_path']):
            os.mkdir(self.config['data_path'])
        if not os.path.exists(self.config['data_path'] + 'db/'):
            os.mkdir(self.config['data_path'] + 'db/')
        # 初始化spider路径
        for path in self.spider_dict:
            if not os.path.exists(self.config['cache_path'] + 'html/' + path):
                os.mkdir(self.config['cache_path'] + 'html/' + path)


