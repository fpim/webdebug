# webdebug
[![Build Status](https://travis-ci.com/fpim/webdebug.svg?branch=master)](https://travis-ci.com/fpim/webdebug)

Make werkzeug's interactive debugger available in two lines of code.

Have you always wished to have better debugging experience with python? We all know how frustrating it is to
have your long running tasks throwing error, unhandled, leaving you clueless with a bunch of meaningless trace stack.

`webdebug` is to solver the problem by the following work flow:

 > - Run your python code > unhandled exception > set-up `werkzeug` debug wep app > trigger notification (optional) > you debug interactively

![screen](https://raw.githubusercontent.com/fpim/webdebug/master/screen1.png)
![screen2](https://raw.githubusercontent.com/fpim/webdebug/master/screen2.png)

## Installation

`pip install webdebug`

## werkzeug debugger

**wendebug** simply makes **werkzeug debugger** available to your python scripts. For more information, please visit
[werkzeug's documentation](https://werkzeug.palletsprojects.com/en/1.0.x/debug/)

## Use

> **WARNING**: Do not, do not, and do not X 1,000 times, use this in production environments which is connect to the
> external, because the debugger allow arbitrary code execution.

### 1. Run as mudule

Usage: `python -m webdebug [--host] address [--port] port [--pin] pin your_python_file.py`

> `$ python -m webdebug your_python_script.py`

or

> `$ python -m webdebug --host localhost --port 54321 --pin 12345 your_python_script.py`

It's that easy! Now that your script will stop and host a werkzeug debugger in case of unhandled exception.

### 2. Enable web debug in you script

```python
from webdebug import set_web_debug,unset_web_debug

set_web_debug()
0 / 0

#or

set_web_debug(host='localhost' ,pin='12345',port='54321',callbacks=[])
0 / 0

# to un-set web debug use:

unset_web_debug()

```

### 3. Function decorator

```python
from webdebug import web_debug

@web_debug
def err():
    0 / 0

# or

@web_debug()
def err():
    0 / 0

# or

@web_debug(catch=True,host='localhost',pin='12345',port='54321',callbacks=[])
def err():
    0 / 0
 
err()

* Debugger is active!
```
Behavior of argument `catch`:

The following will trigger webdebug:
```python
@web_debug(catch=True)
def err():
    0 / 0

try:
    err()
except:
    ...

* Debugger is active!
```

and the following will not
```python
@web_debug(catch=False)
def err():
    0 / 0

try:
    err()
except:
    ...

# nothing happens
```

## 4. Start server from exception


```python
from webdebug import start_server

try:
    99/0
except Exception as ex:
    start_server(ex)

# or

try:
    99/0
except Exception as ex:
    start_server(ex,host='localhost',pin='12345',port='54321')

* Debugger is active!
```

## Callback/Notification
You can extend `webdebug.callback.BaseCallBack` and `webdebug.callback.Notifier` classes.

This package provides an out-of-the-box Gmail notifyer

To use the notifyer, you need a gmail account and an [app password](https://support.google.com/accounts/answer/185833):


```python
from webdebug import set_web_debug,GmailNotifier


set_web_debug(callbacks=[GmailNotifier(gmail_user='frompythonimportme@gmail.com'
                                       ,gmail_password='xxxxxxxx'
                                       ,to='frompythonimportme@gmail.com')])


99/0

```
![screen3](https://raw.githubusercontent.com/fpim/webdebug/master/screen3.png)

## Exceptions exclusion

`web_debug`,`set_web_debug` can be passed with `exclude` (`tuple` of `exception`)argument, 
so the `webdebug` will ignore the exception type.

```python
from webdebug import set_web_debug

set_web_debug(exclude=(ZeroDivisionError,))
0/0

#raise ZeroDivisionError as python normally world.
```