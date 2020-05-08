from nltk.corpus import wordnet


def nltk_to_oxford_pos(tag):
    if tag.startswith('J'):
        return "adjective"
    elif tag.startswith('V'):
        return "verb"
    elif tag.startswith('N'):
        return "noun"
    elif tag.startswith('R'):
        return "adverb"
    elif tag.startswith('PRP'):
        return "pronoun"
    elif tag.startswith('DT'):
        return "determiner"
    elif tag.startswith('TO'):
        return "infinitive marker"
    elif tag.startswith('CD'):
        return "number"
    else:
        return ''


def nltk_to_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def oxford_to_wordnet_pos(tag):
    if tag.startswith('adjective'):
        return wordnet.ADV
    elif tag.startswith('verb'):
        return wordnet.VERB
    elif tag.startswith('noun'):
        return wordnet.NOUN
    elif tag.startswith('adverb'):
        return wordnet.ADJ
    else:
        return ''
