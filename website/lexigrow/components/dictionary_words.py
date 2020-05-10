import nltk
from nltk.stem import WordNetLemmatizer

from frontend.models import SeenWordInfo, WordInfo
from lexigrow.components.context2vec.context2vec import Context2Vec
from lexigrow.components.oxford_learners_dict_wrapper import OxfordLearnersDictWrapper
from common.pos import nltk_to_wordnet_pos, nltk_to_oxford_pos
from lexigrow.components.word_dfficulty_classifier_wrapper import cefr_to_num

dictionary = OxfordLearnersDictWrapper()
context2vec = Context2Vec()
lemmatizer = WordNetLemmatizer()


def order_words_info(words_info, user_level):
    level_less_equal = []
    level_greater = []
    unknown_level = []

    user_level_num = cefr_to_num.get(user_level, 6) # if Unknown, give one more than the highest number

    for word_info in words_info:
        level_num = cefr_to_num.get(word_info["level"], None) # if work is Unknown, give None
        if level_num is None:
            unknown_level.append(word_info)
        elif level_num <= user_level_num:
            level_less_equal.append(word_info)
        else:
            level_greater.append(word_info)

    level_less_equal = sorted(level_less_equal, key=lambda x: cefr_to_num.get(x["level"], 0), reverse=True)
    level_greater = sorted(level_greater, key=lambda x: cefr_to_num.get(x["level"], 0))

    return level_less_equal + level_greater + unknown_level


def get_seen_words(user, phrase):
    words_list = phrase.split()

    seen_words = {}
    for index, word in enumerate(words_list):
        lemma = get_lemma(index, words_list)

        seen_word_info_entries = SeenWordInfo.objects.filter(word_info__word=lemma, user=user)
        if seen_word_info_entries.exists():
            seen_words[lemma.title()] = ", ".join([entry.word_info.pos for entry in seen_word_info_entries])
    return seen_words


def set_has_seen(user, words_info):
    for word_info in words_info:
        word_info_entry = WordInfo.objects.get(word=word_info["word"], pos=word_info["pos"])
        entry, _ = SeenWordInfo.objects.get_or_create(user=user, word_info=word_info_entry)
        entry.save()


def similar_dictionary_word(similar_words, phrase, target_index, target_word_infos, max_word_num=5, max_level=6):
    target_word_list = {x["word"] for x in target_word_infos}
    target_pos_list = {x["pos"] for x in target_word_infos}

    words_info = []
    for word_info in dictionary.get_words_info_gen(similar_words):
        if word_info["word"] not in target_word_list and word_info["pos"] in target_pos_list and len(word_info["word"].split()) == 1 and cefr_to_num.get(word_info["level"], 6) <= max_level:
            if len(word_info["details"]) > 1:
                sorted_details = context2vec.sorted_similar_contexts(target_index, phrase, word_info)
                word_info["details"] = [sorted_details[0]]
            words_info.append(word_info)
        if len(words_info) >= max_word_num:
            break

    return words_info


def get_lemma(target_index, word_list):
    word = word_list[target_index]
    nltk_target_pos = nltk.pos_tag(word_list)[target_index][1]  # One to get POS, returns word POS tuple
    wordnet_target_pos = nltk_to_wordnet_pos(nltk_target_pos)
    return lemmatizer.lemmatize(word, pos=wordnet_target_pos)


def get_word_info(word=None, target_index=None, phrase=None, user=None):
    if phrase is not None:
        word_list = phrase.split()
        lemma = get_lemma(target_index, word_list)
    else:
        lemma = lemmatizer.lemmatize(word)

    words_info = dictionary.get_word_info(lemma)

    if words_info is None:
        return None

    words_info = [word_info for word_info in words_info if word_info["details"]]

    if len(words_info) == 1:  # If there is only one word (e.g. only noun, not noun and verb)
        return words_info
    elif phrase is not None:
        oxford_target_pos = nltk_to_oxford_pos(nltk.pos_tag(word_list)[target_index][1])

        for info in words_info:
            if info["pos"] == oxford_target_pos:
                return [info]

    return words_info
