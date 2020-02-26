class BaseCallBack():
    def __init__(self,ex,host, port,pin):
        self.ex, self.host, self.port, self.pin = ex,host, port,pin
    def run(self):
        raise NotImplementedError

class Notifier(BaseCallBack):
    @property
    def simple_message(self):
        import traceback
        url = 'http://{0}:{1}'.format(str(self.host),str(self.port))
        tb = "".join(traceback.TracebackException.from_exception(self.ex).format()) + '\n'
        return 'Debuger is running at {0}, pin: {1} . To terminate debuger, go: {0}?shutdown=Y \n\n'.format(url,str(self.pin)) + tb
