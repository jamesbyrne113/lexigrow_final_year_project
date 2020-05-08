import json
import pickle
from joblib import load

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

num_to_cefr = {
	0: "A1",
	1: "A2",
	2: "B1",
	3: "B2",
	4: "C",
	5: "C2",
}

cefr_to_num = {
	"A1": 0,
	"A2": 1,
	"B1": 2,
	"B2": 3,
	"C": 4,
	"C1": 4,
	"C2": 5,
}

class WordDifficultyClassifierWrapper:
	wdc_model_path = "./resources/word_difficulty_classifier.joblib"
	cefr_path = "./resources/cefr.json"
	word_count_path = "./resources/word_count.pickle"

	wdc_model = load(wdc_model_path)
	with open(cefr_path, "r") as f:
		cefr = json.load(f)
	with open(word_count_path, "rb") as f:
		word_count = pickle.load(f)


	def get_cefr_level(self, word, pos=None):
		cefr_word = self.cefr[word]
		if pos is not None and pos in cefr_word:
			return cefr_word[pos]
		else:
			return cefr_word["min"]

	def is_in_cefr(self, word):
		return word in self.cefr.keys()

	def get_level_num(self, word, pos=None):
		if self.is_in_cefr(word):
			return self.get_cefr_level(word, pos)

		return self.wdc_model.get_numeric_cefr_level(word)

	def get_level(self, word, pos=None):
		cefr_int = self.get_level_num(word, pos)
		if cefr_int is None:
			return None

		return num_to_cefr[cefr_int]
