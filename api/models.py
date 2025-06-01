# from django.db import models
# from django.contrib.auth.models import User

# class Word(models.Model):
#     text = models.CharField(max_length=100)
#     translation = models.CharField(max_length=100)
#     example = models.TextField(blank=True)

#     def __str__(self):
#         return self.text

# class UserWordProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     word = models.ForeignKey(Word, on_delete=models.CASCADE)
#     is_learned = models.BooleanField(default=False)
#     review_count = models.IntegerField(default=0)
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'),  ('other', 'Інша')], blank=True)
    english_level = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
