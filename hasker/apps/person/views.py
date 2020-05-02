from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, FormView

from .forms import SignUpForm, SettingsForm
from .models import Person


class SignUpView(CreateView):
    model = Person
    form_class = SignUpForm
    template_name = 'person/sign_up.html'
    success_url = '/register/'

    def form_valid(self, form):
        valid = super().form_valid(form)
        person = self.object
        person.set_password(self.object.password)
        person.save()
        new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, new_user)
        messages.success(self.request, 'Registration successful')
        return valid


class SettingsView(FormView, SuccessMessageMixin):
    model = Person
    form_class = SettingsForm
    template_name = 'person/settings.html'
    success_url = '/settings/'

    def get_initial(self):
        args = super().get_initial()
        args.update({
            'username': self.request.user.username,
            'email': self.request.user.email,
            'avatar': self.request.user.avatar,
        })
        return args