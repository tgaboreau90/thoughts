'emails each address in mailing.txt'

from gen_thought import *
import time

'generates random thought'
thought = gen_thought(exclude = 'recents.txt')


import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

'builds email object'
emailfrom = "nonsense@tommy.com"
msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = ""

recipients = [recipient for recipient in open('mailing.txt', 'r').read().split('\n') if recipient]

msg["Subject"] = "Inspiration for the day - DO NOT REPLY"
text = """Perhaps you should:

%s


Follow https://twitter.com/GreatIdeasDaily for more! :)
""" % thought


msg.attach (MIMEText(text))
     
 
server = smtplib.SMTP("localhost")
for address in recipients:
	'sends email to each recipient'
        server.sendmail(emailfrom, address, msg.as_string())
	'waits 10 seconds between each to avoid clogging up mail queue'
        time.sleep(10)
server.quit()

