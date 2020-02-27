from webdebug import set_web_debug, unset_web_debug
import webdebug
def dummy(*agg):
    print('called')
webdebug.core.start_server = dummy
set_web_debug()
def err():
    0 / 0
err()