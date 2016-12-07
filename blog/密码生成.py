# -*- coding: utf-8 -*-

import hashlib
m = hashlib.md5()
pwd=raw_input()
pwd +=  '1396'
m.update(pwd)
print m.hexdigest()
raw_input()