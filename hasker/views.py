from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView

from .forms import SignUpForm, SignInForm
from .models import Person


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


class SignInView(LoginView):
    template_name = 'person/sign_in.html'


class SignOutView(LogoutView):
    pass
