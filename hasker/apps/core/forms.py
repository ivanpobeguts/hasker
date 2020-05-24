from django import forms

from .models import Question, Answer


class TagsField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        return value.split(',')


class AskForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 70}), label='Text')
    tags = TagsField()

    class Meta:
        model = Question
        fields = ('title', 'body', 'tags')

    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tags')
        if len(tags) > 3:
            self.add_error('tags', "You cannot add more than 3 tags")
        return cleaned_data


class AnswerForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 70}), label='')

    class Meta:
        model = Answer
        fields = ('body',)