from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import nltk

from lexigrow.components.context2vec.context2vec import Context2Vec
from common.pos import nltk_to_wordnet_pos


class WordNet:
    context2vec = Context2Vec()

    lemmatizer = WordNetLemmatizer()

    def _get_pos(self, phrase, target_index):
        target_pos = nltk.pos_tag(phrase)[target_index][1]  # One to get POS value
        return nltk_to_wordnet_pos(target_pos)

    def _get_synsets(self, phrase, target_index, target_word, target_wordnet_pos):
        if target_wordnet_pos is None:
            target_wordnet_pos = self._get_pos(phrase, target_index)

        synsets = wn.synsets(target_word, pos=target_wordnet_pos)
        if synsets:
            return synsets

        synsets = wn.synsets(target_word)
        if not synsets:
            return synsets

        target_lemma = self.lemmatizer.lemmatize(target_word, pos=target_wordnet_pos)
        synsets = wn.synsets(target_lemma, pos=target_wordnet_pos)
        if synsets:
            return synsets

        synsets = wn.synsets(target_lemma)
        if synsets:
            return synsets

        return None


    def get_similar_words(self, phrase, target_index, target_wordnet_pos):
        target_word = phrase.split()[target_index]

        synsets = self._get_synsets(phrase, target_index, target_word, target_wordnet_pos)

        if not synsets:
            return []

        words_info = {
            "word": target_word,
            "details": [],
        }

        definiton_synsets = {}
        for synset in synsets:
            definition = synset.definition()
            words_info["details"].append({
                "definition": definition,
                "examples": synset.examples(),
            })
            definiton_synsets[definition] = synset
        sorted_details = self.context2vec.sorted_similar_contexts(target_index, phrase, words_info)

        selected_synset = definiton_synsets[sorted_details[0]["definition"]]

        return [word for word in selected_synset.lemma_names() if word != target_word]

if __name__ == "__main__":
    test = WordNet()
    print(test.get_similar_words("I am going to my house", 5))

