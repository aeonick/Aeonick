# -*- coding:utf-8 -*- 
import os
from flask import Flask, render_template, session, redirect, url_for, request, g, flash
import sys
import sqlite3
import aids
reload(sys)
sys.setdefaultencoding( "utf-8" )

app = Flask(__name__)

DATABASE = os.path.join(app.root_path, 'db.db')
SECRET_KEY = 'foolish'
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
            if request.form['editor'] and request.form['titl']:
                abstr=aids.abstr(request.form['editor'])
                get_db().execute('insert into blog (title, content, abstract) values (?, ?, ?)', (request.form['titl'], request.form['editor'], abstr))
                get_db().commit()
                return redirect(url_for('index'))
            elif request.form['editor']:
                flash('请填写标题')
                return render_template('edit.html',saave=request.form['editor'])
        return render_template('edit.html')
    return redirect(url_for('index'))
@app.route('/edit/<int:bg>', methods=['GET', 'POST'])
def edit(bg):
    if session.get('log'):
        try:
            cont=get_db().execute('SELECT title, content from blog where id=?',(bg,)).fetchall()[0]
        except:
            return redirect(url_for('index'))
        if request.method == 'POST':
            if request.form['editor'] and request.form['titl']:
                abstr=aids.abstr(request.form['editor'])
                get_db().execute('UPDATE blog SET title = ? ,content = ?,abstract=? WHERE ID = ?;', (request.form['titl'], request.form['editor'],abstr, bg))
                get_db().commit()
                return redirect(url_for('article',bg_id=bg))
            elif request.form['editor']:
                flash('请填写标题')
                return render_template('edit.html',saave=request.form['editor'])
        return render_template('edit.html',saave=cont[1],title=cont[0])
    return redirect(url_for('index'))
@app.route('/dele/<int:bg>')
def dele(bg):
    if session.get('log'):
        try:
            get_db().execute('DELETE FROM blog WHERE id = ? ',(bg,))
            get_db().commit()
        except:
            return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/article/None')
def backnone():
    return redirect(url_for('page',pg=1))


@app.route('/page/<int:pg>')
def page(pg):
    tem=get_db().execute(' SELECT id, title, date, abstract FROM blog ORDER BY id DESC LIMIT 8 OFFSET ?',(pg*8-8,)).fetchall()
    nu=(get_db().execute('SELECT count(*) FROM blog;').fetchall()[0][0]+7)/8
    if pg > nu or pg < 1:
        return render_template('error.html'), 500
    else:
        return render_template('page.html',tem=tem,nu=nu,pg=pg)

@app.route('/memo',methods=['GET', 'POST'])
def memo():
    if request.method == 'POST':
        if request.form['comment']:
                author = request.form['author'] or u'匿名'
                get_db().execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comment'], author, 0))
                get_db().commit()
                return redirect(url_for('memo'))
    try:
        tem=get_db().execute(' SELECT content, date, author, id FROM comm WHERE blog=0').fetchall()
        tem.reverse()
    except:
        return render_template('memo.html',id=0,tem=[])
    else:
        return render_template('memo.html',id=0,tem=tem)



@app.route('/article/<int:bg_id>', methods=['GET', 'POST'])
def article(bg_id):
    if request.method == 'POST':
        if request.form['comment']:
                author = request.form['author'] or u'匿名'
                get_db().execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comment'], author, bg_id))
                get_db().commit()
                return redirect(url_for('article',bg_id=bg_id))
    try:
        cont=get_db().execute('SELECT title, date, content from blog where id=?',(bg_id,)).fetchall()[0]
    except:
        return render_template('error.html'), 404
    else:
        tem=get_db().execute(' SELECT content, date, author, id FROM comm WHERE blog=?',(bg_id,)).fetchall() or [('快来发布第一条评论吧','',''),]
        return render_template('article.html',t=cont[0],d=cont[1],c=cont[2],id=bg_id,tem=tem,back=request.referrer)


@app.route('/del/<int:bg>/<int:ccid>')
def delet(bg,ccid):
    if session.get('log'):
        try:
            get_db().execute('DELETE FROM comm WHERE id = ? ',(ccid,))
            get_db().commit()
        finally:
            if not bg== 0 :
                return redirect(url_for('article',bg_id=bg))
            else:
                return redirect(url_for('memo'))
    return redirect(url_for('article',bg_id=bg))




if __name__ == '__main__':
    app.run()
