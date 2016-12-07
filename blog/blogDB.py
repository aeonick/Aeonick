# -*- coding: utf-8 -*-

from blog import app
from flask import Flask, g
import sqlite3


#链接和关闭数据库的两个函数
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv
    
def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db