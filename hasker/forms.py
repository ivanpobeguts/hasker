from io import BytesIO
from PIL import Image

from django import forms
from django.conf import settings

from .models import Person


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    rep_password = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')
    username = forms.CharField(help_text=False)

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            image = Image.open(avatar.file)
            output_stream = BytesIO()

            resized_img = image.resize(settings.AVATAR_SIZE)
            resized_img.save(output_stream, format=avatar.image.format, quality=100)

            avatar.file = output_stream
            avatar.image = resized_img

        return avatar

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('rep_password'):
            # raise forms.ValidationError("Passwords don't match")
            self.add_error('rep_password', "Passwords don't match")

    class Meta():
        model = Person
        fields = ('username', 'password', 'rep_password', 'email', 'avatar')


class SignInForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'password')
