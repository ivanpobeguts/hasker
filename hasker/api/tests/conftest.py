from django.contrib.auth import get_user_model
from pytest import fixture
from rest_framework.test import APIClient

from hasker.apps.core.models import Answer, Question, Tag


@fixture
def person():
    return get_user_model().objects.create_user(username='testuser', password='12345', email='test@gmail.com')


@fixture
def auth_client(person):
    client = APIClient()
    client.force_authenticate(user=person)
    return client


@fixture
def question(person):
    question = Question(title='Title1', body='Where is test?', author=person, slug='title1')
    question.save()
    return question


@fixture
def tag():
    tag = Tag(name='tag1')
    tag.save()
    return tag


@fixture
def answer(question, person):
    answer = Answer(question=question, author=person, body='Answer1')
    answer.save()
    return answer
