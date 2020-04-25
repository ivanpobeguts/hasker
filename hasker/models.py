from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone


class Person(AbstractUser):
    avatar = models.ImageField(blank=True)

    @classmethod
    def get_by_email(cls, email):
        return cls.objects.filter(email=email)


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
