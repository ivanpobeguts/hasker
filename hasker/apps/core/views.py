from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Question, Tag
from .forms import AskForm


class IndexView(ListView):
    template_name = 'index.html'
    model = Question
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = qs.order_by("-created_at")
        return qs


class AskView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = AskForm
    template_name = 'core/ask.html'
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.object = None

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            tag_names = form.cleaned_data.get('tags')
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
            return redirect('index')
        else:
            return self.form_invalid(form)

