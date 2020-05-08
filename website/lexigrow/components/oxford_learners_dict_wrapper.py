import requests
from bs4 import BeautifulSoup

from frontend.models import WordInfo, Details, Example
from lexigrow.components.word_dfficulty_classifier_wrapper import WordDifficultyClassifierWrapper

class OxfordLearnersDictWrapper:
	cache_path = "./resources/oxford_dictionary_words/"
	oxford_url = "https://www.oxfordlearnersdictionaries.com/definition/english/"
	cache_word_list = "./resources/cache_word_list.txt"
	word_difficulty_classifier = WordDifficultyClassifierWrapper()

	def _get_soup(self, word=None, url=None):
		if word is None and url is None:
			raise Exception("Need either URL or Word")

		if url is None:
			url = self.oxford_url + word

		response = requests.get(url)

		soup = BeautifulSoup(response.text, features="html.parser")

		for div in soup.find_all('div', {'class': 'idioms'}):
			div.decompose()

		return soup

	def get_words_info_gen(self, words):
		words_info = []

		for word in words:
			if len(words_info) > 0:
				yield words_info.pop(0)
			else:
				word_info = self.get_word_info(word)
				if word_info is not None:
					words_info.extend(word_info)


	def get_words_info_model(self, word):
		words_info_query = WordInfo.objects.filter(word=word)
		if not words_info_query.exists():
			return None

		words_info = []
		for word_info in words_info_query:
			all_details = []
			details_query = word_info.details_set.all()
			if details_query.exists():
				for details in details_query:
					examples = []
					examples_query = details.example_set.all()
					if examples_query.exists():
						for example in details.example_set.all():
							examples.append(example.example)

				all_details.append({
					"definition": details.definition,
					"examples": examples
				})

			words_info.append({
				"word": word_info.word,
			   	"pos": word_info.pos,
				"level": word_info.level,
				"details": all_details,
			})

		return list(words_info)

	def save_words_info_model(self, words_info):
		for word_info in words_info:
			word_info_entry, _ = WordInfo.objects.get_or_create(
				word=word_info["word"],
				pos=word_info["pos"],
				level=word_info["level"],
			)
			word_info_entry.save()

			for details in word_info["details"]:
				details_entry = Details(definition=details["definition"])
				details_entry.word_info = word_info_entry
				details_entry.save()

				for example in details["examples"]:
					example_entry = Example(example=example)
					example_entry.details = details_entry
					example_entry.save()


	def get_word_info(self, word=None, url=None, is_nearby_words=True, soup=None):
		if word is None and url is None and soup is None:
			raise Exception("Need either URL or Word")
		elif word is not None:
			try:
				words_info = self.get_words_info_model(word)
				if words_info:
					return words_info
			except:
				pass

		if soup is None:
			soup = self._get_soup(word, url)

		word = self.get_word(soup)
		pos = self.get_pos(soup)

		words_info = [{
			"word": word,
			"pos": pos,
			"details": self.get_word_details(soup),
			"level": self.word_difficulty_classifier.get_level(word, pos),
		}]

		if words_info[0]["word"] == '':
			return None

		if is_nearby_words:
			nearby_words = self.get_nearby_words(soup, words_info[0])
			if len(nearby_words) > 0:
				words_info.extend(nearby_words)
			try:
				self.save_words_info_model(words_info)
			except Exception as ex:
				print(ex)

		return words_info

	def get_nearby_words(self, soup, word_info):
		urls = self.get_other_urls(soup, word_info)

		nearby_words = []
		for url in urls:
			nearby_word = self.get_word_info(url=url, is_nearby_words=False)
			if len(nearby_word) > 0:
				nearby_words.append(nearby_word[0])

		return nearby_words

	def get_other_urls(self, soup, word_info):
		urls = []

		try:
			for li in soup.find('h4', string="Nearby words").parent.find('ul').findAll('li'):
				a_ele = li.find('a')
				if a_ele.get("class") != "selected":
					text_list = a_ele.get_text(' ', strip=True).split()

					if text_list[0] == word_info["word"] and (not len(text_list) > 1 or text_list[1] != word_info["pos"]):
						urls.append(a_ele.get("href"))
			return urls
		except:
			return []

	def get_word(self, soup):
		try:
			return soup.find(id="main_column").find('h1', {'class': 'headword'}).get_text(' ', strip=True)
		except:
			return ""

	def get_pos(self, soup):
		try:
			return soup.find(id="main_column").find('span', {'class': 'pos'}).get_text(' ', strip=True)
		except:
			return ""

	def get_word_details(self, soup):
		details = []
		try:
			for li_soup in soup.find(id="main_column").findAll('li', {'class': 'sense'}):
				word_def = self.get_word_definition(li_soup)
				if word_def:
					details.append({
						"definition": word_def,
						"examples": self.get_word_examples(li_soup),
					})
			return details
		except:
			return []

	def get_word_definition(self, li_soup):
		try:
			grammar = li_soup.find('span', {'class': 'grammar'})
			definition = li_soup.find('span', {'class': 'def'})
			# labels = li_soup.find('span', {'class': 'labels'})

			definition_text = ""
			if definition is None:
				return None
			else:
				definition_text += definition.get_text(' ', strip=True)

			if grammar:
				definition_text = grammar.get_text(' ', strip=True) + definition_text

			# if labels:
			# 	definition_text = labels.get_text(' ', strip=True)

			return definition_text
		except:
			return ""

	def get_word_examples(self, li_soup):
		try:
			uls = li_soup.findAll('ul', {'class': 'examples'})

			if len(uls) == 0:
				return []

			examples = []
			for element in uls[0].findAll('li'):
				examples.append(element.get_text(' ', strip=True))

			example_number = min(3, len(examples))
			return examples[:example_number]
		except:
			return []

if __name__ == "__main__":
	words = ['going', 'off', 'addicted', 'getting', 'coming', 'close', 'rushing', 'walking', 'closer', 'transported', 'hurrying', 'heading', 'returning', 'moving', 'flown', 'taken', 'talking', 'hooked', 'back', 'sent', 'drifting', 'listening', 'flying', 'halfway', 'drawn', 'near', 'closest', 'rushed', 'journeying', 'glued', 'allergic', 'brought', 'sailing', 'tied', 'driven', 'hobbling', 'dashing', 'connected', 'sticking', 'leaning', 'stuck', 'travelling', 'thankful', 'chained', 'unsuited', 'traveling', 'wedded', 'clinging', 'thirsty', 'straight', 'gone', 'waddling', 'pointing', 'driving', 'returned', 'vacationing', 'newish', 'nearer', 'sleepwalking', 'away', 'cycling', 'barefoot', 'popping', 'headed', 'awakened', 'swimming', 'new', 'diving', 'jumping', 'leaping', 'looking', 'pooped', 'steaming', 'confined', 'descending', 'bound', 'blind', 'commuting', 'paddling', 'heir', 'chatting', 'betrothed', 'led', 'up', 'directed', 'tottering', 'got', 'ascending', 'rooted', 'loyal', 'down', 'barred', 'doomed', 'come', 'beastly', 'whispering', 'transferring', 'humming', 'curious', 'naked']
	dictionary = OxfordLearnersDictWrapper()

	from datetime import datetime

	print(datetime.now())
	# print(dictionary.get_words_info_list(words))
	for index, test in enumerate(dictionary.get_words_info_gen(words)):
		print(test)
		if index > 1:
			break;

	# for word in words[:10]:
	# 	dictionary.get_word_info(word=word)

	# print(list(dictionary.get_words_info_gen(words)))
	print(datetime.now())
