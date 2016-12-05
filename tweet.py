import random
from twitter import *
from gen_thought import *

thought = gen_thought(exclude = 'recents.txt')

token = '804637450677129216-1pSVXfgUCGz83CSzYOG1ugRRDMvrGsX'
token_key = 'aiYNuvyuclOg0a5mP1tNs1P7i0X5lgmQ7SurzhxbqXbxK'
con_secret_key = 'VmoD9e1szaQ1UTen1ukSpapr3VWEQ0wYVAVXfjavkOPxniwhTn'
con_secret = 'mMBAEbGhbyw60lsSYwuvqkB5L'

t = Twitter(auth = OAuth(token, token_key, con_secret, con_secret_key))

t.statuses.update(status = thought)

