from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect

from .models import Question
from .forms import AskForm


class IndexView(TemplateView):
    template_name = 'index.html'


class AskView(CreateView):
    model = Question
    form_class = AskForm
    template_name = 'core/ask.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.object = None

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('index')
        else:
            return self.form_invalid(form)