import hashlib


def md5(str_):
    t = hashlib.md5()
    t.update(str_.encode('utf8'))
    return t.hexdigest()