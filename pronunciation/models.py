from django.db import models
from django.contrib.auth.models import User

class PronunciationAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    spoken_text = models.TextField()
    score = models.FloatField()
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.word} -> {self.spoken_text} ({'✓' if self.is_correct else '✗'})"

