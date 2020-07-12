from django.db import models
from django.contrib.auth import get_user_model
from django.http import Http404
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class Question(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField('Tag', blank=True, related_name='questions', max_length=10)
    slug = models.SlugField(unique=True, null=True)
    rating = models.IntegerField(default=0)

    def update_params(self, author, tag_names):
        self.author = author
        self.slug = slugify(self.title)[:40]
        self.save()
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            self.tags.add(tag)

    def update_rating(self, value):
        self.rating += value
        self.save()

    @classmethod
    def trending(cls, n=5):
        return cls.objects.all().order_by('-rating', '-created_at')[:n]

    @classmethod
    def find_by_title(cls, param):
        return cls.objects.filter(title__icontains=str(param))

    @classmethod
    def find_by_tag(cls, param):
        return cls.objects.filter(tags__name=str(param))


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)
    body = models.CharField(max_length=1000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def update_rating(self, value):
        self.rating += value
        self.save()

    def update_params(self, question, author):
        self.question = question
        self.author = author
        self.save()

    def mark_correct(self, user):
        if self.question.author.id == user.id:
            self.is_correct = True
            self.save()

    @classmethod
    def get_correct(cls, question):
        answers = (cls.objects.filter(question=question).order_by('-rating', '-created_at'))
        return answers, any(answer.is_correct for answer in answers)


class VoteAnswer(models.Model):
    value = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='answer_vote')
    entity = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_vote')


class VoteQuestion(models.Model):
    value = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='question_vote')
    entity = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_vote')


def vote(entity_id, entity_type, person, value):
    try:
        if entity_type == 'question':
            entity = get_object_or_404(Question, id=entity_id)
            if entity in person.questions.all():
                return
            vote_obj = VoteQuestion.objects.get_or_create(author_id=person.id, entity_id=entity_id)[0]
        else:
            entity = get_object_or_404(Answer, id=entity_id)
            if entity in person.answers.all():
                return
            vote_obj = VoteAnswer.objects.get_or_create(author_id=person.id, entity_id=entity_id)[0]
    except Http404:
        return

    with transaction.atomic():
        new_value = 0 if value == vote_obj.value else value
        entity.update_rating(new_value - vote_obj.value)
        vote_obj.value = new_value
        vote_obj.save()
