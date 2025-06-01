# leveltest/models.py
from django.db import models
from django.contrib.auth.models import User

# leveltest/models.py
from django.db import models

class LevelQuestion(models.Model):
    TYPE_CHOICES = [
        ('grammar', 'Grammar'),
        ('idiom', 'Idiom'),
        ('phrasal', 'Phrasal Verb'),
        ('listening', 'Listening'),
    ]

    LEVEL_CHOICES = [
        ('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'),
        ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct = models.CharField(max_length=1)
    audio_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.level} - {self.type}: {self.question[:50]}"


class LevelTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=LevelQuestion.LEVEL_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.level} ({self.score}%)"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(LevelQuestion, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1)
    is_correct = models.BooleanField()
