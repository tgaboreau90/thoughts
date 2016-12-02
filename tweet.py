import random
from twitter import *
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

thought = ''
while len(thought) <= 140:
	thought = "%s %s %s %s." % (t_adverb, t_verb, t_adjective, t_noun)
	if len(thought) <= 140:
		break
print thought

token = '804637450677129216-1pSVXfgUCGz83CSzYOG1ugRRDMvrGsX'
token_key = 'aiYNuvyuclOg0a5mP1tNs1P7i0X5lgmQ7SurzhxbqXbxK'
con_secret_key = 'VmoD9e1szaQ1UTen1ukSpapr3VWEQ0wYVAVXfjavkOPxniwhTn'
con_secret = 'mMBAEbGhbyw60lsSYwuvqkB5L'

t = Twitter(auth = OAuth(token, token_key, con_secret, con_secret_key))

t.statuses.update(status = thought)

