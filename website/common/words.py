from nltk.corpus import words
from nltk.corpus import wordnet

all_words = {x.lower() for x in words.words()}.union(wordnet.words())