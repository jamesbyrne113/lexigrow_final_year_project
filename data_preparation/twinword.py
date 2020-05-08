import os
import sys
ROOT_PATH = os.getcwd()
sys.path.append(ROOT_PATH)

import json
import urllib3
import random
import argparse

from nltk.corpus import words as nltk_words
from nltk.corpus import wordnet as wn

TWINWORD_PATH = "data/word_difficulty_classifier/twinword.json"

class TwinwordScores():

    http = urllib3.PoolManager()
    
    def __init__(self, twinword_api_key):
        self.twinword_api_key = twinword_api_key

    def _get_word_score(self, word):
        url = "https://api.twinword.com/api/v5/score/word/"
        params = {"entry": word}
        headers = {
            "XHost": "api.twinword.com",
            "Content-Type": "application/json",
            "X-Twaip-Key": self.twinword_api_key,
            }

        response =  self.http.request('GET', url, fields=params, headers=headers)
        data = json.loads(response.data.decode('utf-8'))
        return response, data

    def twinword_scores(self, words, save_path, no_score_path=None):
        """ words: list of words, save_path: path to save valid words, no_score_path(Optional): path to save words with no score"""
        
        twinword_scores_raw = {}
        for i, word in enumerate(words):
            response, data = self._get_word_score(word)
            print("collected {}: {}".format(i, str(data)))
            twinword_scores_raw[word] = data
            
        twinword_scores = {}
        twinword_no_words = {}
        for k, v in twinword_scores_raw.items():
            if "ten_degree" in v:
                twinword_scores[k] = v["ten_degree"]
            else:
                twinword_no_words[k] = v
                
        with open(save_path, "w") as fp:
            print("saving scores to:", save_path)
            json.dump(twinword_scores, fp)
        
        if no_score_path:
            with open(no_score_path, "w") as fp:
                print("saving invalid words to:", no_score_path)
                json.dump(twinword_no_words, fp)

def twinword_scores_oxford5000_words(twinword_api_key, words, save_path, no_score_path=None):
    """save_path: path to save valid words, level_type: min or avg for mutliple levels of a word for different pos, no_score_path(Optional): path to save words with no score"""
    
    
    twinword_scores = TwinwordScores(twinword_api_key)

    twinword_scores.twinword_scores(words, save_path, no_score_path)
    
if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--non_cefr_save_path", 
        type=str,
        default="data/word_difficulty_classifier/non_cefr_words_twinword.json",
        help="Save path for json file consisting of twinword words not in the Oxford 5000 data set",
    )
    parser.add_argument(
        "--cefr_save_path", 
        type=str,
        default="data/word_difficulty_classifier/cefr_words_twinword.json",
        help="Save path for json file consisting of twinword words that are in the Oxford 5000 data set",
    )
    parser.add_argument(
        "twinword_api_key",
        type=str,
        help="API key from twinword must be provided, visit https://www.twinword.com/api/language-scoring.php for further details",
    )
    parser.add_argument(
        "--cefr_path",
        type=str,
        default="data/word_difficulty_classifier/cefr_min.json",
        help="path to cefr min file",
    )
    
    args = parser.parse_args()

    with open(args.cefr_path, "r") as f:
        cefr = json.load(f)
        
    cefr_words = set(cefr.keys())
    
    # All words in both NLTK and WordNet word lists that are not in the CEFR data set
    valid_words = list(set(nltk_words.words()).intersection(wn.words()).difference(cefr_words))
    
    words = set()
    for word in random.sample(valid_words, 1000):
        words.add(word.lower())
        
    print("non_cefr_save_path: " + non_cefr_save_path)
    twinword_scores_oxford5000_words(args.twinword_api_key, words=words, save_path=args.non_cefr_save_path, no_score_path=None)
    
    print("cefr_save_path: " + cefr_save_path)
    twinword_scores_oxford5000_words(args.twinword_api_key, words=cefr_words, save_path=args.cefr_save_path, no_score_path=None)


