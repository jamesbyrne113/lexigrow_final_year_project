# %%

import json
from datetime import datetime
import argparse

import pathlib
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from scipy.stats import zscore


class PrepareText:
    def __init__(self, data_path, max_words=20, z_score_filter=False, z_score_threshold=1.960):
        """

        Parameters
        ----------
        data_path
        max_words - (optional - int: default = 20) - maximum number of words in a sentence (ignore longer sentences)
        z_score_filter - (optional - boolean: default = False) - use z-score filter or max_words
        z_score_threshold - (optional - double: default 1.96) - used as z-score threshold
        """
        common_preprocessing = []
        for path in pathlib.Path(data_path).iterdir():
            if path.is_file() and not path.stem.startswith("."):
                with open(path, "r") as f:
                    file_data = json.load(f)


                word_tokenized = [word_tokenize(comment) for comment in file_data["comment_expandeds"]]
                comments = [" ".join(x) for x in word_tokenized]
                common_preprocessing.extend(comments)

        self.all_comments = self._process_comments(common_preprocessing, max_words, z_score_filter, z_score_threshold)


    def _z_score_filter(self, threshold, data):
        lengths = [len(x.split()) for x in data]
        zscores = zscore(lengths)
        filtered = [x for x, z in zip(data, zscores) if abs(z) < threshold]
        max_words = max([len(x.split()) for x in filtered])
        return filtered, max_words

    def _filter_data(self, max_words, comments):
        """
        Parameter
        ----------
        max_words - maximum number of words in a sentence (ignore all sentences with more words)
        comments - list of comments

        Returns
        -------
        sublist of comments where all comments have less words that the max_words param
        """
        filtered = []
        for comment in comments:
            if len(comment.split()) <= max_words:
                filtered.append(comment)
        return filtered

    def _tokenize_sentence(self, comments, max_words):
        tokenized_comments = []
        for tokenized_comment in [sent_tokenize(x) for x in comments]:
            tokenized_comments.extend(tokenized_comment)
        return tokenized_comments

    def _get_wordnet_phrases(self, data, max_words):
        word_set = set()
        for comment in data:
            word_set.update(comment.split())

        examples = set()
        definitions = set()
        for word in word_set:
            synsets = wn.synsets(word)
            for synset in synsets:
                examples.update(synset.examples())
                definitions.add(synset.definition())

        examples_tokenize = self._tokenize_sentence(examples, max_words)
        definitions_tokenize = self._tokenize_sentence(definitions, max_words)
        return examples_tokenize, definitions_tokenize

    def _process_comments(self, comments, max_words=20, z_score_filter=False, z_score_threshold=1.960):
        """
        Parameters
        ----------
        comments - list of comments
        max_words - (optional - int: default = 20) - maximum number of words in a sentence (ignore longer sentences)
        z_score_filter - (optional - boolean: default = False) - use z-score filter or max_words
        z_score_threshold - (optional - double: default 1.96) - used as z-score threshold

        Returns
        -------
        list of filtered comments and wornet example phrases and definitions for all words in the sentences
        """

        comments = [comment.lower() for comment in comments]
        examples, definitions = self._get_wordnet_phrases(comments, max_words)

        all_comments = comments + examples + definitions
        if z_score_filter:
            filtered_comments, max_words = self._z_score_filter(z_score_threshold, all_comments)
        else:
            filtered_comments = self._filter_data(max_words, all_comments)


        return filtered_comments

    def _spell_corrections(self, comments):
        comment_words = []
        for comment in comments:
            words = []
            for word in word_tokenize(comment):
                word = word.strip()
                if self.word_re.match(word):
                    words.append(self.spell_checker.correction(word))
                else:
                    words.append(word)
            comment_words.append(words)
        return " ".join(comment_words)

    def get_all(self):
        """
        Returns all processed comments
        -------

        """
        return self.all_comments

    def get_all_string(self, delimiter="\n"):
        return delimiter.join(self.all_comments)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--reddit_preprocessed_path", 
        type=str,
        default="data/reddit_data_processed/",
        help="Path to folder containing preprocessed files (the output from data_preparation/data_preprocessing.py)",
    )
    
    parser.add_argument(
        "--save_path",
        type=str,
        default="data/context2vec/texts/" + str(datetime.date(datetime.now())) + "/",
        help="Path to text file to output processed sentences"
    )
    
    args = parser.parse_args()

    prepare_text = PrepareText(args.reddit_preprocessed_path, max_words=20)
    processed_text = prepare_text.get_all_string()

    with open(save_path, "w") as f:
        f.write(processed_text)