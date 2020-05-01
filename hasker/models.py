from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.templatetags.static import static
from django.conf import settings


class Person(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to='user_images/')

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return static(settings.DEFAULT_AVATAR_URL)


class Question(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="questions")
    tags = models.ManyToManyField("Tag", blank=True, related_name="questions")


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)
    body = models.CharField(max_length=150)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="answers")
    created_at = models.DateTimeField(default=timezone.now)
