from rest_framework import serializers
from .models import PronunciationAttempt

class PronunciationAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PronunciationAttempt
        fields = ['id', 'user', 'word', 'spoken_text', 'score', 'is_correct', 'timestamp']
        read_only_fields = ['user', 'timestamp']
