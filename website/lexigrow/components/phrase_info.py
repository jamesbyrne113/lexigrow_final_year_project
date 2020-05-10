import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from lexigrow.components.dictionary_words import similar_dictionary_word, get_word_info
from lexigrow.components.oxford_learners_dict_wrapper import OxfordLearnersDictWrapper
from lexigrow.components.same_sound_generator import SameSoundGenerator
from lexigrow.components.context2vec.context2vec import Context2Vec
from lexigrow.components.word2vec import Word2Vec
from lexigrow.components.word_dfficulty_classifier_wrapper import cefr_to_num
from lexigrow.components.wordnet import WordNet

from common.pos import oxford_to_wordnet_pos

nltk.data.path.append("/home/student/nltk_data")

lemmatizer = WordNetLemmatizer()
stopword_set = set(stopwords.words('english'))

same_sound_generator = SameSoundGenerator()
dictionary = OxfordLearnersDictWrapper()
context2vec = Context2Vec()
word2vec = Word2Vec()
wordnet = WordNet()

def are_clickable_words(phrase):
	has_target_links = []
	for word in phrase.split():
		if word in stopword_set:
			has_target_links.append(False)
		else:
			has_target_links.append(True)
	return has_target_links


def get_target_word_infos(target_index, phrase):
	words_info = get_word_info(target_index=target_index, phrase=phrase)

	for word_info in words_info:
		if len(word_info["details"]) > 1:
			sorted_details = context2vec.sorted_similar_contexts(target_index, phrase, word_info)
			word_info["details"] = [sorted_details[0]]

	return words_info


def get_similar_context(phrase, target_index, target_word_infos, max_level=6):
	similar_words = context2vec.similar_words(phrase, target_index, max_words=50)

	return similar_dictionary_word(similar_words, phrase, target_index, target_word_infos, max_level=max_level)


def get_similar_meaning(phrase, target_index, target_word_infos, max_level=6):
	target_word = phrase.split()[target_index]
	similar_words = word2vec.get_n_similar_words(target_word)

	for target_word_info in target_word_infos:
		if target_word_info["word"] in similar_words:
			similar_words.remove(target_word_info["word"])

	return similar_dictionary_word(similar_words, phrase, target_index, target_word_infos, max_level=max_level)


def get_similar_meaning_wordnet(phrase, target_index, target_word_infos, max_level=6):
	target_wordnet_pos = None
	if len({x["pos"] for x in target_word_infos}) == 1:
		target_wordnet_pos = oxford_to_wordnet_pos(target_word_infos[0]["pos"])
	similar_words = wordnet.get_similar_words(phrase, target_index, target_wordnet_pos)

	return similar_dictionary_word(similar_words, phrase, target_index, target_word_infos, max_word_num=len(similar_words), max_level=max_level)

def get_same_sound(word, max_level=6):
	same_sound_words = same_sound_generator.same_sound_words(word)

	unique_words = set()
	words_info = []
	for word_info in dictionary.get_words_info_gen(same_sound_words):
		if word_info["word"] != word and word_info["word"] not in unique_words and cefr_to_num.get(word_info["level"], 0) <= max_level:
			words_info.append(word_info)
			unique_words.add(word_info["word"])
		if len(words_info) >= 10:
			break
	return list(words_info)
