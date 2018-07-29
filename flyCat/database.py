#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
数据库文件
'''
# os
import os.path
# SQLite3
import sqlite3
# 配置文件
import flyCat.config as config
# 数据库文件路径
db_path = config.Config['data_path'] + 'db/ip_pool.db'

def create():
    '''
    创建SQLite数据库
    '''
    with sqlite3.connect(db_path) as db:
        db.execute('CREATE TABLE pool(protocol varchar(5) NOT NULL,ip varchar(21) NOT NULL PRIMARY KEY,status int(1) NOT NULL)')
    print(u'SQLite数据库创建成功,%s' % db_path)

# 如果数据库文件不存在贼创建，并初始化变量conn
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
else:
    create()
    conn = sqlite3.connect(db_path)

def insert(data):
    '''
    往数据库中插入新数据
    '''
    with conn:
        conn.executemany('REPLACE INTO pool(protocol,ip,status) VALUES(?,?,?)',data)
        #conn.commit()

def select():
    '''
    获取数据库中所有数据
    '''
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pool')
        values = cursor.fetchall()
        cursor.close()
    return values

def update(ip,status):
    '''
    更新status，
    在proxy_test以后，如果连接异常，则更新数据的status
    '''
    with conn:
        conn.execute('UPDATE pool SET status = \'' + status + '\' WHERE ip = \'' + ip + '\'')
        #conn.commit()

def delete(ip = None):
    '''
    删除低等级数据，
    删除数据库中status为0的数据，
    也可以直接传入需要删除的IP进行删除操作
    '''
    with conn:        
        if ip:
            conn.execute('DELETE FROM pool WHERE ip = ?',ip)
        else:
            conn.execute('DELETE FROM pool WHERE status = \'0\'')
        #conn.commit()

def status():
    '''
    查询status
    '''
    with conn:
        count = conn.execute('SELECT count(*) FROM pool')
    for i in count:
        print(i)

def rand_proxy(limit = ''):
    '''
    随机获取数据库中指定条数数据，
    如果没有设置limit，则按照config中的默认条数进行返回
    '''
    if limit == '':
        limit = config.Config['rand_proxy_limit']
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT protocol,ip FROM pool WHERE status = \'5\' ORDER BY random() LIMIT ' + str(limit))
        values = cursor.fetchall()
        cursor.close()
    return values

