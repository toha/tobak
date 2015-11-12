import sys, traceback
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def handleError(msg, e=None, exit=True):
	mailtxt = u"The following error occured during the backup:\n\n"
	mailtxt += msg
	if e != None:
		mailtxt += "\n\n%s\n%s"%(str(e), traceback.format_exc())

	msg = MIMEText(mailtxt.encode('utf-8'), 'plain', 'utf-8')
	msg["From"] = "mail@example.com"
	msg["To"] = "mail@example.com"
	msg["Subject"] = "error on backup"
	p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
	p.communicate(msg.as_string())

	if exit:
		sys.exit(1)
