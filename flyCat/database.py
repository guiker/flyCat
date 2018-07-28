#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import flyCat.config as config

def create():
    conn = sqlite3.connect(config.Config['save_path'] + '/db/ip_pool.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE pool(protocol varchar(5) NOT NULL,ip varchar(21) NOT NULL PRIMARY KEY,status int(1) NOT NULL)')
    cursor.close()
    conn.commit()
    conn.close()

def insert(datas):
    conn = sqlite3.connect(config.Config['save_path'] + '/db/ip_pool.db')
    cursor = conn.cursor()
    for data in datas:
        cursor.execute('REPLACE INTO pool(protocol,ip,status) VALUES(\'' + data[0] + '\',\'' + data[1] + '\',\'' + data[2] + '\')')
    cursor.close()
    conn.commit()
    conn.close()

def select():
    conn = sqlite3.connect(config.Config['save_path'] + '/db/ip_pool.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pool')
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return values

def update(ip,status):
    conn = sqlite3.connect(config.Config['save_path'] + '/db/ip_pool.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE pool SET status = \'' + status + '\' WHERE ip = \'' + ip + '\'')
    cursor.close()
    conn.commit()
    conn.close()

def delete(ip = None):
    conn = sqlite3.connect(config.Config['save_path'] + '/db/ip_pool.db')
    cursor = conn.cursor()
    if ip:
        cursor.execute('DELETE FROM pool WHERE ip = \'' + ip + '\'')
    else:
        cursor.execute('DELETE FROM pool WHERE status = \'0\'')
    cursor.close()
    conn.commit()
    conn.close()

