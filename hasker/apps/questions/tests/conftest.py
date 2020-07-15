from django.contrib.auth import get_user_model
from pytest import fixture

from ..models import Question, Tag


@fixture
def person():
    return get_user_model().objects.create_user(username='testuser', password='12345', email='test@gmail.com')


@fixture
def another_person():
    return get_user_model().objects.create_user(username='another_testuser', password='12345', email='test@gmail.com')


@fixture
def question(another_person):
    question = Question(title='Title1', body='Where is test?', author=another_person, slug='title1')
    question.save()
    return question


@fixture
def tag():
    tag = Tag(name='tag1')
    tag.save()
    return tag


@fixture
def trending_questions(person):
    question1 = Question(title='Title1', body='Where is test?', author=person, slug='title1', rating=5)
    question1.save()
    question2 = Question(title='Title2', body='Where is test?', author=person, slug='title2', rating=10)
    question2.save()
