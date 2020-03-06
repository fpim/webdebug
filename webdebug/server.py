import traceback
import threading
import ctypes
import time
from .config import _DEFAULT_PORT, _DEFAULT_PIN, _DEFAULT_HOST
import socket

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

    if is_port_in_use(port):
         print(str(port) + ' is in use, cannot setup debugger.')
         raise ex
    else:
        for cb in callbacks:
            cb.load_exception(ex, host, port, pin)
            cb.run()

        def log_startup(sock):
            from werkzeug._internal import _log
            try:
                af_unix = socket.AF_UNIX
            except AttributeError:
                af_unix = None

            display_hostname = host if host not in ("", "*") else "localhost"
            quit_msg = "(Press CTRL+C to quit)"
            if sock.family == af_unix:
                _log("info", " * Running on %s %s", display_hostname, quit_msg)
            else:
                if ":" in display_hostname:
                    display_hostname = "[%s]" % display_hostname
                port = sock.getsockname()[1]
                _log(
                    "info",
                    " * Running on %s://%s:%d/ %s",
                    "http",
                    display_hostname,
                    port,
                    quit_msg,
                )

        try:
            fd = int(os.environ['WERKZEUG_SERVER_FD'])
        except (LookupError, ValueError):
            fd = None
        srv = make_server(host, port, app, threaded=False, processes=1,
                          request_handler=None, passthrough_errors=False,
                          ssl_context=None,
                          fd=fd)
        if fd is None:
            log_startup(srv.socket)
        srv.serve_forever()
        raise ex

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_open_port():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port