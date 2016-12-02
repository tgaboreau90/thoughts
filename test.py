import random
ch = random.choice

recents = [word for word in open('recents_test.txt', 'r').read().split('\n') if word]

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

f = open('recents_test.txt', 'w')
for word in recents[-40:]:
	f.write(word + '\n')
f.close()

thought = "%s %s %s %s." % (t_adverb, t_verb, t_adjective, t_noun)
print thought