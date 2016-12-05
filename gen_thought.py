import random
from IOPlus import *


def gen_thought(exclude = None):
	ch = random.choice

	if not exclude:
		recents = []
	else:
		recents = [word for word in open(exclude, 'r').read().split('\n') if word]

	adv = [word for word in open('adverbs.txt', 'r').read().split('\n') if word and word not in recents]
	verb = [word for word in open('verbs.txt', 'r').read().split('\n') if word and word not in recents]
	adj = [word for word in LocalCsv('adjectives.csv').OpenToDictList() if word['singular'] not in recents and word['plural'] not in recents]
	noun = [word for word in LocalCsv('nouns.csv').OpenToDictList() if word['singular'] not in recents and word['plural'] not in recents]

	form = ch(['singular', 'plural'])

	t_adverb = ch(adv)
	t_verb = ch(verb)
	t_adjective = ch(adj)[form]
	t_noun = ch(noun)[form]

	recents.append(t_adverb)
	recents.append(t_verb)
	recents.append(t_adjective)
	recents.append(t_noun)

	if not exclude:
		pass
	else:
		f = open(exclude, 'w')
		for word in recents[-80:]:
			f.write(word + '\n')
		f.close()

	thought = "%s %s %s %s." % (t_adverb, t_verb, t_adjective, t_noun)
	return thought
