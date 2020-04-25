from django import forms
from .models import Person


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = Person
        fields = ('username', 'password', 'email', 'avatar')



