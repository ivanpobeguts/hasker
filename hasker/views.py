from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import CreateView, TemplateView

from .forms import SignUpForm
from .models import Person


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = Person
    form_class = SignUpForm
    template_name = 'person/sign_up.html'
    success_url = '/register/'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        person = self.object
        person.set_password(self.object.password)
        person.save()
        new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, new_user)
        messages.success(self.request, 'Registration successful')
        return valid
