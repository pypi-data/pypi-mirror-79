"""

@FileName: wrappers.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 13:49
@Descriptions: 

"""


# adb装饰器
def adb_wrapper(func):
    def wrapper(*args, **kwargs):
        u = func()
        return u

    return wrapper()


# 单例模式
def singleton(cls):
    _instance = {}

    def inner(*args, **kw):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kw)
        return _instance[cls]

    return inner


def singleton2(cls, *args, **kw):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls(*args, **kw)
        return _instance[cls]

    return inner
