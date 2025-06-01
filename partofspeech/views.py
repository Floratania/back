# import random
# import nltk
# import spacy
# from nltk.corpus import brown
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from translator.utils import local_translate
# from gtts import gTTS
# from io import BytesIO
# from django.http import HttpResponse

# # Завантаження моделей
# nlp = spacy.load("en_core_web_sm")
# nltk.download("brown")
# nltk.download("punkt")
# # translator = Translator()


# class NLPPracticeView(APIView):
#     def get(self, request):
#         mode = request.query_params.get("type", "word")  # word|sentence
#         lang = request.query_params.get("lang", "uk")    # мова перекладу

#         if mode == "sentence":
#             sentence = " ".join(random.choice(brown.sents(categories="news")))
#             doc = nlp(sentence)
#             tokens = [token for token in doc if not token.is_punct]
#             target = random.choice(tokens) if tokens else doc[0]
#         else:
#             word = random.choice(brown.words(categories="news"))
#             doc = nlp(word)
#             target = doc[0]
#             sentence = word

#         # Переклад слова або фрази
#         translated = local_translate(target.text, direction="en_to_uk")

#         return Response({
#             "text": target.text,                    # обране слово
#             "translation": translated,              # переклад
#             "full": sentence if mode == "sentence" else "",  # повне речення
#             "pos": target.pos_.lower()              # частина мови
#         })


# class TextToSpeechView(APIView):
#     def get(self, request):
#         text = request.query_params.get("text", "")
#         if not text:
#             return Response({"error": "No text provided"}, status=400)

#         tts = gTTS(text=text, lang='en')
#         fp = BytesIO()
#         tts.write_to_fp(fp)
#         fp.seek(0)

#         return HttpResponse(fp.read(), content_type="audio/mpeg")
# views.py — NLPPracticeView
import random
import nltk
import spacy
from nltk.corpus import brown
from rest_framework.views import APIView
from rest_framework.response import Response
from gtts import gTTS
from io import BytesIO
from django.http import HttpResponse

from translator.utils import local_translate

nlp = spacy.load("en_core_web_sm")
nltk.download("brown")
nltk.download("punkt")

ALLOWED_POS = {"NOUN", "VERB", "ADJ", "ADV", "ADP"}  # додай ще за потребою

class NLPPracticeView(APIView):
    def get(self, request):
        mode = request.query_params.get("type", "word")  # word|sentence
        lang = request.query_params.get("lang", "uk")

        if mode == "sentence":
            sentence = " ".join(random.choice(brown.sents(categories="news")))
            doc = nlp(sentence)
            candidates = [t for t in doc if t.pos_ in ALLOWED_POS and t.text.isalpha()]
            target = random.choice(candidates) if candidates else doc[0]
            text = target.text
        else:
            # Генерація одного слова з фільтрацією
            while True:
                word = random.choice(brown.words(categories="news"))
                doc = nlp(word)
                token = doc[0]
                if token.pos_ in ALLOWED_POS and token.text.isalpha():
                    target = token
                    break
            text = target.text
            sentence = ""

        # 🔁 Переклад через твою локальну функцію
        translated = local_translate(text, direction="en_to_uk")

        return Response({
            "text": text,
            "translation": translated,
            "full": sentence,
            "correct_part": target.pos_.lower()
        })

class TextToSpeechView(APIView):
    def get(self, request):
        text = request.query_params.get("text", "")
        if not text:
            return Response({"error": "No text provided"}, status=400)

        tts = gTTS(text=text, lang='en')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        return HttpResponse(fp.read(), content_type="audio/mpeg")
