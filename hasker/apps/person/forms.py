from django import forms
from django.utils.safestring import mark_safe

from .mixins import AvatarMixin
from .models import Person


class AvatarWidget(forms.widgets.ClearableFileInput):

    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        return ''.join([mark_safe(f'<img src="{value.url}"/><br>'), input_html]) if value else input_html


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
