from django.db import models
from django.contrib.auth.models import User

class LevelQuestion(models.Model):
    # Питання, типи та рівень
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct = models.CharField(max_length=1)  # Правильна відповідь (A, B, C, D)
    level = models.CharField(max_length=3, choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')])
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.question

from django.db import models
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(LevelQuestion, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    level = models.CharField(max_length=5, default='A1')  # Add this field to store the level

    def __str__(self):
        return f"{self.user} - {self.question} - {self.selected} - {self.is_correct}"


class LevelTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=3)
    score = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.level} - {self.score}'
