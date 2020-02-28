from webdebug import set_web_debug, unset_web_debug
import webdebug
import sys
exclude_dic = {'ZeroDivisionError':(ZeroDivisionError,),
               'ValueError':(ValueError,),
               'None':()}
def dummy(*agg):
    print('called')
webdebug.core.start_server = dummy
set_web_debug(exclude=exclude_dic[sys.argv[1]])
def err():
    0 / 0
err()