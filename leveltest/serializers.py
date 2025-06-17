from rest_framework import serializers
from .models import LevelQuestion

class LevelQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelQuestion
        fields = ['id', 'question', 'type', 'level', 'option_a', 'option_b', 'option_c', 'option_d', 'correct']
