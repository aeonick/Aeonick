# -*- coding:utf-8 -*- 
import os
from flask import Flask, render_template, session, redirect, url_for, request, g, flash, send_from_directory
import sys
import sqlite3
import aids

#初始化设置
reload(sys)
sys.setdefaultencoding( "utf-8" )
app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'db.db')
SECRET_KEY = os.environ.get('SECRET_KEY') or 'foolish'
app.config.from_object(__name__)

#数据库链接模块
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

#笨办法手动加盐验证密码
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        import aids
        if aids.check(request.form['password']):
            session['log'] = True
            return redirect(url_for('index'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    session['log'] = False
    return redirect(url_for('index'))

#博客编辑模块
@app.route('/new', methods=['GET', 'POST'])
def new():
    if session.get('log'):
        if request.method == 'POST':
            if request.form['editor'] and request.form['title']:
                abstract=aids.abstr(request.form['editor'])
                #偷懒写一块了,file即分类编号（历史遗留问题）
                get_db().execute('insert into blog (title, content, abstract, tag, file) values (?, ?, ?, ?, ?)', (request.form['title'], request.form['editor'], abstract,request.form['tags'],request.form['file'],))
                get_db().commit()
                return redirect(url_for('index'))
            elif request.form['editor']:
                flash('请填写标题')
                return render_template('edit.html',content=request.form['editor'])
        return render_template('edit.html')
    return redirect(url_for('index'))
@app.route('/edit/<int:blog>', methods=['GET', 'POST'])
def edit(blog):
    if session.get('log'):
        try:
            temp=get_db().execute('SELECT title, content,tag from blog where id=?',(blog,)).fetchall()[0]
        except:
            return redirect(url_for('index'))
        if request.method == 'POST':
            if request.form['editor'] and request.form['title']:
                abstract=aids.abstr(request.form['editor'])
                get_db().execute('UPDATE blog SET title = ? ,content = ?,abstract=?,tag=? ,file=? WHERE ID = ?;', (request.form['title'], request.form['editor'],abstract,request.form['tags'],request.form['file'], blog))
                get_db().commit()
                return redirect(url_for('article',blog=blog))
            elif request.form['editor']:
                flash('请填写标题')
                return render_template('edit.html',content=request.form['editor'])
        return render_template('edit.html',content=temp[1],title=temp[0],tags=temp[2])
    return redirect(url_for('index'))


@app.route('/delb/<int:blog>')
def del_blog(blog):
    if session.get('log'):
        try:
            get_db().execute('DELETE FROM blog WHERE id = ? ',(blog,))
            get_db().commit()
        except:
            return redirect(url_for('index'))
    return redirect(url_for('index'))
@app.route('/delc/<int:blog>/<int:c_id>')
def del_comment(blog,c_id):
    if session.get('log'):
        try:
            get_db().execute('DELETE FROM comm WHERE id = ? ',(c_id,))
            get_db().commit()
        finally:
            if blog == 0 :
                return redirect(url_for('memo'))
            else:
                return redirect(url_for('article',blog=blog))
    return redirect(url_for('article',blog=blog))

@app.route('/')
def index():
    return redirect(url_for('page',pg=1))

@app.route('/article/None')
def back_to_index():
    return redirect(url_for('page',pg=1))

@app.route('/page/<int:pg>')
def page(pg):
    temp=get_db().execute('SELECT id, title, date, abstract FROM blog ORDER BY id DESC LIMIT 8 OFFSET ?',(pg*8-8,)).fetchall()
    max_pg=((get_db().execute('SELECT count(*) FROM blog;').fetchall()[0][0]+7)/8) or 1
    if pg > max_pg or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',temp=temp,max_pg=max_pg,pg=pg)

@app.route('/memo',methods=['GET', 'POST'])
def memo():
    if request.method == 'POST':
        if request.form['comment']:
                author = request.form['author'] or u'匿名'
                get_db().execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comment'], author, 0))
                get_db().commit()
                return redirect(url_for('memo'))
    try:
        temp=get_db().execute(' SELECT content, date, author, id FROM comm WHERE blog=0').fetchall()
        temp.reverse()
    except:
        return render_template('memo.html',temp=[])
    else:
        return render_template('memo.html',temp=temp)

@app.route('/article/<int:blog>', methods=['GET', 'POST'])
def article(blog):
    if request.method == 'POST':
        if request.form['comment']:
                author = request.form['author'] or u'匿名'
                get_db().execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comment'], author, blog))
                get_db().commit()
                return redirect(url_for('article',blog=blog))
    try:
        temp=get_db().execute('SELECT title, date, content from blog where id=?',(blog,)).fetchall()[0]
    except:
        return render_template('error.html'), 404
    else:
        tem=get_db().execute(' SELECT content, date, author, id FROM comm WHERE blog=?',(blog,)).fetchall() or [('快来发布第一条评论吧','',''),]
        return render_template('article.html',t=temp[0],d=temp[1],c=temp[2],id=blog,tem=tem,back=request.referrer)

@app.route('/arch<int:arc>/<int:pg>')
def arch(arc,pg):
    temp=get_db().execute(' SELECT id, title, date, abstract FROM blog WHERE file=? ORDER BY id DESC LIMIT 8 OFFSET ?',(arc,pg*8-8)).fetchall()
    max_pg=(get_db().execute('SELECT count(*) FROM blog;').fetchall()[0][0]+7)/8
    if pg > max_pg or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',temp=temp,max_pg=max_pg,pg=pg)


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder,'robots.txt')

if __name__ == '__main__':
    app.run(debug=True)
