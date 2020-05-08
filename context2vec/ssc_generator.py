import re
import nltk
import random
from nltk.corpus import stopwords

class SentenceCompletionChallenge:
    word_re = re.compile('[a-zA-Z]+$')
    MIN_SENT_LENGTH = 5
    A_TO_E = ['a', 'b', 'c', 'd', 'e']
    self.stopwords = set(stopwords.words('english'))
    
    def __init__(self, path, is_testset=True):
        # self.save_path = texts_path
        # self.is_testset = is_testset
        
        # if is_testset:
        #     path = texts_path + "test.txt"
        # else:
        #     path = texts_path + "train.txt"
            
        with open(path, "r") as f:
            phrases = f.read().split('\n')
        self._setup(phrases)
    
    def _setup(self, phrases):
        """make dicitonary key:POS,  value:list of unique words
        list of phrases where each word is a tuple of (word, POS)"""
        
        self.phrases_pos = []
        self.pos_dict = {}
        for phrase in phrases:
            phrase_list = phrase.split()
            if len(phrase_list) < self.MIN_SENT_LENGTH:
                continue
            phrase_pos = nltk.pos_tag(phrase_list)
            for word, pos in phrase_pos:
                if self.word_re.match(word):
                    if pos in self.pos_dict:
                        self.pos_dict[pos].add(word)
                    else:
                        self.pos_dict[pos] = {word}
            self.phrases_pos.append(phrase_pos)

        self.invalid_poses = set()
        for pos, words in self.pos_dict.items():
            if len(words) < 5:
                self.invalid_poses.add(pos)
            self.pos_dict[pos] = list(words)
            
    def generate_question_and_answers(self, path):
        question_phrases = []
        answer_phrases = []

        for index, phrase_pos in enumerate(self.phrases_pos, 1):
            if len(phrase_pos) < self.MIN_SENT_LENGTH:
                continue
            target_index = self._select_target_index(phrase_pos)
            if target_index is None:
                continue
            target_word, target_pos = phrase_pos[target_index]

            wrong_options = self._get_random_words(target_word, target_pos, 4)
            if wrong_options is None:
                continue
            all_options = wrong_options + [target_word]
            random.shuffle(all_options)

            for letter, word in zip(self.A_TO_E, all_options):
                phrase_list = [x[0] for x in phrase_pos] # get words (i.e. exclude pos)
                phrase_list[target_index] = "[" + word + "]"
                new_phrase = "{}{}) {}".format(str(index), letter, " ".join(phrase_list))
                if word == target_word:
                    answer_phrases.append(new_phrase)
                question_phrases.append(new_phrase)
        
        # if self.is_testset:
        #     path = self.save_path + "test_"
        # else:
        #     path = self.save_path + "train_"
              
        print("Save path:", path)
        with open(path + "/questions.txt", "w") as f:
            f.write("\n".join(question_phrases))

        with open(path + "/answers.txt", "w") as f:
            f.write("\n".join(answer_phrases))
            
    def _select_target_index(self, phrase_pos):
        valid_indexes = []
        for index, (word, pos) in enumerate(phrase_pos):
            if self.word_re.match(word) and pos not in self.invalid_poses and word not in self.stopwords:
                valid_indexes.append(index)
        if not valid_indexes:
            print("ERROR: _select_target_index:", phrase_pos)
            return None
        return random.choice(valid_indexes)
    
    def _get_random_words(self, word, pos, num=4):
        try:
            random_indexes = random.sample(range(1, len(self.pos_dict[pos])), num)
        except Exception as ex:
            print("ERROR: _get_random_words:", word, pos, num)
            return None
        
        return [self.pos_dict[pos][i] for i in random_indexes]
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file_path", 
        type=str,
        help="path to file containing sentences"
    )
    parser.add_argument(
        "--output_folder_path", 
        type=str,
        help="path to output folder"
    )
     
    args = parser.parse_args()

    scc = SentenceCompletionChallenge(args.input_file_path)
    scc.generate_question_and_answers(args.output_folder_path)