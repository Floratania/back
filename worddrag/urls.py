from django.urls import path
from .views import get_generated_sentence, check_sentence

urlpatterns = [
    path('wd/', get_generated_sentence, name='get_generated_sentence'), 
    path('check/', check_sentence, name='check_sentence'),

]
