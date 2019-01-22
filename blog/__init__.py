# -*- coding:utf-8 -*-
import os
from flask import Flask

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'db.db')
app.config.from_object(__name__)

import blog.views
