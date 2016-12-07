# -*- coding: utf-8 -*-

from blog import app
from flask import Flask, render_template, session, redirect, url_for, request, g, flash, send_from_directory
from mylib import *



#异常处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html'), 404




#管理权限认证模块
@app.route('/login', methods = ['GET', 'POST'])
def login():
    pwd = password(request.form.get('passwd'))
    if pwd.check():
        session['log'] = True
        return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['log'] = False
    return redirect(url_for('page',pg = 1))



#博客的添加、编辑和删除
@app.route('/new', methods = ['GET', 'POST'])
def new():
    if session.get('log'):
        if request.method == 'POST':
            curArti = Article(0)
            curArti.update(request.form['title'],request.form['tags'],request.form['img'],request.form['file'],request.form['editor'])
            return redirect(url_for('page',pg = 1))
        return render_template('edit.html')
    return redirect(url_for('page',pg = 1))

@app.route('/edit/<int:bg_id>', methods = ['GET', 'POST'])
def edit(bg_id):
    if session.get('log'):
        try:
            curArti = Article(bg_id)
            curArti.getEdit()
        except:
            return redirect(url_for('page',pg = 1))
        if request.method  == 'POST':
            curArti.update(request.form['title'],request.form['tags'],request.form['img'],request.form['file'],request.form['editor'])
            return redirect(url_for('article',bg_id = bg_id))
        return render_template('edit.html',content = curArti.content,title = curArti.title,tags = curArti.tag)
    return redirect(url_for('page',pg = 1))

@app.route('/dele/<int:bg_id>')
def dele(bg_id):
    if session.get('log'):
        curArti = Article(bg_id)
        curArti.delArti()
    return redirect(url_for('page',pg = 1))

@app.route('/del/<int:ccid>')
def delet(ccid):
    if session.get('log'):
        curComm = comment(ccid)
        curComm.dele()
    return redirect(request.referrer)



#文章浏览页
@app.route('/article/<int:bg_id>', methods = ['GET', 'POST'])
def article(bg_id):
    if request.method == 'POST' and request.form['comment']:
        tem = comment(bg_id)
        tem.insert(request.form['comment'],request.form['author'],request.form['reply'])
        return redirect(url_for('article',bg_id = bg_id))
    try:
        curArti = Article(bg_id)
        cont = curArti.getArti()
        tem = comment(bg_id)
        tem = tem.commList()
    except:
        return render_template('error.html'), 404
    return render_template('article.html',cont = cont,id = bg_id,tem = tem)



#留言板
@app.route('/memo',methods = ['GET', 'POST'])
def memo():
    curComm = comment(0)
    if request.method == 'POST' and request.form['comment']:
        curComm.insert(request.form['comment'], request.form['author'], None)
        return redirect(url_for('memo'))
    tem = curComm.commList()
    return render_template('memo.html',tem = tem)



#许愿池
@app.route('/wish',methods = ['GET', 'POST'])
def wish():
    if request.method == 'POST':
        flash('许愿池收到了你的愿望,祝你好运！')
        if request.form['comments']:
            newWish = comment(-1)
            newWish.insert(request.form['comments'], request.form['authors'], None)
            return render_template('wish.html')
        if request.form['commentm']:
            newWish = comment(-2)
            newWish.insert(request.form['commentm'], request.form['authorm'], None)
            return render_template('wish.html')
    return render_template('wish.html')



#文章检索、分类模块
@app.route('/')
def index():
    blogdb = get_db()
    cur = blogdb.cursor()
    cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog ORDER BY id DESC LIMIT 8')
    tem = cur.fetchall()
    cur.execute('SELECT count(*) FROM blog;')
    pmax = ((cur.fetchall()[0][0]+7)/8 or 1)
    return render_template('index.html',tem = tem,pmax = pmax,pg = 1)

@app.route('/page/<int:pg>')
def page(pg):
    blogdb = get_db()
    cur = blogdb.cursor()
    cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog ORDER BY id DESC LIMIT 8 OFFSET ?',(pg*8-8,))
    tem = cur.fetchall()
    cur.execute('SELECT count(*) FROM blog;')
    pmax = ((cur.fetchall()[0][0]+7)/8 or 1)
    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',tem = tem,pmax = pmax,pg = pg)

@app.route('/arch<int:arc>/<int:pg>')
def arch(arc,pg):
    blogdb = get_db()
    cur = blogdb.cursor()
    cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog WHERE file = ? ORDER BY id DESC LIMIT 8 OFFSET ?',(arc,pg*8-8,))
    tem = cur.fetchall()
    try:
        cur.execute('SELECT count(*) FROM blog WHERE file = ?;',(arc,))
        pmax = (cur.fetchall()[0][0]+7)/8
    finally:
        pmax = pmax or 1
    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',tem = tem,pmax = pmax,pg = pg)

@app.route('/arch/<tag>/<int:pg>')
def tag(tag,pg):
    blogdb = get_db()
    cur = blogdb.cursor()
    cur.execute('select blog from tag where tag = ? LIMIT 8 OFFSET ?',(tag,pg*8-8))
    tem = cur.fetchall()
    blogs = map(lambda x: int(x[0]),tem)
    blogs.sort(reverse = True)
    tem = []
    item = 0
    for blog in blogs:
        cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog WHERE id = ?',(blog,))
        tem.append(cur.fetchall()[0])
    try:
        cur.execute('SELECT count(*) FROM tag WHERE tag = ?;',(tag,))
        pmax = (cur.fetchall()[0][0]+7)/8
    finally:
        pmax = pmax or 1
    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',tem = tem,pmax = pmax,pg = pg)



#历史遗留，标签功能出故障时可以用它解决
@app.route('/heal')
def heal():
    blogdb = get_db()
    cur = blogdb.cursor()
    cur.execute('delete from tag')
    cur.execute('SELECT id,tag from blog')
    cont = cur.fetchall()
    for connn in cont:
        tags = connn[1]
        bg_id = connn[0]
        tags = tags.split(',')
        for tag in tags:
            cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, bg_id))
        blogdb.commit()
    return redirect(url_for('page',pg = 1))



#管理页面
@app.route('/admin')
def admin():
    if session.get('log'):
        blogdb = get_db()
        cur = blogdb.cursor()
        cur.execute(' SELECT content, author, date,blog FROM comm ORDER BY id DESC')
        tem = cur.fetchall()
        return render_template('admin.html',tem = tem)
    else:
        return redirect(url_for('login'))



#robots.txt
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])