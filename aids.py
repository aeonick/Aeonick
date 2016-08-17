# -*- coding:utf-8 -*-

def check(pasword):
    import hashlib
    m = hashlib.md5()
    if not pasword:
        pasword = ''
    else:
        pasword += '1396'
    m.update(pasword)
    if m.hexdigest()=='9bd414e8c3cdd92cc9df53cc5a2f98dc':
        return True
    else:
        return False

def abstr(text):
    sta=0
    while sta<len(text) and sta < 180:
        if text[sta] == '<':
            end = sta
            while not text[end] == '>':
                end += 1
            if (text[sta:sta+3] == '''</p''' or text[sta:sta+3] == '''</h''' or text[sta:sta+6] == '''</bloc''') and text[sta-4:sta]!='<br>':
                text=text[0:sta]+'<br>'+text[end+1:]
                sta += 2
            elif text[sta:sta+4] == '''<img''':
                sta += 1
            else:
                text=text[0:sta]+text[end+1:]
            sta -= 1
        sta += 1
    text = text[:160]+'...'
    return text
