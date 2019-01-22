# -*- coding: utf-8 -*-
from blog import app
from flask import Flask, render_template, session, redirect, url_for, request, g, send_from_directory,abort,jsonify
from blog.mylib import Comment,Article,ArtiList,Manager

#异常处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500
@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html'), 400
@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html'), 403

#自动关闭数据库连接
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    data=ArtiList().getList()
    return render_template('index.html',data=data)
@app.route('/page/<int:pg>')
def page(pg):
    data=ArtiList().getList(page=pg)
    if data['count']>0:
        return render_template('page.html', data=data)
    else:
        abort(404)
@app.route('/arch<int:file>/<int:pg>')
def arch(file,pg):
    data=ArtiList().getList('file',file,pg)
    if data['count']>0:
        return render_template('page.html', data=data)
    else:
        abort(404)
@app.route('/arch/<tag>/<int:pg>')
def tag(tag,pg):
    data=ArtiList().getList('tag',tag,pg)
    if data['count']>0:
        return render_template('page.html', data=data)
    else:
        abort(404)
@app.route('/login', methods = ['GET', 'POST'])
def login():
    pwd = request.form.get('password')
    if pwd and Manager().verify(pwd):
        session['log'] = True
        return redirect(url_for('admin'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    session['log'] = False
    return redirect(url_for('page',pg = 1))
@app.route('/admin')
def admin():
    if not session.get('log'):
        return redirect(url_for('login'))
    return render_template('admin.html')
@app.route('/article/<int:bg_id>')
def article(bg_id):
    data=Article().getFull(bg_id)
    if data=='0':
        abort(404)
    return render_template('article.html',data = data)
@app.route('/memo')
def memo():
    return render_template('memo.html')
@app.route('/wish')
def wish():
    return render_template('wish.html')
@app.route('/edit/<pg>')
@app.route('/edit')
def edit(pg=0):
    if not session.get('log'):
        return redirect(url_for('login'))
    data=Article().getFull(pg)
    return render_template('edit.html',data = data)
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/api/getinfo')
def getInfo():
    data=Manager().getInfo()
    return jsonify(data)
@app.route('/api/getcomment', methods=['POST'])
def getComment():
    id=request.form.get('id',type=int)
    data=Comment().getIt(id)
    return jsonify(data)
@app.route('/api/postcomment', methods=['POST'])
def commentPost():
    author = request.form.get('author')
    content = request.form.get('content')
    bid = request.form.get('bid',type=int)
    rid = request.form.get('rid',type=int)
    timestamp=request.form.get('timestamp')
    md5Str=request.form.get('md5')
    import time
    now=int(time.time())
    from hashlib import md5
    timestampMD5=md5(timestamp.encode('utf8')).hexdigest()[0:3]
    md5String=md5(md5Str.encode('utf8')).hexdigest()[0:3]
    if int(timestamp)+60>now and timestampMD5==md5String:
        data=Comment().insert(bid,content,author,rid)
        return jsonify(data)
    return jsonify('0')
@app.route('/api/postarticle', methods=['POST'])
def articlePost():
    if not session.get('log'):
        return jsonify('failed')
    title = request.form.get('title')
    abstract = request.form.get('abstract')
    content = request.form.get('content')
    img = request.form.get('img')
    file = request.form.get('file',type=int)
    tag = request.form.get('tags')
    id = request.form.get('id',type=int)
    re=Article().edit(id, title, abstract, tag, img, file, content)
    return jsonify(re)
@app.route('/api/delcomment', methods=['POST'])
def commentDel():
    if not session.get('log'):
        return jsonify('failed')
    id = request.form.get('id',type=int)
    re=Comment().delIt(id)
    return jsonify(re)
@app.route('/api/delarticle', methods=['POST'])
def articleDel():
    if not session.get('log'):
        return jsonify('failed')
    id = request.form.get('id',type=int)
    Article().hideIt(id)
    return "Success"
@app.route('/api/verify', methods = ['POST'])
def verify():
    pwd = request.form.get('pwd')
    timestamp = request.form.get('timestamp')
    md5Str = request.form.get('md5')
    import time
    now=int(time.time())
    from hashlib import md5
    timestampMD5=md5(timestamp.encode('utf8')).hexdigest()[0:4]
    md5String=md5(md5Str.encode('utf8')).hexdigest()[0:4]
    if int(timestamp)+60>now and timestampMD5==md5String and Manager().verify(pwd)=='1':
        session['log']=True
        return jsonify('1')
    return jsonify('0')