# -*- coding:utf-8 -*-
from hashlib import sha1
import hmac
import base64
import datetime
import time
import os


def getToken():
    AK = os.environ.get('AK') or ''#七牛Access Key，推荐写入环境变量
    SK = os.environ.get('SK') or '' #七牛Secret Key，推荐写入环境变量
    dl=int(time.mktime(datetime.datetime.now().timetuple()))+21600
    s='{"scope":"BUCKET","deadline":%s}'%(dl,) #BUCKET填自己存储空间bucket的名字
    s=base64.urlsafe_b64encode(s)
    sign=hmac.new(SK,s,sha1).digest()
    sign = base64.urlsafe_b64encode(sign)
    token = AK + ':' + sign + ':' + s
    return token
