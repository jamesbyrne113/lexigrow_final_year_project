import gensim

class Word2Vec():

    # w2v = gensim.models.KeyedVectors.load_word2vec_format('./resources/word2vec/GoogleNews-vectors-negative300.bin', binary=True)

    def get_n_similar_words(self, word, num_words=10):
        similar_words = [x[0] for x in self.w2v.similar_by_word(word, topn=num_words)]
        return similar_words