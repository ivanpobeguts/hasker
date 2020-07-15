from os.path import dirname, join
from urllib.parse import urlencode

from django.core.files.images import ImageFile
from django.urls import reverse
import pytest

from ..models import Person

BASE_PATH = dirname(__file__)


@pytest.mark.django_db
def test_register_ok(client):
    data = urlencode({
        'username': 'John1',
        'password': 'pass',
        'rep_password': 'pass',
        'email': 'john_don@gmail.com'
    })
    client.post(reverse('sign_up'), data=data, content_type='application/x-www-form-urlencoded')
    person_query = Person.objects
    assert person_query.count() == 1
    assert person_query.get().username == 'John1'


@pytest.mark.django_db
def test_register_diff_passwords(client):
    data = urlencode({
        'username': 'John1',
        'password': 'pass',
        'rep_password': 'pass1',
        'email': 'john_don@gmail.com'
    })
    client.post(reverse('sign_up'), data=data, content_type='application/x-www-form-urlencoded')
    assert Person.objects.count() == 0


@pytest.mark.django_db
def test_settings_ok(client, person):
    assert person.avatar_url == '/static/img/user_images/default/default_avatar.jpg'

    client.login(username='testuser', password='12345')
    with open(join(BASE_PATH, 'files', 'test_avatar.png'), 'rb') as fp:
        image = ImageFile(fp)
        data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'avatar': image,
        }
        client.post(reverse('settings'), data=data)
    assert Person.objects.get().avatar_url.startswith('/media/user_images/test_avatar')