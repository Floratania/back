from django.urls import path
from .views import NLPPracticeView, TextToSpeechView

urlpatterns = [
    path("practice/nlp/", NLPPracticeView.as_view()),
    path("practice/tts/", TextToSpeechView.as_view()),
]
