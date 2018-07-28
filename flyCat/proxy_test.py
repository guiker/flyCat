#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#===================================
# 代理IP测试
#===================================
import flyCat.agents as agents
import flyCat.config as config
import flyCat.log as log
import flyCat.database as db
import urllib.request
import urllib.error
import socket
def ping(ip = {},data = 'csv'):
    ip_dict = {}
    if ip:
        pass
    else:
        db.delete()
        data = db.select()
        for rows in data:
            try:
                # print(rows[0],rows[1],rows[2])
                proxySupport = urllib.request.ProxyHandler({rows[0]:rows[1]})
                opener = urllib.request.build_opener(proxySupport)
                #载入User-Agent
                opener.addheaders = {('User-Agent',agents.userAgents())}
                urllib.request.install_opener(opener)
                read = urllib.request.urlopen(config.Config['ping_site'],timeout = 5).read()
                html=read[0:9]
                if html.decode('UTF-8') == '<!DOCTYPE':
                    print(rows[1],'...OK')
                    if rows[2] != 5:
                        db.update(ip = rows[1],status = str(5))
                else:
                    print(rows[1],'...Bad')
                    db.update(ip = rows[1],status = str(rows[2]-1))
            except urllib.error.HTTPError as e:
                log.msg('tightened',rows[1] + u'HTTP错误，错误代码是:' + str(e.code))
                db.update(ip = rows[1],status = str(rows[2]-1))
            except urllib.error.URLError as e:
                log.msg('tightened',rows[1] + u'URL错误，错误代码是:' + str(e.reason))
                db.update(ip = rows[1],status = str(rows[2]-1))
            except socket.timeout as e:
                log.msg('tightened',rows[1] + u'链接超时')
                db.update(ip = rows[1],status = str(rows[2]-1))

