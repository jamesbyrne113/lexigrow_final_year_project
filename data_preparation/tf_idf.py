import json
import math

import numpy as np
import pathlib


class TfIdfGenerator:
    def __init__(self, data_path, comments_key):
        self.data_path = data_path
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

        self.frequencies = {}
        for doc, data in self.docs.items():
            frequency = dict.fromkeys(self.all_words_set, 0)
            for comment in data[comments_key]:
                for word in comment.split():
                    if not word.startswith("__"):
                        frequency[word] = frequency[word] + 1
            self.frequencies[doc] = frequency
    
    def compute_tf(self):
        def compute_tf(word_freq, word_list):
            tf_dict = {}
            word_num = len(word_list)
            for word, count in word_freq.items():
                if count == 0:
                    tf_dict[word] = np.nan
                else:
                    tf_dict[word] = count/word_num
            return tf_dict
        
        self.tf = {}
        
        for doc in self.docs.keys():
            self.tf[doc] = compute_tf(self.frequencies[doc], self.doc_words[doc])
            
    def compute_idf(self):
        def compute_idf(docs):
            N = len(docs)

            idf_dict = dict.fromkeys(docs[0].keys(), 0)
            for doc in docs:
                for word, val in doc.items():
                    if val > 0:
                        idf_dict[word] += 1

            for word, val in idf_dict.items():
                idf_dict[word] = math.log(N/val)

            return idf_dict
        
        self.idf = compute_idf(list(self.frequencies.values()))
        
    def compute_tf_idf(self, compute_all=True):
        def compute_tf_idf(tf_freq, idfs):
            tf_idf = {}
            for word, val in tf_freq.items():
                if val is None:
                    tf_idf[word] = np.nan
                else:
                    tf_idf[word] = val * idfs[word]
            return tf_idf
        
        if compute_all or hasattr(self, "tf"):
            self.compute_tf()
        if compute_all or hasattr(self, "idf"):
            self.compute_idf()
            
        self.tf_idf = {}
        
        for doc in self.docs.keys():
            self.tf_idf[doc] = compute_tf_idf(self.tf[doc], self.idf)