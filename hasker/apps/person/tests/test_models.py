from unittest.mock import Mock

import pytest

from ..models import Person


@pytest.mark.django_db
def test_create_person_with_avatar():
    avatar = Mock(url='path/to/url')
    new_person = Person(username='John', email='john.don@gmail.com', avatar=avatar)
    assert new_person.username == 'John'
    assert new_person.email == 'john.don@gmail.com'
    assert new_person.avatar_url == 'path/to/url'


@pytest.mark.django_db
def test_create_person_without_avatar():
    new_person = Person(username='John', email='john.don@gmail.com')
    new_person.save()
    assert Person.objects.count() == 1
    assert new_person.username == 'John'
    assert new_person.email == 'john.don@gmail.com'
    assert new_person.avatar_url == '/media/user_images/default/default_avatar.jpg'
