import sys
from .server import start_server
from .callback import *
from functools import partial,wraps
import os
from .config import _DEFAULT_PIN,_DEFAULT_HOST,_DEFAULT_PIN_LEN,_DEFAULT_PORT
_original_excepthook = sys.excepthook

def _validation(host,pin,port,callbacks,exclude):
    for cb in callbacks:
        if not isinstance(cb, BaseCallBack):
            raise ValueError(str(cb) + ' is not subclass of webdebug.callback.BaseCallBack')
    if not isinstance(exclude,tuple):
        raise ValueError('Argument "exclude" must be tuple of exception type')
    for e in exclude:
        if not issubclass(e,Exception):
            raise ValueError('Argument "exclude" must be tuple of exception type')
    if not isinstance(port,int):
        raise ValueError('port must be int.')

def set_web_debug(host=_DEFAULT_HOST ,pin=_DEFAULT_PIN,port=_DEFAULT_PORT,callbacks=[],exclude=()):
    if os.environ.get('webdebug','true') == 'true':
        _validation(host,pin,port,callbacks,exclude)
        sys.excepthook = partial(__web_excepthook, host=host, pin=pin, port=port, callbacks=callbacks,exclude=exclude)

def unset_web_debug():
    if os.environ.get('webdebug','true') == 'true':
        sys.excepthook = _original_excepthook

def __web_excepthook(exc_type, exc_value, tb, host, pin, port, callbacks,exclude):
    if not issubclass(exc_type,exclude):
        start_server(exc_type(exc_value).with_traceback(tb),host,pin,port,callbacks)
    _original_excepthook(exc_type, exc_value, tb)

def web_debug(catch=True,host=_DEFAULT_HOST,pin=_DEFAULT_PIN,port=_DEFAULT_PORT,callbacks=[],exclude=()):
    _validation(host, pin, port, callbacks,exclude)
    def wrapper(fn):
        if os.environ.get('webdebug', 'true') == 'true':
            if catch:
                @wraps(fn)
                def warpped(*args, **kwargs):
                    result = None
                    try:
                        result = fn(*args, **kwargs)
                    except Exception as ex:
                        if isinstance(ex,exclude):
                            raise ex
                        else:
                            start_server(ex,host,pin,port,callbacks)
                    return result
                return warpped
            else:
                @wraps(fn)
                def warpped(*args, **kwargs):
                    result = None
                    set_web_debug(host, pin, port, callbacks,exclude)
                    result = fn(*args, **kwargs)
                    unset_web_debug()
                    return result
                return warpped
        else:
            return fn
    if isinstance(catch,bool):
        return wrapper
    else:
        return wrapper(catch)


_usage = """
usage: [-m webdebug | pyfile] [arg] ...
"""





