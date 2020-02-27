import sys
import time
from subprocess import Popen, PIPE
import requests
import socket
import pdb


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()

    return port

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

port = get_open_port()
print('-m webdebug --host localhost --port {0} error_code_module.py'.format(str(port)))
proc = Popen([sys.executable] +  '-m webdebug --host localhost --port {0} error_code_module.py'.format(str(port)).split(' '),
             # stdout=PIPE, stderr=PIPE,
             cwd='./')
pdb.set_trace()
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(("localhost", port))
