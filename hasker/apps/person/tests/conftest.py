from django.contrib.auth import get_user_model
from pytest import fixture


@fixture
def person():
    return get_user_model().objects.create_user(username='testuser', password='12345', email='test@gmail.com')