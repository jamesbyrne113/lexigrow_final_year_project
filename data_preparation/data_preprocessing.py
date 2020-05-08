# %%

import json
import re
import argparse

import nltk
import pathlib
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from pycontractions import Contractions
from spellchecker import SpellChecker


class TextCleaner:
    word_re = re.compile('[a-zA-Z]+')
    number_re = re.compile('[0-9]+$')
    spell_checker = SpellChecker()
    lemmatizer = WordNetLemmatizer()
    all_words = set(words.words())

    def __init__(self, save_path, word2vec_model_path, previously_processed=[]):
        self.contractions = Contractions(word2vec_model_path)
        self.previously_processed = previously_processed
        self.save_path = save_path

    def _get_all_comments(self, subreddit):
        comments = []
        for submission in subreddit["submissions"]:
            for comment in submission["comments"]:
                comments.extend(sent_tokenize(comment["body"]))
        return comments

    def _remove_urls(self, text):
        url_pattern = r'(((https?|ftp)://)?(([a-zA-Z])+\.)?([a-zA-Z])+\.([a-zA-Z])+/?.*)|http'

        new_sentences = []
        for word in text.split():
            if re.compile(url_pattern).search(word):
                new_sentences.append(re.sub(url_pattern, "__isurl__", word))
            else:
                new_sentences.append(word)
        return " ".join(new_sentences)

    def _invalid_characters(self, string):
        string = re.sub("(\s|-|_|\.\.\.)+", " ", string)
        return re.sub("!|#|&|\(|\)|–|\[|{|}|\]|:|;|\?|\*", "", string)

    def _expand_sentences(self, texts):
        return list(self.contractions.expand_texts([x.replace("’", "'") for x in texts], precise=True))

    def _replace(self, sentence, is_spell_check=True):
        words = []
        for word in word_tokenize(sentence):
            word = word.strip()
            if "/" in word or "\\" in word:
                words.append("__isslashinword__")
            elif self.word_re.match(word):
                if is_spell_check and word not in self.all_words:
                    words.append(self.spell_checker.correction(word))
                else:
                    words.append(word)
            elif self.number_re.match(word):
                words.append("__isnumber__")
            elif "__isurl__" in word:
                words.append("__isurl__")
            else:
                words.append("__isinvalidword__")
        return words

    def _words_and_tags(self, words):
        lemmas = []
        pos_tags = []
        for word, pos_tag in nltk.pos_tag(words):
            pos_tags.append(pos_tag)
            if self._get_wordnet_pos(pos_tag):
                lemmas.append(self.lemmatizer.lemmatize(word, pos=self._get_wordnet_pos(pos_tag)))
            else:
                lemmas.append(self.lemmatizer.lemmatize(word))
        return (" ".join(lemmas), pos_tags)

    ## there are others but this is sufficient, e.g. one more wordnet pos tag (adjective satellite) and many more nltk pos tags
    def _get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''

    def process_subreddits(self, subreddits, save=True, check_previous=True):
        for subreddit in subreddits:
            print(subreddit["display_name"])
            pathlib.Path(self.save_path).mkdir(exist_ok=True)

            all_raw_comments = self._get_all_comments(subreddit)
            raw_comments = all_raw_comments

            comment_no_urls = []
            comment_removed_chars = []
            comment_expandeds = []

            comment_replaced_spell_corrections = []
            comment_processed_spell_corrections = []
            pos_tag_sent_spell_corrections = []

            comment_replaced_no_spell_corrections = []
            comment_processed_no_spell_corrections = []
            pos_tag_no_sent_spell_corrections = []

            count = 0;
            total = len(raw_comments)
            for comment in raw_comments:
                print(comment)
                comment_no_url = self._remove_urls(comment)
                comment_removed_char = self._invalid_characters(comment_no_url)
                comment_expanded = self._expand_sentences([comment_removed_char])[0]

                comment_replaced_spell_correction = self._replace(comment_expanded.lower(), is_spell_check=True)
                comment_processed_spell_correction, pos_tag_sent_spell_correction = self._words_and_tags(
                    comment_replaced_spell_correction)

                comment_replaced_no_spell_correction = self._replace(comment_expanded.lower(), is_spell_check=False)
                comment_processed_no_spell_correction, pos_tag_no_sent_spell_correction = self._words_and_tags(
                    comment_replaced_no_spell_correction)

                count += 1
                print("count:", count, "total:", total, subreddit["display_name"])

                # Appending
                comment_no_urls.append(comment_no_url)
                comment_removed_chars.append(comment_removed_char)
                comment_expandeds.append(comment_expanded)

                comment_replaced_spell_corrections.append(comment_replaced_spell_correction)
                comment_processed_spell_corrections.append(comment_processed_spell_correction)
                pos_tag_sent_spell_corrections.append(pos_tag_sent_spell_correction)

                comment_replaced_no_spell_corrections.append(comment_replaced_no_spell_correction)
                comment_processed_no_spell_corrections.append(comment_processed_no_spell_correction)
                pos_tag_no_sent_spell_corrections.append(pos_tag_no_sent_spell_correction)

            data = {
                "raw": raw_comments,
                "comment_no_urls": comment_no_urls,
                "comment_removed_chars": comment_removed_chars,
                "comment_expandeds": comment_expandeds,
                "comment_replaced_spell_corrections": comment_replaced_spell_corrections,
                "comment_processed_spell_corrections": comment_processed_spell_corrections,
                "pos_tag_sent_spell_corrections": pos_tag_sent_spell_corrections,
                "comment_replaced_no_spell_corrections": comment_replaced_no_spell_corrections,
                "comment_processed_no_spell_corrections": comment_processed_no_spell_corrections,
                "pos_tag_no_sent_spell_corrections": pos_tag_no_sent_spell_corrections,
            }

            if save:
                subreddit_path = self.save_path + "TEST" + subreddit["display_name"] + ".json"
                with open(subreddit_path, 'w') as fp:
                    json.dump(data, fp)
            else:
                return data


# %%

def get_subreddits(subreddit_dir):
    subreddit_paths = [x for x in pathlib.Path(subreddit_dir).iterdir() if x.is_file() and x.suffix == ".json"]

    subreddits = []
    for subreddit_path in subreddit_paths:
        with subreddit_path.open() as file:
            subreddits.append(json.load(file))
    return subreddits

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
   
    parser.add_argument(
        "--reddit_collected_path", 
        type=str,
        default="data/reddit_data",
        help="path to folder with originally collected reddit data",
    )
    parser.add_argument(
        "--processed_reddit_path", 
        type=str,
        default="data/reddit_data",
        help="output path for processed reddit files",
    )
    parser.add_argument(
        "--word2vec_model_path",
        type=str,
        default="models/GoogleNews-vectors-negative300.bin",
        help="Path to Word2Vec model used for",
    )
    
    args = parser.parse_args()

    subreddits = get_subreddits(args.reddit_collected_path)

    text_cleaner = TextCleaner(args.processed_reddit_path, args.word2vec_model_path)
    text_cleaner.process_subreddits(subreddits, check_previous=False)


