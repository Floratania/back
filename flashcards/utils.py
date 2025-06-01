import spacy
from wordfreq import word_frequency
import re
import os

nlp = spacy.load("en_core_web_sm")

# Завантаження списку Oxford 3000
def load_oxford_3000():
    oxford_path = os.path.join(os.path.dirname(__file__), 'data', 'The_Oxford_3000.txt')
    with open(oxford_path, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())

OXFORD_3000 = load_oxford_3000()

def count_syllables(word):
    return len(re.findall(r'[aeiouy]+', word.lower()))

def determine_difficulty(word):
    word = word.lower()
    freq = word_frequency(word, 'en')
    syllables = count_syllables(word)
    length = len(word)
    doc = nlp(word)
    pos = doc[0].pos_ if doc else 'X'
    is_common = word in OXFORD_3000

    score = 0
    if freq > 0.001:
        score += 0
    elif freq > 0.0001:
        score += 1
    else:
        score += 2

    if syllables > 3:
        score += 1
    if length > 8:
        score += 1
    if pos not in ['NOUN', 'PROPN']:
        score += 1
    if not is_common:
        score += 1

    if score <= 1:
        return 'easy'
    elif score <= 3:
        return 'medium'
    else:
        return 'hard'
