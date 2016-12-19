'posts a tweet'

from twitter import *
from gen_thought import *
import json

'generates random thought'
thought = gen_thought(exclude = 'recents.txt')

'loads twitter credentials'
twitterCreds = json.loads(open('twitterCreds.json', 'r').read())

token = twitterCreds['token']
token_key = twitterCreds['token_key']
con_secret_key = twitterCreds['con_secret_key']
con_secret = twitterCreds['con_secret']

'authentication'
t = Twitter(auth = OAuth(token, token_key, con_secret, con_secret_key))

'posts tweet'
t.statuses.update(status = thought)

