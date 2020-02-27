from webdebug import web_debug
import pytest
import pytest_mock
import webdebug
from unittest.mock import patch

patch_start_server = patch('webdebug.core.start_server', lambda *args:...)

@patch_start_server
def test_web_debug(mocker):
	mocker.patch('webdebug.core.start_server')
	@web_debug()
	def err():
		0/0
	err()
	webdebug.core.start_server.assert_called_once()

@patch_start_server
def test_web_debug_catch(mocker,monkeypatch):
	mocker.patch('webdebug.core.start_server')

	@web_debug(catch=False)
	def err():
		0/0
	try:
		err()
	except:
		...
	webdebug.core.start_server.assert_not_called()

@patch_start_server
def test_web_debug_catch_2(mocker,monkeypatch):
	mocker.patch('webdebug.core.start_server')

	@web_debug(catch=True)
	def err():
		0/0
	try:
		err()
	except:
		...
	webdebug.core.start_server.assert_called_once()



def test_set_web_debug():
    import sys
    from subprocess import Popen, PIPE
    proc = Popen([sys.executable, 'error_code.py'], stdout=PIPE, stderr=PIPE,cwd='./')
    stdout, stderr = proc.communicate()
    print(stdout,stderr)
    assert stdout.startswith(b'called')

def test_run_as_module():
    import sys
    import time
    from subprocess import Popen, PIPE
    import requests
    import socket
    def get_open_port():

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
    port = get_open_port()
    # , stdout=PIPE, stderr=PIPE
    proc = Popen([sys.executable] +  '-m webdebug --host localhost --port {0} error_code_module.py'.format(str(port)).split(' '),cwd='./')
    time.sleep(3)
    def is_port_in_use(port):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    assert is_port_in_use(port)