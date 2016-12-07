# -*- coding: utf-8 -*-
from blog import app
from flask import Flask, g
import sqlite3

#链接和关闭数据库的三个函数
def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv

#定义类
class password:
    def __init__(self,pwd):
        self.pwd = pwd
    def check(self):
        import hashlib
        m = hashlib.md5()
        if self.pwd:
            self.pwd +=  '1396'
        else:
            return False
        m.update(self.pwd)
        if m.hexdigest()=='01bf2bf3375b3fbaf8d2dac6dad08c84':
            return True
        else:
            return False

class Article:
    def __init__(self, id):
        self.id = id
    def getExit(self):
        pass
    def getArti(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT title, date, content, tag, abstract from blog where id = ?',(self.id,))
        self.arti = cur.fetchall()[0]
        return self.arti
    def getEdit(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT title, content,tag from blog where id = ?',(self.id,))
        content = cur.fetchall()[0]
        self.title = content[0]
        self.content = content[1]
        self.tag = content[2]
    def update(self, title, tag, img, file, content):
        abstract = abstr(content,img)
        tags = (tag or '').replace('，',',')
        blogdb = get_db()
        cur = blogdb.cursor()
        if self.id:
            cur.execute('UPDATE blog SET title = ? ,content = ?,abstract = ?,tag = ? ,file = ? WHERE ID = ?;', (title, content,abstract,tags,file, self.id))
        else:
            cur.execute('insert into blog (title,tag,file,abstract,content) values (?, ?, ?, ?, ?)', (title,tag,file,abstract,content))
            cur.execute('select id from blog order by id desc limit 1')
            blog = cur.fetchall()
            self.id = blog[0][0]
        blogdb.commit()
        cur.execute('delete from tag where blog = ?',(self.id,))
        tags = tags.split(',')
        for tag in tags:
            cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, self.id))
        blogdb.commit()
    def delArti(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('DELETE FROM blog WHERE id = ? ',(self.id,))
        cur.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        cur.execute('DELETE FROM comm WHERE blog = ? ',(self.id,))
        blogdb.commit()

class comment:
    def __init__(self, id):
        self.id = id
    def commList(self):
        try:
            blogdb = get_db()
            cur = blogdb.cursor()
            cur.execute(' SELECT content, date, author, id, reply FROM comm WHERE blog = ? ORDER BY id DESC',(self.id,))
            temp = cur.fetchall() or []
            temp = list(temp)
            temp = map(lambda x:list(x),temp)
            def coSort(x,y):
                xId = x[4] or x[3]
                yId = y[4] or y[3]
                if xId<yId:
                    return 1
                else:
                    return -1
            temp = sorted(temp, coSort)
            def coVeri(x):
                x[4] = x[4] or x[3]
                diff = x[4]-x[3]
                x[4] = diff and u're'
                return x
            self.cList = map(coVeri,temp)
        except:
            self.cList = []
        finally:
            return self.cList
    def insert(self, content, author, reply):
        author = author or u'访客'
        reply = reply or None
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('insert into comm (content, author, blog, reply) values (?, ?, ?, ?)', (content, author, self.id, reply))
        blogdb.commit()
    def dele(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('DELETE FROM comm WHERE id = ? ',(self.id,))
        blogdb.commit()



#摘要生成函数，这个实现方式比较蠢，还有一个更快的在aids.py里，但很难看
def abstr(text,img = ""):
    text = text[:1200]
    text = text.replace(u'&nbsp;',u' ')
    text = text.replace(u'</p',u'\n<')
    text = text.replace(u'</b',u'\n<')
    text = text.replace(u'</h',u'\n<')
    text = text.replace(u'<br>',u'\n')
    def fn(x, y):
        if x[-1] == "<" and y != ">":
            return x
        else:
            return x+y
    text = reduce(fn,text)
    text = text.replace(u'<>',u'')
    text = text.replace(u'\n\n\n',u'\n')
    text = text.replace(u'\n\n',u'\n')
    print text
    text = text[:120]+'...'+'<center>'+img+'</center>'
    return text
