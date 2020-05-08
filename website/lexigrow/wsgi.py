"""
WSGI config for lexigrow project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from lexigrow.components.context2vec.context2vec import Context2Vec
from lexigrow.components.word_dfficulty_classifier_wrapper import WordDifficultyClassifierWrapper
from lexigrow.components.word2vec import Word2Vec

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lexigrow.settings')

application = get_wsgi_application()

# Preload context2vec, word2vec and WordDifficultyClassifier models
wdc = WordDifficultyClassifierWrapper()
print("Finished loading Word Difficulty Classifier Model")
w2v = Word2Vec()
print("Finished loading Word2Vec Model")
context2vec = Context2Vec()
print("Finished loading Context2Vec Model")
