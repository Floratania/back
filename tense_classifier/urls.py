# urls.py
from django.urls import path
from tense_classifier.api.views import predict_tense

urlpatterns = [
    path('predict/', predict_tense),
    # path('check-grammar/', check_grammar, name='check_grammar'),
]
# urlpatterns = [