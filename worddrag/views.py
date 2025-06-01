import random
import spacy
from nltk.corpus import wordnet as wn
from django.http import JsonResponse
from rest_framework.decorators import api_view

import re
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import spacy

nlp = spacy.load("en_core_web_sm")

def normalize(text):
    """Нормалізує речення: прибирає пунктуацію, переводить у нижній регістр, видаляє зайві пробіли"""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

@csrf_exempt
def check_sentence(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sentence = data.get("sentence", "")
        original_sentence = data.get("original_sentence", "")

        norm_user = normalize(sentence)
        norm_original = normalize(original_sentence)

        return JsonResponse({
            "is_correct": norm_user == norm_original,
            "sentence": sentence,
            "original_sentence": original_sentence
        })




TEMPLATES = [
    # A1–A2: Просте ствердження
    "The {adj} {noun1} {verb}s the {noun2}.",
    "{noun1} likes to {verb} every day.",
    "She always {verb}s with a {adj} {noun2}.",
    "A {noun1} can {verb} very well.",
    "They {verb} in the {noun2} every morning.",
    
    # A2–B1: Запитання, складніші речення
    "Why does the {noun1} {verb} the {noun2}?",
    "Do you want to {verb} the {adj} {noun2}?",
    "The {noun1} didn’t {verb} the {noun2} because it was {adj}.",
    "Can a {adj} {noun1} really {verb} that fast?",
    "Does the {noun1} know how to {verb} a {noun2}?",

    # B1–B2: Складні речення з підрядними
    "Although the {noun1} was {adj}, it managed to {verb} the {noun2}.",
    "If the {noun1} {verb}s, the {noun2} will be {adj}.",
    "Since the {noun2} is {adj}, the {noun1} should {verb} now.",
    "While the {adj} {noun1} tried to {verb}, the {noun2} escaped.",
    "The {noun1}, who was very {adj}, tried to {verb} the {noun2}.",

    # Речення з прислівниками
    "The {noun1} {verb}s {adverb} in the {noun2}.",
    "Suddenly, the {adj} {noun1} began to {verb}.",
    "The {noun1} {verb}s the {noun2} {adverb}.",
    "He {adverb} {verb}s the {noun2} every afternoon.",

    # Складені речення
    "The {noun1} {verb}ed the {noun2} and then {verb}ed away.",
    "First, the {adj} {noun1} tried to {verb}, but it failed.",
    "Either the {noun1} {verb}s the {noun2}, or it gets {adj}.",
]

def get_word_by_pos(pos):
    synsets = list(wn.all_synsets(pos))
    while True:
        syn = random.choice(synsets)
        word = syn.lemmas()[0].name()
        if "_" not in word and word.isalpha():
            return word

def generate_filled_sentence():
    template = random.choice(TEMPLATES)
    values = {
        'noun1': get_word_by_pos('n'),
        'noun2': get_word_by_pos('n'),
        'verb': get_word_by_pos('v'),
        'adj': get_word_by_pos('a')
    }
    return template.format(**values)

@api_view(['GET'])
def get_generated_sentence(request):
    sentence = generate_filled_sentence()
    words = sentence.split()
    shuffled = words.copy()
    random.shuffle(shuffled)

    # граматичний аналіз з spaCy
    doc = nlp(sentence)
    pos_tags = [{'word': token.text, 'pos': token.pos_} for token in doc]

    return JsonResponse({
        "original": sentence,
        "shuffled": shuffled,
        "pos": pos_tags
    })
