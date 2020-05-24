from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Person(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to='user_images/')

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return settings.DEFAULT_AVATAR_URL