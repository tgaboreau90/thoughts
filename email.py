import random
ch = random.choice

recents = [word for word in open('recents.txt', 'r').read().split('\n') if word]

adj = [word for word in open('adjectives.txt', 'r').read().split('\n') if word and word not in recents]
adv = [word for word in open('adverbs.txt', 'r').read().split('\n') if word and word not in recents]
verb = [word for word in open('verbs.txt', 'r').read().split('\n') if word and word not in recents]
noun = [word for word in open('nouns.txt', 'r').read().split('\n') if word and word not in recents]

t_adverb = ch(adv)
t_verb = ch(verb)
t_adjective = ch(adj)
t_noun = ch(noun)

recents.append(t_adverb)
recents.append(t_verb)
recents.append(t_adjective)
recents.append(t_noun)

f = open('recents.txt', 'w')
for word in recents[-120:]:
	f.write(word + '\n')
f.close()

thought = "%s %s %s %s." % (t_adverb, t_verb, t_adjective, t_noun)
print thought


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

