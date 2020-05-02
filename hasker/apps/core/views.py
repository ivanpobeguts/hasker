from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import CreateView, TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'