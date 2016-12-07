# -*- coding:utf-8 -*- 
import os,sys
from flask import Flask


#初始化配置参数
reload(sys)
sys.setdefaultencoding( "utf-8" )
app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'db.db')
SECRET_KEY = os.environ.get('SECRET_KEY') or 'foolish'
app.config.from_object(__name__)



import blog.views
