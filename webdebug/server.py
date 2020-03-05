import traceback
import threading
import ctypes
import time
from .config import _DEFAULT_PORT, _DEFAULT_PIN, _DEFAULT_HOST


def start_server(ex, host=_DEFAULT_HOST, pin=_DEFAULT_PIN, port=_DEFAULT_PORT, callbacks=[]):
    traceback.print_tb(ex.__traceback__)
    from werkzeug.debug import DebuggedApplication
    from werkzeug import Request, run_simple, Response
    from werkzeug.serving import make_server
    import os
    if pin:
        from .core import _DEFAULT_PIN, _DEFAULT_PIN_LEN
        if pin == _DEFAULT_PIN:
            import random
            pin = ''.join((str(random.randint(0, 9)) for _ in range(_DEFAULT_PIN_LEN)))
        os.environ["WERKZEUG_DEBUG_PIN"] = pin
    os.environ["WERKZEUG_RUN_MAIN"] = 'true'

    @Request.application
    def app(request):
        if request.args.get('ping', 'N').upper() == 'Y':
            return Response("ok")
        if request.args.get('shutdown', 'N').upper() == 'Y':
            # func = request.environ.get('werkzeug.server.shutdown')
            # if func is None:
            #     raise RuntimeError('Not running with the Werkzeug Server')
            # func()
            srv._BaseServer__shutdown_request = True
            return Response('Shutdown!')
        else:
            raise ex

    app = DebuggedApplication(app, evalex=True, pin_security=True if pin else False)

    if port == 0:
        port = get_open_port()
    for cb in callbacks:
        cb.load_exception(ex, host, port, pin)
        cb.run()

    try:
        fd = int(os.environ['WERKZEUG_SERVER_FD'])
    except (LookupError, ValueError):
        fd = None
    srv = make_server(host, port, app, threaded=False, processes=1,
                      request_handler=None, passthrough_errors=False,
                      ssl_context=None,
                      fd=fd)

    th = threading.Thread(target=srv.serve_forever)
    th.start()
    while th.isAlive():
        time.sleep(1)
    raise ex


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port