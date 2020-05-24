from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Question(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="questions")
    tags = models.ManyToManyField("Tag", blank=True, related_name="questions", max_length=10)
    slug = models.SlugField(unique=True, null=True)
    rating = models.IntegerField(default=0)

    def update_rating(self, value):
        self.rating += value
        self.save()

    @classmethod
    def trending(cls, n=5):
        return Question.objects.all().order_by('-rating', '-created_at')[:n]


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)
    body = models.CharField(max_length=1000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="answers")
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def update_rating(self, value):
        self.rating += value
        self.save()


class VoteAnswer(models.Model):
    value = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="answer_vote")
    entity = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="answer_vote")


class VoteQuestion(models.Model):
    value = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="question_vote")
    entity = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_vote")
