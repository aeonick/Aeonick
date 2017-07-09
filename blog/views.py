# -*- coding: utf-8 -*-

from blog import app
from flask import Flask, render_template, session, redirect, url_for, request, g, flash, send_from_directory,abort
from mylib import Comment,Article,ArtiList,blogInfo



#异常处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html' ,info=blogInfo()), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',info=blogInfo()), 500
@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html',info=blogInfo()), 400
@app.errorhandler(403)
def forbidden(e):
    return render_template('forbidden.html',info=blogInfo()), 403


#自动关闭数据库连接
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    info=blogInfo()
    curPage = ArtiList(page=1)
    curPage.getAl()
    curPage.getPagn()
    curPage.getRe()
    return render_template('index.html',results = curPage.results, pagn = curPage.pagn,info=info)
@app.route('/page/<int:pg>')
def page(pg):
    info=blogInfo()
    curPage = ArtiList(page=pg)
    if curPage.getPagn():
        curPage.getAl()
        curPage.getRe()
        return render_template('page.html',results = curPage.results, pagn = curPage.pagn,info=info)
    else:
        abort(404)
@app.route('/arch<int:file>/<int:pg>')
def arch(file,pg):
    info=blogInfo()
    curPage = ArtiList('file',file,pg)
    if curPage.getPagn():
        curPage.getAl()
        curPage.getRe()
        return render_template('page.html',results = curPage.results, pagn = curPage.pagn,info=info)
    else:
        abort(404)
@app.route('/arch/<tag>/<int:pg>')
def tag(tag,pg):
    info=blogInfo()
    curPage = ArtiList('tag',tag,pg)
    if curPage.getPagn():
        curPage.getAl()
        curPage.getRe()
        return render_template('page.html',results = curPage.results, pagn = curPage.pagn,info=info)
    else:
        abort(404)
@app.route('/login', methods = ['GET', 'POST'])
def login():
    info=blogInfo()
    pwd = request.form.get('password')
    if pwd and info.verify(pwd):
        session['log'] = True
        return redirect(url_for('admin'))
    return render_template('login.html',info=info)
@app.route('/logout')
def logout():
    session['log'] = False
    return redirect(url_for('page',pg = 1))
@app.route('/admin')
def admin():
    if not session.get('log'):
        return redirect(url_for('login'))
    return render_template('admin.html',info=blogInfo(),cl=Comment().getNew())
@app.route('/article/<int:bg_id>')
def article(bg_id):
    if bg_id==0:
        return redirect(url_for('memo'))
    try:
        curArti = Article(bg_id)
        curArti.getIt()
    except:
        abort(404)
    if curArti.file!=0 or session.get('log'):
        info=blogInfo()
        info.subtitle=info.title
        info.title=curArti.title
        curComm=Comment(bg_id)
        curComm.getIt()
        return render_template('article.html',curArti = curArti,info=info,cl=curComm.cl)
    abort(404)
@app.route('/post/comment', methods=['POST'])
def commentPost():
    author = request.form.get('author')
    content = request.form.get('content')
    bid = request.form.get('bid',type=int)
    rid = request.form.get('rid',type=int)
    try:
        Comment(bid).insert(content,author,rid)
        return "Success"
    except:
        return "Error"
@app.route('/post/article', methods=['POST'])
def articlePost():
    if not session.get('log'):
        abort(403)
    title = request.form.get('title')
    content = request.form.get('editor')
    img = request.form.get('img')
    file = request.form.get('file',type=int)
    tag = request.form.get('tags')
    id = request.form.get('id',type=int)
    try:
        curArti=Article(id)
        curArti.edit(title, tag, img, file, content)
        return str(curArti.id)
    except:
        return "Error"
@app.route('/del/comment', methods=['POST'])
def commentDel():
    if not session.get('log'):
        abort(403)
    try:
        cid = request.form.get('cid',type=int)
        Comment(0).delIt(cid)
        return "Success"
    except:
        return "Error"
@app.route('/del/article', methods=['POST'])
def articleDel():
    if not session.get('log'):
        abort(403)
    try:
        bid = request.form.get('bid',type=int)
        Article(bid).hideIt()
        return "Success"
    except:
        return "Error"
@app.route('/config/tcg0', methods=['POST'])
def tcg0():
    if not session.get('log'):
        abort(403)
    title = request.form.get('tcg0')
    try:
        blogInfo().config(title=title)
        return "Success"
    except:
        return "Error"
@app.route('/config/tcg1', methods=['POST'])
def tcg1():
    if not session.get('log'):
        abort(403)
    subtitle = request.form.get('tcg1')
    try:
        blogInfo().config(subtitle=subtitle)
        return "Success"
    except:
        return "Error"
@app.route('/config/tcg2', methods=['POST'])
def tcg2():
    if not session.get('log'):
        abort(403)
    old = request.form.get('old')
    new = request.form.get('new')
    try:
        res = blogInfo().setPwd(old,new)
        return res
    except:
        return "Error"
@app.route('/config/tcg3', methods=['POST'])
def tcg3():
    if not session.get('log'):
        abort(403)
    sidebar = request.form.get('tcg3')
    try:
        blogInfo().config(sidebar=sidebar)
        return "Success"
    except:
        return "Error"
@app.route('/config/tcg4', methods=['POST'])
def tcg4():
    if not session.get('log'):
        abort(403)
    tags = request.form.get('tcg4')
    try:
        blogInfo().config(tags=tags)
        return "Success"
    except:
        return "Error"
@app.route('/config/cate', methods=['POST'])
def cate():
    if not session.get('log'):
        abort(403)
    oldId = request.form.get('oldId',type=int)
    newId = request.form.get('newId',type=int)
    content = request.form.get('content')
    res = blogInfo().setCate(oldId,newId,content)
    return res
@app.route('/memo')
def memo():
    curComm=Comment(0)
    curComm.getIt()
    return render_template('memo.html',cl = curComm.cl,info=blogInfo())
@app.route('/wish')
def wish():
    return render_template('wish.html',info=blogInfo())
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
@app.route('/edit/<int:bg_id>')
def edit(bg_id):
    if not session.get('log'):
        abort(403)
    try:
        curArti = Article(bg_id)
        curArti.getIt()
    except:
        abort(404)
    return render_template('edit.html',curArti = curArti,info=blogInfo())
@app.route('/edit')
def new():
    if not session.get('log'):
        abort(403)
    curArti = Article(0)
    return render_template('edit.html',curArti = curArti,info=blogInfo())
'''


@app.route('/new', methods = ['GET', 'POST'])
def new():
    if session.get('log'):
        curArti = Article(0)
        if request.method == 'POST':
            curArti.update(request.form['title'],request.form['tags'],request.form['img'],request.form['file'],request.form['editor'])
            return redirect(url_for('page',pg = 1))
        return render_template('edit.html',curArti = curArti)
    return redirect(url_for('page',pg = 1))



'''