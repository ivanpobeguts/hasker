from urllib.parse import urlencode

import pytest
from django.urls import reverse

from ..models import Question, Answer


@pytest.mark.django_db
def test_index_ok(client, question):
    response = client.get('/?order_by=hot')
    assert response.status_code == 200
    assert response.context_data['question_list'].count() == 1


@pytest.mark.django_db
def test_search_ok(client, question):
    response = client.get('/search?q=Title1')
    assert response.status_code == 200
    assert response.context_data['question_list'].count() == 1


@pytest.mark.django_db
def test_search_by_tag_ok(client, question, tag):
    question.tags.add(tag)
    question.save()
    response = client.get('/tags?q=tag1')
    assert response.status_code == 200
    assert response.context_data['question_list'].count() == 1


@pytest.mark.django_db
def test_search_redirect_to_tag_ok(client, question, tag):
    question.tags.add(tag)
    question.save()
    response = client.get('/search_redirect?q=tag:tag1')
    assert response.status_code == 302
    assert response.url == '/tags?q=tag1'


@pytest.mark.django_db
def test_ask_ok(client, person):
    assert Question.objects.count() == 0
    data = urlencode({
        'title': 'Title',
        'body': 'Why?',
        'tags': 'tag1,tag2'
    })
    client.login(username='testuser', password='12345')
    client.post(reverse('ask'), data=data, content_type='application/x-www-form-urlencoded')

    question = Question.objects.get()
    assert question.title == 'Title'
    assert question.body == 'Why?'
    assert question.author.username == 'testuser'
    assert [t.name for t in question.tags.all()] == ['tag1', 'tag2']


@pytest.mark.django_db
def test_get_question_ok(client, question):
    response = client.get('/question/title1')
    assert response.status_code == 200
    assert response.context_data['question'].title == 'Title1'


@pytest.mark.django_db
def test_create_answer_ok(client, question, person):
    assert Answer.objects.count() == 0
    data = urlencode({
        'body': 'Answer',
    })
    client.login(username='testuser', password='12345')
    client.post('/question/title1', data=data, content_type='application/x-www-form-urlencoded')

    answer = Answer.objects.get()
    assert answer.body == 'Answer'


@pytest.mark.django_db
def test_vote_for_question_ok(client, question, person):
    assert question.rating == 0
    data = urlencode({
        'value': '1',
        'entity_id': question.id,
        'entity_type': 'question',
    })
    client.login(username='testuser', password='12345')
    header = {'HTTP_REFERER': '/question/title1'}
    client.post(
        reverse('vote'),
        data=data,
        content_type='application/x-www-form-urlencoded',
        **header)

    queried_question = Question.objects.get()
    assert queried_question.rating == 1


@pytest.mark.django_db
def test_mark_answer_correct_ok(client, question, another_person, person):
    answer = Answer(body='Correct answer', author=person, question=question)
    assert not answer.is_correct
    answer.save()
    client.login(username='another_testuser', password='12345')
    header = {'HTTP_REFERER': '/question/title1'}
    client.post(
        reverse('correct_answer'),
        data=urlencode({'id': answer.id}),
        content_type='application/x-www-form-urlencoded',
        **header)

    queried_answer = Answer.objects.get()
    assert queried_answer.is_correct
