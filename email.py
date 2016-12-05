import random
from gen_thought import *

thought = gen_thought(exclude = 'recents.txt')


import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

username = "tommy@yum.co.uk"
password = "d1lb3rt"
emailfrom = "tommy@yum.co.uk"
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
     
 
server = smtplib.SMTP("10.48.0.2")
server.login(username,password)
for address in recipients:
    server.sendmail(emailfrom, address, msg.as_string())
server.quit()

