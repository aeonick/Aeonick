# -*- coding: utf-8 -*-
from flask import g
import sqlite3
from blog import app

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv
    
def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db