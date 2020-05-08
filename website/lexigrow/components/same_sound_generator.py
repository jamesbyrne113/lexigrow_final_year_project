import cmudict
import pathlib
import pickle
from common.words import all_words


class SameSoundGenerator:
	cmu = cmudict.dict()
	all_phonemes = cmudict.symbols()

	def __init__(self, reverse_cmu_path="./resources/cmu_reverse.pickle"):
		self.reverse_cmu = self._reverse_cmu(reverse_cmu_path)

	# phonemes collection, collection of collection (e.g. list of phoneme list)
	def phoneme_variances(self, phonemes_tuple):
		all_variances = set()

		phoneme_list = list(phonemes_tuple)
		for index, phonemes in enumerate(phoneme_list):
			for current_phoneme in self.all_phonemes:
				new_variant = phoneme_list[:index] + [current_phoneme] + phoneme_list[index + 1:]
				all_variances.add(tuple(new_variant))
		return all_variances

	def word_phoneme_variances(self, word, max_number=3, max_word_num=5):
		if word not in self.cmu:
			return []

		word_phonemes_tuples = set(
			[tuple(x) for x in self.cmu[word]])  # list of different phoneme representations of a word

		all_variances = set()

		current_variance_set = word_phonemes_tuples
		variance_count = 0
		while (variance_count < max_number):
			new_variance_set = set()
			for current_variance in current_variance_set:
				# only remove duplicates from current_variance set. First iteration prevents phoneme list for original word, Any other duplication removed with sets
				new_variance_set.update(self.phoneme_variances(current_variance))

			current_variance_set = new_variance_set
			all_variances.update(new_variance_set)
			if max_word_num > len(all_variances):
				return all_variances

			variance_count += 1

		for unwanted in word_phonemes_tuples:
			all_variances.discard(tuple(unwanted))

		return all_variances

	def same_sound_words(self, word):
		real_words = set()

		word_variances = self.word_phoneme_variances(word, 2)

		valid_phonemes_list = [var for var in word_variances if var in self.reverse_cmu]
		for phonemes in valid_phonemes_list:
			for word in self.reverse_cmu[phonemes]:
				if word in all_words:
					real_words.add(word)

		return list(real_words)

	def _reverse_cmu(self, reverse_cmu_path):
		if pathlib.Path(reverse_cmu_path).is_file():
			with open(reverse_cmu_path, "rb") as f:
				reverse_cmu = pickle.load(f)
		else:
			reverse_cmu = {}
			for word, phonemes_list in self.cmu.items():
				for phoneme in phonemes_list:
					phoneme_tuple = tuple(phoneme)

					if phoneme_tuple in reverse_cmu:
						if word not in reverse_cmu[phoneme_tuple]:
							reverse_cmu[phoneme_tuple].append(word)
					else:
						reverse_cmu[phoneme_tuple] = [word]

			with open(reverse_cmu_path, "wb") as f:
				pickle.dump(reverse_cmu, f)

		return reverse_cmu
