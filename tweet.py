from twitter import *
from gen_thought import *
import json

thought = gen_thought(exclude = 'recents.txt')

twitterCreds = json.loads(open(twitterCreds.json, 'r').read())

token = twitterCreds['token']
token_key = twitterCreds['token']
con_secret_key = twitterCreds['con_secret_key']
con_secret = twitterCreds['con_secret']

t = Twitter(auth = OAuth(token, token_key, con_secret, con_secret_key))

t.statuses.update(status = thought)

