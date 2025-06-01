# importer.py
import os
from django.conf import settings
from flashcards.models import WordSet, Flashcard
from django.db import IntegrityError
from .translator import translate  # 👈 імпортуємо функцію перекладу

FILE_SOURCES = {
    "oxford3000": "The_Oxford_3000.txt",
    "oxford5000": "Oxford_5000.txt",
    "phrases": "Oxford Phrase List.txt",
}

def import_words_from_file(filename, wordset_name, user, is_public=False, file_dir=None):
    if not file_dir:
        file_dir = os.path.join(settings.BASE_DIR, 'flashcards', 'data')

    file_path = os.path.join(file_dir, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не знайдено: {file_path}")

    with open(file_path, encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    word_set, _ = WordSet.objects.get_or_create(name=wordset_name, owner=user, is_public=is_public)

    count = 0
    for word in words:
        try:
            translation = translate(word).lower()
            # print(f"✅ Translating: {word} -> {translation}")

            Flashcard.objects.create(word=word, definition=translation, set=word_set)
            count += 1
        except IntegrityError:
            continue
        except Exception as e:
            print(f"❌ '{word}': {e}")
            continue

    return count, word_set.id
