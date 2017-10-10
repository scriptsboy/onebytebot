# -*- coding:utf-8 -*-

def Singleton(cls, *args, **kw):
    """
    单例模式装饰器
    """
    instance = {}
    def _singleton():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]
    return _singleton
