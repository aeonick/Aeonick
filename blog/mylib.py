# -*- coding: utf-8 -*-
from blogDB import get_db

class blogInfo:
    def __init__(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT id,content from info order by id')
        temp = cur.fetchall()
        self.title=temp[4][1]
        self.subtitle=temp[3][1]
        self.password=temp[2][1]
        self.sidebar=temp[1][1]
        self.tags=temp[0][1]
        self.cate=dict(temp[6:])
    def verify(self,password=''):
        import hashlib
        m = hashlib.md5()
        m.update(password)
        m.update(m.hexdigest()+'1396')
        if m.hexdigest()==self.password:
            return True
        else:
            return False
    def config(self,title='',subtitle='',sidebar='',tags=''):
        blogdb = get_db()
        cur = blogdb.cursor()
        if title:
            cur.execute('UPDATE info SET content = ? where id = -1',(title,))
        if subtitle:
            cur.execute('UPDATE info SET content = ? where id = -2',(subtitle,))
        if sidebar:
            cur.execute('UPDATE info SET content = ? where id = -4',(sidebar,))
        if tags:
            cur.execute('UPDATE info SET content = ? where id = -5',(tags,))
        blogdb.commit()
    def setPwd(self,old,new):
        import hashlib
        m = hashlib.md5()
        m.update(old)
        m.update(m.hexdigest()+'1396')
        if m.hexdigest()==self.password:
            m = hashlib.md5()
            m.update(new)
            m.update(m.hexdigest()+'1396')
            blogdb = get_db()
            cur = blogdb.cursor()
            cur.execute('UPDATE info SET content = ? where id = -3',(m.hexdigest(),))
            blogdb.commit()
            return 'Success'
        else:
            return "Couldn't match"
    def setCate(self,oldId,newId,content):
        blogdb = get_db()
        cur = blogdb.cursor()
        try:
            if newId<1:
                cur.execute('delete from info where id = ?',(oldId,))
                cur.execute('UPDATE blog SET file=0 where file = ?',(oldId,))
                blogdb.commit()
            if oldId==0:
                cur.execute('insert into info (id,content) values (?, ?)', (newId,content))
            else:
                cur.execute('UPDATE info SET id=?,content=? where id = ?',(newId,content,oldId))
                cur.execute('UPDATE blog SET file=? where file = ?',(newId,oldId))
            blogdb.commit()
            return 'Success'
        except:
            return 'Database Error'

class Article:
    def __init__(self,id=0):
        self.id = id
    def getIt(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('SELECT title, date, content, tag, abstract, file,img from blog where id = ?',(self.id,))
        arti = cur.fetchall()[0]
        self.title = arti[0]
        self.date = arti[1]
        if hasattr(self.date,'strftime'):
            self.date = self.date.strftime("%Y-%m-%d %H:%M:?")
        self.content = arti[2]
        self.tag = arti[3] or ''
        self.abstract = arti[4]
        self.file=arti[5]
        self.img=arti[6] or ''
    def edit(self, title, tag, img, file, content):
        abstract = abstr(content)
        tags = (tag or '').replace('，',',')
        blogdb = get_db()
        cur = blogdb.cursor()
        if self.id:
            cur.execute('UPDATE blog SET title = ? ,content = ?,abstract = ?,tag = ? ,file = ? ,img=? WHERE ID = ?;', (title, content,abstract,tags,file,img, self.id))
        else:
            cur.execute('insert into blog (title,tag,file,abstract,content,img) values (?, ?, ?, ?, ?, ?)', (title,tags,file,abstract,content,img))
            cur.execute('select id from blog order by id desc limit 1')
            blog = cur.fetchall()
            self.id = blog[0][0]
        blogdb.commit()
        cur.execute('delete from tag where blog = ?',(self.id,))
        tags = tags.split(',')
        for tag in tags:
            cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, self.id))
        blogdb.commit()
    def delIt(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('DELETE FROM blog WHERE id = ? ',(self.id,))
        cur.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        cur.execute('DELETE FROM comm WHERE blog = ? ',(self.id,))
        blogdb.commit()
    def hideIt(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('update blog set file = 0 WHERE id = ? ',(self.id,))
        cur.execute('DELETE FROM tag WHERE blog = ? ',(self.id,))
        blogdb.commit()

class Comment:
    def __init__(self, id=0):
        self.id = id
    def getIt(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute(' SELECT content, date, author, id, reply FROM comm WHERE blog = ? ORDER BY id DESC',(self.id,))
        temp = cur.fetchall()
        def preRep(c):
            c=list(c)+['']
            if c[4]:
                c[5]='1'
            else:
                c[4]=c[3]
            return c
        temp = map(preRep,list(temp))
        def coSort(x,y):
            if x[4]<y[4]:
                return 1
            else:
                return -1
        temp.sort(coSort)
        self.cl = temp
    def getNew(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute(' SELECT content, date, author, id, blog FROM comm ORDER BY id DESC LIMIT 8 ')
        temp = cur.fetchall()
        self.cl = temp
        return self.cl
    def insert(self, content, author, reply):
        author = author or u'访客'
        reply = reply or None
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('insert into comm (content, author, blog, reply) values (?, ?, ?, ?)', (content, author, self.id, reply))
        blogdb.commit()
    def delIt(self,cid):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute('DELETE FROM comm WHERE id = ? ',(cid,))
        blogdb.commit()

class ArtiList:
    def __init__(self,method = '',key = '',page = 1):
        self.method = method
        self.key = key
        self.offset = ( page - 1 ) * 8
        self.page = page
    def getRe(self):
        results = []
        for arti in self.al:
            temp = Article(arti)
            temp.getIt()
            results.append(temp)
        self.results = results
    def getPagn(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        if self.method == 'file':
            cur.execute('SELECT count(*) FROM blog WHERE file = ?;',(self.key,))
        elif self.method == 'tag':
            cur.execute('SELECT count(*) FROM tag WHERE tag = ?;',(self.key,))
        else:
            cur.execute('SELECT count(*) FROM blog where file>0;')
        pMax = cur.fetchall()
        pMax = (int(pMax[0][0])+7)/8
        if self.page<=pMax and self.page>0:
            pagn = [[x,'',x] for x in range(1,pMax+1)]
            pagn[self.page-1][1]='active'
            if self.page==1:
                before=[]
            else:
                before=[['','prev',self.page-1],]
            if self.page==pMax:
                after=[]
            else:
                after=[['','next',self.page+1],]
            self.pagn = before+pagn+after
        else:
            self.pagn = []
        return self.pagn
    def getAl(self):
        blogdb = get_db()
        cur = blogdb.cursor()
        if self.method == 'file':
            cur.execute(' SELECT id FROM blog WHERE file = ? ORDER BY id DESC LIMIT 8 OFFSET ?',(self.key,self.offset,))
        elif self.method == 'tag':
            cur.execute('select blog from tag where tag = ? LIMIT 8 OFFSET ?',(self.key,self.offset,))
        else:
            cur.execute(' SELECT id FROM blog where file>0 ORDER BY id DESC LIMIT 8 OFFSET ?',(self.offset,))
        al = cur.fetchall()
        al = map(lambda x: int(x[0]),al)
        al.sort(reverse = True)
        self.al = al




def abstr(text):
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
    if text:
        text = reduce(fn,text)
        text = text.replace(u'<>',u'')
        text = text.replace(u'\n\n\n',u'\n')
        text = text.replace(u'\n\n',u'\n')
        text = text[:120]
        while text[0]==u'\n':
            text=text[1:]
        while text[-1]==u'\n':
            text=text[:-1]
    text=text+'...'
    return text