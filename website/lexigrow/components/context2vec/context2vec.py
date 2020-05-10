import sys
import re

import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

from common.pos import nltk_to_wordnet_pos
from common.words import all_words
from .common.model_reader import ModelReader


class Context2Vec:
    lemmatizer = WordNetLemmatizer()

    model_reader = ModelReader("./resources/context2vec_model_package/model.params")
    w = model_reader.w
    word2index = model_reader.word2index
    index2word = model_reader.index2word
    model = model_reader.model

    def similar_words(self, context, target_index, max_words=20, include_similarity=False):
        context_v = self.get_context_vector(context, target_index)

        similarity = (self.w.dot(context_v) + 1.0) / 2  # Cosine similarity can be negative, mapping similarity to [0,1]

        count = 0
        similar_words = []
        for i in (-similarity).argsort():
            word = self.index2word[i]
            if np.isnan(similarity[i]) or word not in all_words:
                continue
            similar_words.append((word, similarity[i]))
            count += 1
            if count == max_words:
                break

        if include_similarity:
            return similar_words
        return [x[0] for x in similar_words]

    # context_phrases is a list of dictionaries containing definitions and examples
    # OLD
    # def sorted_similar_contexts(self, target_index, target_context, words_info):
    #     context_lemmas = self.get_context_lemma(target_context)
    #     target_lemma = context_lemmas[target_index]
    #
    #     target_v = self.get_context_vector(target_context, target_word=target_lemma)
    #
    #     scores = {}
    #     for index, def_examples in enumerate(words_info["details"]):
    #         examples_sum = 0
    #         for example in def_examples["examples"]:
    #             example_v = self.get_context_vector(example, target_word=words_info["word"])
    #             examples_sum += self.mult_sim(target_v, example_v)
    #         if len(def_examples["examples"]) == 0:
    #             scores[index] = 0
    #         else:
    #             scores[index] = examples_sum / len(def_examples["examples"])
    #
    #     # sort array of context phrases (definition and example dicitonaries) and return them in a list
    #     return [words_info["details"][i] for i, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

    # context_phrases is a list of dictionaries containing definitions and examples
    # gets average vector for example phrases and determines the similarity with the target phrases
    def sorted_similar_contexts(self, target_index, target_context, words_info):
        context_lemmas = self.get_context_lemma(target_context)
        target_lemma = context_lemmas[target_index]
        target_word = target_context.split()[target_index]

        target_v = self.get_context_vector(target_context, target_words=[target_lemma, target_word])

        scores = {}
        for index, def_examples in enumerate(words_info["details"]):
            example_vectors = []

            if "lemmas" in def_examples:
                words = def_examples["lemmas"]
            else:
                words = [words_info["word"]]

            for example in def_examples["examples"]:
                example_vectors.append(self.get_context_vector(example, target_words=words))
            if len(example_vectors) == 0:
                scores[index] = -sys.maxsize -1
            else:
                average_vector = np.mean(example_vectors, axis=0)
                scores[index] = self.mult_sim(target_v, average_vector)

        # sort array of context phrases (definition and example dicitonaries) and return them in a list
        return [words_info["details"][i] for i, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

    def mult_sim(self, vector1, vector2):
        vector1_similarity = self.w.dot(vector1)
        vector1_similarity[vector1_similarity < 0] = 0.0

        vector2_similarity = self.w.dot(vector2)
        vector2_similarity[vector2_similarity < 0] = 0.0
        return vector1_similarity @ vector2_similarity

    def get_context_lemma(self, context):
        context_list = context.split()
        lemmas = []
        for (word, pos) in nltk.pos_tag(context_list):
            lemmas.append(self.lemmatizer.lemmatize(word, pos=nltk_to_wordnet_pos(pos)))
        return lemmas

    def get_context_vector(self, context, target_index=-1, target_words=None):
        context = re.sub("[^a-z ]", "", context.lower())
        context_list = context.lower().split()

        if target_words is not None:
            context_lemmas = self.get_context_lemma(context)

            if type(target_words) is not list:
                target_words = [target_words]
            for word in target_words:
                try:
                    target_index = context_lemmas.index(word)
                    if target_index != -1:
                        context_list[target_index] = None
                        break
                except:
                    pass
            if target_index == -1:
                print("Error generating context vector with a target_index={}, words={}, for: {}".format(target_index, target_words, context))

        context_v = self.model.context2vec(context_list, target_index)
        return context_v / np.sqrt((context_v * context_v).sum())
