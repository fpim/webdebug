class BaseCallBack():
    def load_exception(self,ex,host, port,pin):
        self.ex, self.host, self.port, self.pin = ex,host, port,pin
    def run(self):
        print('Run method for ', self ,'not Implemented')

class Notifier(BaseCallBack):
    @property
    def simple_message(self):
        import traceback
        url = 'http://{0}:{1}'.format(str(self.host),str(self.port))
        tb = "".join(traceback.TracebackException.from_exception(self.ex).format()) + '\n'
        return 'Debuger is running at {0}, pin: {1} . To terminate debuger, go: {0}?shutdown=Y \n\n'.format(url,str(self.pin)) + tb

class GmailNotifier(Notifier):

    def __init__(self,gmail_user, gmail_password, to, subject='WebDebug'):

        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.to = to
        self.subject = subject

    
    def run(self):
        try:
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(self.simple_message)
            msg['Subject'] = self.subject
            msg['From'] = self.gmail_user
            msg['To'] = self.to
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg)
            server.quit()
        except Exception as ex:
            print('Notification error:',ex)
