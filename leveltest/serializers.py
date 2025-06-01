# leveltest/serializers.py
from rest_framework import serializers
from leveltest.models import LevelQuestion

class LevelQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelQuestion
        exclude = ['correct']  # don’t send answer to frontend
