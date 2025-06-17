from .models import UserTrainingPreferences
from rest_framework import serializers
from .models import Flashcard, WordSet, UserFlashcardProgress, UserWordSet

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = ['id', 'word', 'definition', 'set']

class WordSetSerializer(serializers.ModelSerializer):
    user_has_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = WordSet
        fields = ['id', 'name', 'is_public', 'owner', 'user_has_subscribed']

    def get_user_has_subscribed(self, obj):
        user = self.context['request'].user
        return obj.userwordset_set.filter(user=user).exists()


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

