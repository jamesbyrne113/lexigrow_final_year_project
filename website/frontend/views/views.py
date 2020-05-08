import json
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from frontend.models import LexiGrowUser

from lexigrow.components import phrase_info
from lexigrow.components.dictionary_words import set_has_seen, get_seen_words, order_words_info
from lexigrow.components.word_dfficulty_classifier_wrapper import cefr_to_num


def get_common_page_context(request, user=None):
    if not user:
        user = LexiGrowUser.objects.get(email=request.user.email)

    return {
        "userFullName": user.get_full_name(),
        "userLevel": user.level,
    }


def process_phrase(request):
    phrase_raw = request.GET.get('phrase').replace("%20", " ").lower()
    return re.sub(r'[^a-z|\s]+', '', phrase_raw)


@login_required
def index_view(request):
    page_context = get_common_page_context(request)
    context = {'page_context': json.dumps(page_context)}
    return render(request, 'frontend/index.html', context)


@login_required
def select_target_word_view(request):
    phrase = process_phrase(request)

    page_context = get_common_page_context(request)
    page_context.update({
        "phrase": phrase,
        "hasTargetLinks": phrase_info.are_clickable_words(phrase),
    })

    context = {"page_context": json.dumps(page_context)}
    return render(request, 'frontend/select_target_word.html', context)


@login_required
def phrase_info_view(request):
    user = LexiGrowUser.objects.get(email=request.user.email)

    phrase = process_phrase(request)
    target_index = int(request.GET.get('targetIndex'))

    request.session["phrase"] = phrase
    request.session["targetIndex"] = target_index

    target_word_infos = phrase_info.get_target_word_infos(target_index=target_index, phrase=phrase)
    seen_words = get_seen_words(user, phrase)

    page_context = get_common_page_context(request, user)
    page_context.update({
        "phrase": phrase,
        "targetIndex": target_index,
        "targetWordsInfo": target_word_infos,
        "hasTargetLinks": phrase_info.are_clickable_words(phrase),
        "seenWords": seen_words,
    })

    context = { "page_context": json.dumps(page_context) }
    return render(request, 'frontend/phrase_info.html', context)


@login_required
def similar_context_info_view(request):
    user = LexiGrowUser.objects.get(email=request.user.email)

    phrase = process_phrase(request)
    target_index = int(request.GET.get('targetIndex'))

    max_level = 6 if user.show_harder_words else cefr_to_num.get(user.level, 6)

    target_words_info = phrase_info.get_target_word_infos(target_index=target_index, phrase=phrase)
    context_words_info = phrase_info.get_similar_context(phrase, target_index, target_words_info, max_level=max_level)

    set_has_seen(user, context_words_info)

    return JsonResponse({"wordsInfo": order_words_info(context_words_info, user.level)})


@login_required
def similar_meaning_info_view(request):
    user = LexiGrowUser.objects.get(email=request.user.email)

    phrase = process_phrase(request)
    target_index = int(request.GET.get('targetIndex'))

    max_level = 6 if user.show_harder_words else cefr_to_num.get(user.level, 6)

    target_word_infos = phrase_info.get_target_word_infos(target_index=target_index, phrase=phrase)
    meaning_word_info = phrase_info.get_similar_meaning(phrase, target_index, target_word_infos, max_level=max_level)

    set_has_seen(user, meaning_word_info)

    return JsonResponse({"wordsInfo": order_words_info(meaning_word_info, user.level)})


@login_required
def similar_meaning_wordnet_info_view(request):
    user = LexiGrowUser.objects.get(email=request.user.email)

    phrase = process_phrase(request)
    target_index = int(request.GET.get('targetIndex'))

    max_level = 6 if user.show_harder_words else cefr_to_num.get(user.level, 6)

    target_word_infos = phrase_info.get_target_word_infos(target_index=target_index, phrase=phrase)
    meaning_word_info = phrase_info.get_similar_meaning_wordnet(phrase, target_index, target_word_infos, max_level=max_level)

    set_has_seen(user, meaning_word_info)

    return JsonResponse({"wordsInfo": order_words_info(meaning_word_info, user.level)})


@login_required
def same_sound_info_view(request):
    user = LexiGrowUser.objects.get(email=request.user.email)

    phrase = process_phrase(request)
    target_index = int(request.GET.get('targetIndex'))
    target_word = phrase.split()[target_index]

    max_level = 6 if user.show_harder_words else cefr_to_num.get(user.level, 6)

    sound_word_info = phrase_info.get_same_sound(target_word, max_level)

    set_has_seen(user, sound_word_info)

    tuple_words_info = {(word_info["word"].title(), word_info["level"]) for word_info in sound_word_info}
    dict_words_info = [{"word": word_info[0], "level": word_info[1]} for word_info in tuple_words_info]
    ordered_words_info = order_words_info(dict_words_info, user.level)

    return JsonResponse({"wordsInfo": list(ordered_words_info)})

