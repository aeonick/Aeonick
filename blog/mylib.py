# -*- coding: utf-8 -*-
from blog.blogDB import get_db

def global_exception(origin_func):
    def wrapper(self, *args, **kwargs):
        try:
            u = origin_func(self, *args, **kwargs)
            return u
        except Exception:
            return '0'
    return wrapper

class Manager:
    def __init__(self):
        self.db = get_db()
        self.cur = self.db.cursor()
        self.cur.execute('SELECT id,content from info order by id')
        temp = self.cur.fetchall()
        self.title=temp[4][1]
        self.subtitle=temp[3][1]
        self.password=temp[2][1]
        self.sidebar=temp[1][1]
        self.tags=temp[0][1]
        self.cate=dict(temp[6:])
    #@global_exception
    def getInfo(self):
        return {'title':self.title,'subtitle':self.subtitle,'sidebar':self.sidebar,'tags':self.tags,'cates':self.cate}
    #@global_exception
    def verify(self,password=''):
        from hashlib import md5
        temp=md5(password.encode('utf8')).hexdigest()+'1396'
        temp=md5(temp.encode('utf8')).hexdigest()
        if temp==self.password:
            return '1'
        else:
            return '0'
    #@global_exception
    def config(self,title='',subtitle='',sidebar='',tags=''):
        if title:
            self.cur.execute('UPDATE info SET content = ? where id = -1',(title,))
        if subtitle:
            self.cur.execute('UPDATE info SET content = ? where id = -2',(subtitle,))
        if sidebar:
            self.cur.execute('UPDATE info SET content = ? where id = -4',(sidebar,))
        if tags:
            self.cur.execute('UPDATE info SET content = ? where id = -5',(tags,))
        self.db.commit()
        return '1'
    #@global_exception
    def setPwd(self,old,new):
        from hashlib import md5
        temp=md5(old.encode('utf8')).hexdigest()+'1396'
        temp=md5(temp.encode('utf8')).hexdigest()
        if temp==self.password:
            self.cur.execute('UPDATE info SET content = ? where id = -3',(md5(new.encode('utf8')).hexdigest()+'1396',))
            self.db.commit()
            return '1'
        else:
            return "0"
    #@global_exception
    def setCate(self,oldId,newId,content):
        '''
        输入：旧id,新id,分类名
        旧id为0：新建分类
        新id为0：删除分类，原文章全部进入回收站
        '''
        if newId<1:
            self.cur.execute('delete from info where id = ?',(oldId,))
            self.cur.execute('UPDATE blog SET file=0 where file = ?',(oldId,))
        if oldId==0:
            self.cur.execute('insert into info (id,content) values (?, ?)', (newId,content))
        else:
            self.cur.execute('UPDATE info SET id=?,content=? where id = ?',(newId,content,oldId))
            self.cur.execute('UPDATE blog SET file=? where file = ?',(newId,oldId))
        self.db.commit()
        return '1'

class Article:
    def __init__(self):
        self.db = get_db()
        self.cur = self.db.cursor()
    @global_exception
    def getFull(self,id):
        self.cur.execute('SELECT title, date, content, tag, abstract, file,img from blog where id = ?',(id,))
        arti = self.cur.fetchall()[0]
        result={'id':id,'artititle':arti[0],'date':arti[1],'content':arti[2],'tag':arti[3],'abstract':arti[4],'file':arti[5],'img':arti[6]}
        return result
    #@global_exception
    def edit(self, id, title, abstract, tag, img, file, content):
        '''
        id=0：新文章
        id不为零：更新旧有文章
        tag：,作为分隔符
        '''
        tags = (tag or '').replace('，',',')
        if id:
            self.cur.execute('UPDATE blog SET title = ? ,content = ?,abstract = ?,tag = ? ,file = ? ,img=? WHERE ID = ?;', (title,content,abstract,tags,file,img,id))
        else:
            self.cur.execute('insert into blog (title,tag,file,abstract,content,img) values (?, ?, ?, ?, ?, ?)', (title,tags,file,abstract,content,img))
            self.cur.execute('select id from blog order by id desc limit 1')
            blog = self.cur.fetchall()
            id = blog[0][0]
        self.cur.execute('delete from tag where blog = ?',(id,))
        tags = tags.split(',')
        for tag in tags:
            self.cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, id))
        self.db.commit()
        return '1'
    #@global_exception
    def delIt(self,id):
        self.cur.execute('DELETE FROM blog WHERE id = ? ',(self.id,))
        self.cur.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        self.cur.execute('DELETE FROM comm WHERE blog = ? ',(self.id,))
        self.db.commit()
        return '1'
    #@global_exception
    def hideIt(self,id):
        self.cur.execute('update blog set file = 0 WHERE id = ? ',(self.id,))
        self.cur.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        self.db.commit()
        return '1'

class Comment:
    def __init__(self):
        self.db = get_db()
        self.cur = self.db.cursor()
    #@global_exception
    def getIt(self,id):
        self.cur.execute(' SELECT content, date, author, id, reply FROM comm WHERE blog = ? ORDER BY id DESC',(id,))
        comms = self.cur.fetchall()
        subcoms=[]
        results={}
        for comm in comms:
            if comm[4]:
                subcoms.append(comm)
            else:
                results[str(comm[3])]={'content':comm[0],'date':comm[1],'author':comm[2],'subcom':{}}
        for subcom in subcoms:
            if str(subcom[4]) in results:
                results[str(subcom[4])]['subcom'][str(subcom[3])]={'content':subcom[0],'date':subcom[1],'author':subcom[2]}
            else:
                results[str(subcom[3])]={'content':subcom[0],'date':subcom[1],'author':subcom[2],'subcom':{}}
        return results
    #@global_exception
    def insert(self,id, content, author, reply):
        self.cur.execute('insert into comm (content, author, blog, reply) values (?, ?, ?, ?)', (content, author, id, reply))
        self.db.commit()
        return '1'
    #@global_exception
    def delIt(self,id):
        self.cur.execute('DELETE FROM comm WHERE id = ? ',(id,))
        self.db.commit()
        return '1'

class ArtiList:
    def __init__(self):
        self.db = get_db()
        self.cur = self.db.cursor()
    #@global_exception
    def getList(self,method = '',key = '',page = 1):
        results={}
        offset=(page-1)*8
        if method == 'file':
            self.cur.execute('SELECT count(*) FROM blog WHERE file = ?;',(key,))
        elif method == 'tag':
            self.cur.execute('SELECT count(*) FROM tag WHERE tag = ?;',(key,))
        else:
            self.cur.execute('SELECT count(*) FROM blog where file>0;')
        results['count']=int((self.cur.fetchall()[0][0]-1)/8)+1
        if method == 'file':
            self.cur.execute('SELECT title, date, id, tag, abstract, file,img FROM blog WHERE file = ? ORDER BY id DESC LIMIT 8 OFFSET ?',(key,offset,))
        elif method == 'tag':
            self.cur.execute('SELECT blog.title, blog.date, blog.id, blog.tag, blog.abstract, blog.file, blog.img FROM blog, tag WHERE blog.id = tag.blog AND tag.tag = ? ORDER BY blog.id DESC LIMIT 8 OFFSET ?',(key,offset,))
        else:
            self.cur.execute('SELECT title, date, id, tag, abstract, file,img FROM blog where file>0 ORDER BY id DESC LIMIT 8 OFFSET ?',(offset,))
        artis = self.cur.fetchall()
        results['artis']=[]
        for arti in artis:
            results['artis'].append({'id':arti[2],'title':arti[0],'date':arti[1],'tag':arti[3],'abstract':arti[4],'file':arti[5],'img':arti[6]})
        return results