from .models import UserTrainingPreferences
from rest_framework import serializers
from .models import Flashcard, WordSet, UserFlashcardProgress, UserWordSet

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'word', 'definition', 'set']

class WordSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordSet
        fields = ['id', 'name', 'is_public', 'owner']
        read_only_fields = ['owner']


class UserFlashcardProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFlashcardProgress
        fields = ['flashcard', 'status']

class UserWordSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWordSet
        fields = ['wordset']
        
        


class UserTrainingPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrainingPreferences
        fields = ['selected_statuses']

