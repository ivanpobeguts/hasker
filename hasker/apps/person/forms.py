from io import BytesIO
from PIL import Image

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import Person


class AvatarWidget(forms.widgets.ClearableFileInput):

    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = ''
        if value:
            img_html = mark_safe(f'<img src="{value.url}"/><br>')
        return f'{img_html}{input_html}'


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


class SignUpForm(forms.ModelForm, AvatarMixin):
    password = forms.CharField(widget=forms.PasswordInput())
    rep_password = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('rep_password'):
            self.add_error('rep_password', "Passwords don't match")

    class Meta:
        model = Person
        fields = ('username', 'password', 'rep_password', 'email', 'avatar')


class SignInForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'password')


class SettingsForm(forms.ModelForm, AvatarMixin):
    avatar = forms.ImageField(widget=AvatarWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

    class Meta:
        model = Person
        fields = ('username', 'email', 'avatar')
