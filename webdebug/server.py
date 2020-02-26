import traceback
import threading
import ctypes
import time
# from webdebug import _DEFAULT_PIN

def start_server(ex,host,pin,port,callbacks):
    traceback.print_tb(ex.__traceback__)
    from werkzeug.debug import DebuggedApplication
    from werkzeug import Request,run_simple
    import os
    if pin:
        from . import _DEFAULT_PIN,_DEFAULT_PIN_LEN
        if pin == _DEFAULT_PIN:
            import random
            pin = ''.join((str(random.randint(0, 9)) for _ in range(_DEFAULT_PIN_LEN)))
        os.environ["WERKZEUG_DEBUG_PIN"] = pin
    os.environ["WERKZEUG_RUN_MAIN"] = 'true'

    def self_kill():
        thread_id = threading.current_thread().ident
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    @Request.application
    def app(request):
        if request.args.get('shutdown','N').upper() == 'Y':
            threading.current_thread().self_kill()
        raise ex

    app = DebuggedApplication(app, evalex=True,pin_security=True if pin else False)
    if port == 0:
        port = get_open_port()
    for cb in callbacks:
        cb(ex,host, port,pin).run()

    thread = threading.Thread(target=run_simple, args=(host, port, app))
    thread.self_kill = self_kill
    thread.start()
    while True:
        if thread.is_alive():
            time.sleep(1)
        else:
            break

def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port