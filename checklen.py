adj = [word for word in open('adjectives.txt', 'r').read().split('\n') if word]
adv = [word for word in open('adverbs.txt', 'r').read().split('\n') if word]
verb = [word for word in open('verbs.txt', 'r').read().split('\n') if word]
noun = [word for word in open('nouns.txt', 'r').read().split('\n') if word]

print max([len(word) for word in adj]) + max([len(word) for word in adv]) + max([len(word) for word in verb]) + max([len(word) for word in noun])