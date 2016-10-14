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
        if aids.check(request.form['passwd']):
            session['log'] = True
            return redirect(url_for('new'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    session['log'] = False
    return redirect(url_for('page',pg=1))

@app.route('/new', methods=['GET', 'POST'])
def new():
    if session.get('log'):
        if request.method == 'POST':
            if request.form['editor'] and request.form['title']:
                abstr=aids.abstr(request.form['editor'],request.form['img'])
                cur=get_db().cursor()
                tags=(request.form['tags'] or '').replace('，',',')
                cur.execute('insert into blog (title, content, abstract, tag, file) values (?, ?, ?, ?, ?)', (request.form['title'], request.form['editor'], abstr,tags,request.form['file'],))
                get_db().commit()
                cur.execute('select id from blog order by id desc limit 1')
                blog=cur.fetchall()
                blog=blog[0][0]
                tags=tags.split(',')
                for tag in tags:
                    cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, blog))
                get_db().commit()
                return redirect(url_for('page',pg=1))
            elif request.form['editor']:
                return render_template('edit.html',content=request.form['editor'],img=request.form['img'])
        return render_template('edit.html')
    return redirect(url_for('page',pg=1))

@app.route('/edit/<int:bg_id>', methods=['GET', 'POST'])
def edit(bg_id):
    if session.get('log'):
        try:
            cur=get_db().cursor()
            cur.execute('SELECT title, content,tag from blog where id=?',(bg_id,))
            cont=cur.fetchall()[0]
        except:
            return redirect(url_for('page',pg=1))
        if request.method == 'POST':
            if request.form['editor'] and request.form['title']:
                abstr=aids.abstr(request.form['editor'],request.form['img'])
                cur=get_db().cursor()
                tags=(request.form['tags'] or '').replace('，',',')
                cur.execute('UPDATE blog SET title = ? ,content = ?,abstract=?,tag=? ,file=? WHERE ID = ?;', (request.form['title'], request.form['editor'],abstr,tags,request.form['file'], bg_id))
                get_db().commit()
                cur.execute('delete from tag where blog = ?',(bg_id,))
                tags=tags.split(',')
                for tag in tags:
                    cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, bg_id))
                get_db().commit()
                return redirect(url_for('article',bg_id=bg_id))
            elif request.form['editor']:
                return render_template('edit.html',content=request.form['editor'],tags=cont[2],img=request.form['img'])
        return render_template('edit.html',content=cont[1],title=cont[0],tags=cont[2])
    return redirect(url_for('page',pg=1))

@app.route('/dele/<int:bg_id>')
def dele(bg_id):
    if session.get('log'):
        try:
            cur=get_db().cursor()
            cur.execute('DELETE FROM blog WHERE id = ? ',(bg_id,))
            cur.execute('DELETE FROM tag WHERE blog = ? ',(bg_id,))
            cur.execute('DELETE FROM comm WHERE blog = ? ',(bg_id,))
            get_db().commit()
        except:
            return redirect(url_for('page',pg=1))
    return redirect(url_for('page',pg=1))

@app.route('/')
def index():
    cur=get_db().cursor()
    cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog ORDER BY id DESC LIMIT 8')
    tem=cur.fetchall()
    cur.execute('SELECT count(*) FROM blog;')
    pmax=((cur.fetchall()[0][0]+7)/8 or 1)
    if False:
        session['new']=True
        return render_template('index.html',tem=tem,pmax=pmax,pg=1)
    else:
        return render_template('index.html',tem=tem,pmax=pmax,pg=1)

@app.route('/article/None')
def backnone():
    return redirect(url_for('page',pg=1))

@app.route('/page/<int:pg>')
def page(pg):
    cur=get_db().cursor()
    cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog ORDER BY id DESC LIMIT 8 OFFSET ?',(pg*8-8,))
    tem=cur.fetchall()
    cur.execute('SELECT count(*) FROM blog;')
    pmax=((cur.fetchall()[0][0]+7)/8 or 1)
    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',tem=tem,pmax=pmax,pg=pg)

@app.route('/memo',methods=['GET', 'POST'])
def memo():
    if request.method == 'POST':
        if request.form['comment']:
                author = request.form['author'] or u'访客'
                cur=get_db().cursor()
                cur.execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comment'], author, 0))
                get_db().commit()
                return redirect(url_for('memo'))
    try:
        cur=get_db().cursor()
        cur.execute('SELECT content, date, author, id FROM comm WHERE blog=0')
        tem=cur.fetchall()
        tem.reverse()
    except:
        return render_template('memo.html',tem=[])
    else:
        return render_template('memo.html',tem=tem)

@app.route('/article/<int:bg_id>', methods=['GET', 'POST'])
def article(bg_id):
    if request.method == 'POST':
        if request.form['comment']:
                author = request.form['author'] or u'访客'
                cur=get_db().cursor()
                cur.execute('insert into comm (content, author, blog, reply) values (?, ?, ?, ?)', (request.form['comment'], author, bg_id, request.form['reply'] or None))
                get_db().commit()
                return redirect(url_for('article',bg_id=bg_id))
    try:
        cur=get_db().cursor()
        cur.execute('SELECT title, date, content, tag, abstract from blog where id=?',(bg_id,))
        cont=cur.fetchall()[0]
    except:
        return render_template('error.html'), 404
    else:
        cur.execute(' SELECT content, date, author,id,reply FROM comm WHERE blog=? ORDER BY id DESC',(bg_id,))
        tem=cur.fetchall() or []
        tem=list(tem)
        tem=map(lambda x:list(x),tem)
        idli=map(lambda x:x[3],tem)
        t=0
        while t < len(tem):
            if type(tem[t][4]) == int:
                try:
                    reid = idli.index(tem[t][4])
                    tem[reid][4]=tem[reid][4] or []
                    tem[reid][4].insert(0,tem[t])
                    tem.pop(t)
                    idli.pop(t)
                    t -= 1
                finally:
                    pass
            t += 1
        return render_template('article.html',cont=cont,id=bg_id,tem=tem)

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
    cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog WHERE file=? ORDER BY id DESC LIMIT 8 OFFSET ?',(arc,pg*8-8,))
    tem=cur.fetchall()
    try:
        cur.execute('SELECT count(*) FROM blog WHERE file=?;',(arc,))
        pmax=(cur.fetchall()[0][0]+7)/8
    finally:
        pmax=pmax or 1
    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',tem=tem,pmax=pmax,pg=pg)

@app.route('/arch/<tag>/<int:pg>')
def tag(tag,pg):
    cur=get_db().cursor()
    cur.execute('select blog from tag where tag=? LIMIT 8 OFFSET ?',(tag,pg*8-8))
    tem=cur.fetchall()
    blogs=map(lambda x: int(x[0]),tem)
    blogs.sort(reverse=True)
    tem=[]
    item=0
    for blog in blogs:
        cur.execute(' SELECT id, title, abstract,tag,date,file FROM blog WHERE id=?',(blog,))
        tem.append(cur.fetchall()[0])
    try:
        cur.execute('SELECT count(*) FROM tag WHERE tag=?;',(tag,))
        pmax=(cur.fetchall()[0][0]+7)/8
    finally:
        pmax=pmax or 1
    if pg > pmax or pg < 1:
        return render_template('error.html'), 404
    else:
        return render_template('page.html',tem=tem,pmax=pmax,pg=pg)

@app.route('/heal')
def heal():
    cur=get_db().cursor()
    cur.execute('delete from tag')
    cur.execute('SELECT id,tag from blog')
    cont=cur.fetchall()
    for connn in cont:
        tags=connn[1]
        bg_id=connn[0]
        tags=tags.split(',')
        for tag in tags:
            cur.execute('insert into tag (tag, blog) values (?, ?)', (tag, bg_id))
        get_db().commit()
    return redirect(url_for('page',pg=1))












@app.route('/admin')
def admin():
    if session.get('log'):
        cur=get_db().cursor()
        cur.execute(' SELECT content, author, date,blog FROM comm ORDER BY id DESC')
        tem=cur.fetchall()
        return render_template('admin.html',tem=tem)
    else:
        return redirect(url_for('login'))

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/wish',methods=['GET', 'POST'])
def wish():
    if request.method == 'POST':
        flash('许愿池收到了你的愿望,祝你好运！')
        if request.form['comments']:
                author = request.form['authors'] or u'访客'
                cur=get_db().cursor()
                cur.execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['comments'], author, -1))
                get_db().commit()
                return render_template('wish.html')
        if request.form['commentm']:
                author = request.form['authorm'] or u'访客'
                cur=get_db().cursor()
                cur.execute('insert into comm (content, author, blog) values (?, ?, ?)', (request.form['commentm'], author, -2))
                get_db().commit()
                return render_template('wish.html')
    return render_template('wish.html')



if __name__ == '__main__':
    app.run(debug=True)
