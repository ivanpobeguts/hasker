from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, FormView
from django.shortcuts import redirect

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


class SettingsView(LoginRequiredMixin, FormView, SuccessMessageMixin):
    model = Person
    form_class = SettingsForm
    template_name = 'person/settings.html'
    success_url = '/settings/'
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.save()
            return redirect('settings')
        else:
            return self.form_invalid(form)

    def get_initial(self):
        args = super().get_initial()
        args.update({
            'username': self.request.user.username,
            'email': self.request.user.email,
            'avatar': self.request.user.avatar,
        })
        return args