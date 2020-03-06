from webdebug import web_debug
import pytest
import pytest_mock
import webdebug
from unittest.mock import patch
import sys

patch_start_server = patch('webdebug.core.start_server', lambda *args: ...)


@patch_start_server
def test_web_debug(mocker):
    mocker.patch('webdebug.core.start_server')

    @web_debug()
    def err():
        0 / 0

    err()


    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_called_once()

@patch_start_server
def test_web_debug_exclude_other_exception(mocker):
    mocker.patch('webdebug.core.start_server')

    @web_debug(exclude=(ValueError,))
    def err():
        0 / 0

    err()


    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_called_once()

@patch_start_server
def test_web_debug_exclude(mocker):
    mocker.patch('webdebug.core.start_server')

    @web_debug(exclude=(ZeroDivisionError,))
    def err():
        0 / 0

    with pytest.raises(ZeroDivisionError):
        err()

    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_not_called()



@patch_start_server
def test_web_debug_catch_env_false(mocker, monkeypatch):
    mocker.patch('webdebug.core.start_server')
    monkeypatch.setenv("webdebug", "false")
    @web_debug(catch=True)
    def err():
        0 / 0

    try:
        err()
    except:
        ...
    webdebug.core.start_server.assert_not_called()


@patch_start_server
def test_web_debug_as_wrapper(mocker):
    mocker.patch('webdebug.core.start_server')

    @web_debug
    def err():
        0 / 0

    err()


    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_called_once()

@patch_start_server
def test_web_debug_catch(mocker, monkeypatch):
    mocker.patch('webdebug.core.start_server')

    @web_debug(catch=False)
    def err():
        0 / 0

    try:
        err()
    except:
        ...
    webdebug.core.start_server.assert_not_called()


@patch_start_server
def test_web_debug_catch_2(mocker, monkeypatch):
    mocker.patch('webdebug.core.start_server')

    @web_debug(catch=True)
    def err():
        0 / 0

    try:
        err()
    except:
        ...
    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_called_once()

@patch_start_server
def test_web_debug_catch_2_exclude(mocker, monkeypatch):
    mocker.patch('webdebug.core.start_server')

    @web_debug(catch=True,exclude=(ZeroDivisionError,))
    def err():
        0 / 0

    try:
        err()
    except:
        ...
    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_not_called()

@patch_start_server
def test_web_debug_context_manager(mocker, monkeypatch):
    mocker.patch('webdebug.core.start_server')
    with pytest.raises(ZeroDivisionError):
        with web_debug:
            0/0
    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_called_once()

@patch_start_server
def test_web_debug_context_manager_env_false(mocker, monkeypatch):
    mocker.patch('webdebug.core.start_server')
    monkeypatch.setenv("webdebug", "false")
    with pytest.raises(ZeroDivisionError):
        with web_debug:
            0/0
    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_not_called()


@patch_start_server
def test_web_debug_context_manager_called(mocker, monkeypatch):
    mocker.patch('webdebug.core.start_server')
    with pytest.raises(ZeroDivisionError):
        with web_debug():
            0/0
    if sys.version_info >= (3, 6):
        webdebug.core.start_server.assert_called_once()

def test_set_web_debug_env_false():
    import sys
    from subprocess import Popen, PIPE
    import os
    my_env = os.environ.copy()
    my_env["webdebug"] = "false"
    proc = Popen([sys.executable, 'error_code.py', 'None'], stdout=PIPE, stderr=PIPE, cwd='./', env=my_env)
    stdout, stderr = proc.communicate()
    print(stdout, stderr)
    assert not stdout.startswith(b'called')

def test_set_web_debug():
    import sys
    from subprocess import Popen, PIPE
    proc = Popen([sys.executable, 'error_code.py', 'None'], stdout=PIPE, stderr=PIPE, cwd='./')
    stdout, stderr = proc.communicate()
    print(stdout, stderr)
    assert stdout.startswith(b'called')

def test_set_web_debug_ValueError():
    import sys
    from subprocess import Popen, PIPE
    proc = Popen([sys.executable, 'error_code.py', 'ValueError'], stdout=PIPE, stderr=PIPE, cwd='./')
    stdout, stderr = proc.communicate()
    print(stdout, stderr)
    assert stdout.startswith(b'called')


def test_set_web_debug_ZeroDivisionError():
    import sys
    from subprocess import Popen, PIPE
    proc = Popen([sys.executable, 'error_code.py', 'ZeroDivisionError'], stdout=PIPE, stderr=PIPE, cwd='./')
    stdout, stderr = proc.communicate()
    print(stdout, stderr)
    assert not stdout.startswith(b'called')


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
    proc = Popen(
        [sys.executable] + '-m webdebug --host localhost --port {0} error_code_module.py'.format(str(port)).split(' '),
        cwd='./')
    time.sleep(1.5)

    def is_port_in_use(port):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    assert is_port_in_use(port)


@pytest.mark.timeout(5, method='signal')
def test_web_debug_shutdown():
    import threading
    import time
    import requests
    def shutdown():
        time.sleep(3)
        requests.get('http://localhost:54545?shutdown=Y',timeout=4)
    th = threading.Thread(target=shutdown)
    th.start()
    with pytest.raises(ZeroDivisionError):
        with web_debug(port=54545):
            0/0
    th.join()

@pytest.mark.timeout(5, method='signal')
def test_web_debug_shutdown_DEFAULT_PORT():
    import threading
    import time
    import requests
    from webdebug.config import _DEFAULT_PORT
    def shutdown():
        time.sleep(3)
        requests.get('http://localhost:{0}?shutdown=Y'.format(str(_DEFAULT_PORT)),timeout=4)
    th = threading.Thread(target=shutdown)
    th.start()
    with pytest.raises(ZeroDivisionError):
        with web_debug:
            0/0
    th.join()
