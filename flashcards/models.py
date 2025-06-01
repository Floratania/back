from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class WordSet(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='word_sets', null=True, blank=True)
    is_public = models.BooleanField(default=False)  # Oxford sets will be public

    def __str__(self):
        return self.name

class Flashcard(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField(blank=True)
    set = models.ForeignKey(WordSet, on_delete=models.CASCADE, related_name='flashcards')

    def __str__(self):
        return self.word

class UserFlashcardProgress(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('learning', 'Learning'),
        ('learned', 'Learned'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    class Meta:
        unique_together = ('user', 'flashcard')

class UserWordSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wordset = models.ForeignKey(WordSet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'wordset')
        
        # flashcards/models.py


class UserTrainingPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_statuses = models.JSONField(default=list)  # 👈 ОБОВ’ЯЗКОВО!


@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        UserTrainingPreferences.objects.create(user=instance)