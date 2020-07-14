from rest_framework.test import APIClient

import pytest
from django.urls import reverse

from hasker.apps.core.models import Question, Answer


@pytest.mark.django_db
def test_index_ok(auth_client, question):
    response = auth_client.get('/api/v1/index?order_by=hot')
    assert response.status_code == 200
    assert response.data.get('count') == 1


@pytest.mark.django_db
def test_trending_ok(auth_client, question):
    response = auth_client.get('/api/v1/trending')
    assert response.status_code == 200
    assert response.data.get('count') == 1


@pytest.mark.django_db
def test_text_search_ok(auth_client, question):
    response = auth_client.get('/api/v1/search:text?q=Title1')
    assert response.status_code == 200
    assert response.data.get('count') == 1


@pytest.mark.django_db
def test_tag_search_ok(auth_client, question, tag):
    question.tags.add(tag)
    question.save()
    response = auth_client.get('/api/v1/search:tag?q=tag1')
    assert response.status_code == 200
    assert response.data.get('count') == 1


@pytest.mark.django_db
def test_get_question_ok(auth_client, question):
    response = auth_client.get('/api/v1/question/title1')
    assert response.status_code == 200
    assert response.data.get('slug') == 'title1'


@pytest.mark.django_db
def test_get_question_answers_ok(auth_client, answer):
    response = auth_client.get('/api/v1/question/title1/answers')
    assert response.status_code == 200
    assert response.data.get('count') == 1
    assert response.data.get('results')[0].get('body') == 'Answer1'