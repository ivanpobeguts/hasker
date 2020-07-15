from io import BytesIO
from PIL import Image

from django.conf import settings


class AvatarMixin:
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            image = Image.open(avatar.file)
            output_stream = BytesIO()

            resized_img = image.resize(settings.AVATAR_SIZE)
            resized_img.save(output_stream, format=image.format, quality=100)

            avatar.file = output_stream
            avatar.image = resized_img

        return avatar
