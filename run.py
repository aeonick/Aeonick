# -*- coding:utf-8 -*- 
import os
from flask import Flask, render_template, session, redirect, url_for, request, g, flash, send_from_directory
import sys
import aids
import sqlite3

reload(sys)
sys.setdefaultencoding( "utf-8" )
app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'db.db')
SECRET_KEY = os.environ.get('SECRET_KEY') or 'foolish'
app.config.from_object(__name__)

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        import aids
        if aids.check(request.form['namea']):
            session['log'] = True
            return redirect(url_for('index'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    session['log'] = False
    return redirect(url_for('index'))

@app.route('/new', methods=['GET', 'POST'])
def new():
    if session.get('log'):
        if request.method == 'POST':
            if request.form['editor'] and request.form['title']:
                abstr=aids.abstr(request.form['editor'])
                cur=get_db().cursor()
                cur.execute('insert into blog (title, content, abstract, tag, file) values (?, ?, ?, ?, ?)', (request.form['title'], request.form['editor'], abstr,request.form['tags'],request.form['file'],))
                get_db().commit()
                return redirect(url_for('index'))
            elif request.form['editor']:
                flash('请填写标题')
                return render_template('edit.html',content=request.form['editor'])
        return render_template('edit.html')
    return redirect(url_for('index'))

@app.route('/edit/<int:bg_id>', methods=['GET', 'POST'])
def edit(bg_id):
    if session.get('log'):
        try:
            cur=get_db().cursor()
            cur.execute('SELECT title, content,tag from blog where id=?',(bg_id,))
            cont=cur.fetchall()[0]
        except:
            return redirect(url_for('index'))
        if request.method == 'POST':
            if request.form['editor'] and request.form['title']:
                abstr=aids.abstr(request.form['editor'])
                cur=get_db().cursor()
                cur.execute('UPDATE blog SET title = ? ,content = ?,abstract=?,tag=? ,file=? WHERE ID = ?;', (request.form['title'], request.form['editor'],abstr,request.form['tags'],request.form['file'], bg_id))
                get_db().commit()
                return redirect(url_for('article',bg_id=bg_id))
            elif request.form['editor']:
                flash('请填写标题')
                return render_template('edit.html',content=request.form['editor'])
        return render_template('edit.html',content=cont[1],title=cont[0],tags=cont[2])
    return redirect(url_for('index'))

@app.route('/dele/<int:bg_id>')
def dele(bg_id):
    if session.get('log'):
        try:
            cur=get_db().cursor()
            cur.execute('DELETE FROM blog WHERE id = ? ',(bg_id,))
            get_db().commit()
        except:
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/')
def index():
    return redirect(url_for('page',pg=1))

@app.route('/article/None')
def backnone():
    return redirect(url_for('page',pg=1))

@app.route('/page/<int:pg>')
def page(pg):
    cur=get_db().cursor()
    cur.execute(' SELECT id, title, date, abstract FROM blog ORDER BY id DESC LIMIT 8 OFFSET ?',(pg*8-8,))
    tem=cur.fetchall()
    cur.execute('SELECT count(*) FROM blog;')
    pmax=((cur.fetchall()[0][0]+7)/8 or 1)
    if pg > pmax or pg < 1:
        return render_template('error.html'), 500
    else:
        return render_template('page.html',tem=tem,pmax=pmax,pg=pg)

@app.route('/memo',methods=['GET', 'POST'])
def memo():
    if request.method == 'POST':
        if request.form['comment'] and session.get('angelina')!=50:
                session['angelina']=(session.get('angelina') or 0)+1
                author = request.form['author'] or u'匿名'
                cur=get_db().cursor()
                cur.execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comment'], author, 0))
                get_db().commit()
                return redirect(url_for('memo'))
    try:
        cur=get_db().cursor()
        cur.execute(' SELECT content, date, author, id FROM comm WHERE blog=0')
        tem=cur.fetchall()
        tem.reverse()
    except:
        return render_template('memo.html',tem=[])
    else:
        return render_template('memo.html',tem=tem)

@app.route('/article/<int:bg_id>', methods=['GET', 'POST'])
def article(bg_id):
    if request.method == 'POST':
        if request.form['comment'] and session.get('angelina')!=50:
                session['angelina']=(session.get('angelina') or 0)+1
                author = request.form['author'] or u'匿名'
                cur=get_db().cursor()
                cur.execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comment'], author, bg_id))
                get_db().commit()
                return redirect(url_for('article',bg_id=bg_id))
    try:
        cur=get_db().cursor()
        cur.execute('SELECT title, date, content from blog where id=?',(bg_id,))
        cont=cur.fetchall()[0]
    except:
        return render_template('error.html'), 404
    else:
        cur.execute(' SELECT content, date, author, id FROM comm WHERE blog=?',(bg_id,))
        tem=cur.fetchall() or [('快来发布第一条评论吧','',''),]
        return render_template('article.html',t=cont[0],d=cont[1],c=cont[2],id=bg_id,tem=tem,back=request.referrer)

@app.route('/del/<int:bg_id>/<int:ccid>')
def delet(bg_id,ccid):
    if session.get('log'):
        try:
            cur=get_db().cursor()
            cur.execute('DELETE FROM comm WHERE id = ? ',(ccid,))
            get_db().commit()
        finally:
            if not bg_id== 0 :
                return redirect(url_for('article',bg_id=bg_id))
            else:
                return redirect(url_for('memo'))
    return redirect(url_for('article',bg_id=bg_id))


@app.route('/arch<int:arc>/<int:pg>')
def arch(arc,pg):
    cur=get_db().cursor()
    cur.execute(' SELECT id, title, date, abstract FROM blog WHERE file=? ORDER BY id DESC LIMIT 8 OFFSET ?',(arc,pg*8-8))
    tem=cur.fetchall()
    cur.execute('SELECT count(*) FROM blog;')
    pmax=(cur.fetchall()[0][0]+7)/8
    if pg > pmax or pg < 1:
        return render_template('error.html'), 500
    else:
        return render_template('page.html',tem=tem,pmax=pmax,pg=pg)


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder,'robots.txt')


if __name__ == '__main__':
    app.run(debug=True)
