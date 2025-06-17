# leveltest/urls.py
from django.urls import path
from .views import LevelTestView, FinalLevelTestView, generate_ai

urlpatterns = [
    path('leveltest/', LevelTestView.as_view(), name='leveltest'),
     path('final/', FinalLevelTestView.as_view(), name='final-level-test'),
    path('ai_generate/', generate_ai, name='ai-generate'),
]
