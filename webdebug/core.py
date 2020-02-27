import sys
from .server import start_server
from .callback import *
from functools import partial,wraps
import os
_DEFAULT_PORT = 59613
_DEFAULT_HOST = 'localhost'
_DEFAULT_PIN = '<random>'
_DEFAULT_PIN_LEN = 6
_original_excepthook = sys.excepthook

def _validation(host,pin,port,callbacks):
    for cb in callbacks:
        if not (isinstance(cb, type) and issubclass(cb, BaseCallBack)):
            raise ValueError(str(cb) + ' is not subclass of webdebug.callback.BaseCallBack')
    if not isinstance(port,int):
        raise ValueError('port must be int.')

def set_web_debug(host=_DEFAULT_HOST ,pin=_DEFAULT_PIN,port=_DEFAULT_PORT,callbacks=[]):
    if os.environ.get('webdebug','true') == 'true':
        _validation(host,pin,port,callbacks)
        sys.excepthook = partial(__web_excepthook, host=host, pin=pin, port=port, callbacks=callbacks)

def unset_web_debug():
    if os.environ.get('webdebug','true') == 'true':
        sys.excepthook = _original_excepthook

def __web_excepthook(exc_type, exc_value, tb, host, pin, port, callbacks):
    start_server(exc_type(exc_value).with_traceback(tb),host,pin,port,callbacks)
    _original_excepthook(exc_type, exc_value, tb)

def web_debug(catch=True,host=_DEFAULT_HOST,pin=_DEFAULT_PIN,port=_DEFAULT_PORT,callbacks=[]):
    _validation(host, pin, port, callbacks)
    def wrapper(fn):
        if os.environ.get('webdebug', 'true') == 'true':
            if catch:
                @wraps(fn)
                def warpped(*args, **kwargs):
                    result = None
                    try:
                        result = fn(*args, **kwargs)
                    except Exception as ex:
                        start_server(ex,host,pin,port,callbacks)
                    return result
                return warpped
            else:
                @wraps(fn)
                def warpped(*args, **kwargs):
                    result = None
                    set_web_debug(host, pin, port, callbacks)
                    result = fn(*args, **kwargs)
                    unset_web_debug()
                    return result
                return warpped
        else:
            return fn
    return wrapper


_usage = """
usage: [-m webdebug | pyfile] [arg] ...
"""





