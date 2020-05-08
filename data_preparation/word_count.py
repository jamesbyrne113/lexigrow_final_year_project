import json

import pathlib


class WordCounter:
    def __init__(self, data_path, comments_key):
        self.data_path = data_path
        self.comments_key = comments_key
        files = [x for x in pathlib.Path(data_path).iterdir() if x.is_file() and x.suffix == ".json" and not x.name == "tf-idf.json"]
        
        self.docs = {}
        for file in files:
            with file.open() as f:
                self.docs[file.stem] = json.load(f)
        self.count = 0
        
        self.doc_words = {}
        self.all_words_set = set()
        for doc, data in self.docs.items():
            words = []
            for comment in data[comments_key]:
                for word in comment.split():
                    if not word.startswith("__"):
                        self.count += 1
                        words.append(word)
            self.doc_words[doc] = words
            self.all_words_set = self.all_words_set.union(set(words))
        
        self.compute_word_count()
            
    def compute_word_count(self):
        self.word_count = {}
        for doc, data in self.docs.items():
            word_count = dict.fromkeys(self.all_words_set, 0)
            for comment in data[self.comments_key]:
                for word in comment.split():
                    if not word.startswith("__"):
                        word_count[word] = word_count[word] + 1
            self.word_count[doc] = word_count
        